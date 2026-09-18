# Auditoría de seguridad de Liquity V2

Este directorio es el espacio de trabajo de la auditoría solicitada en este
chat. La revisión queda fijada al siguiente código fuente:

- Repositorio upstream: `https://github.com/liquity/bold`
- Commit: `ac91fda265707c63bd65c8d06c5c0533754bc3f5`

## Estructura

- `src/`: copia inmutable del código del commit auditado.
- `reports/`: hallazgos, pruebas de concepto y reporte final.

## Alcance de la revisión

La auditoría priorizará vulnerabilidades con impacto económico o riesgo de
bloqueo de fondos, en particular:

1. pérdida de precisión al distribuir recompensas o pérdidas de BOLD;
2. manipulación del ratio de colateral mediante donaciones o flash loans;
3. front-running y MEV al reclamar ganancias; y
4. transiciones de estado que permitan retirar fondos ya absorbidos por una
   liquidación.

## Incorporación del código fuente

El contenido de `src/` debe corresponder exactamente al commit indicado. Antes
de comenzar la auditoría se verificará con:

```bash
git rev-parse HEAD
```

El resultado esperado es
`ac91fda265707c63bd65c8d06c5c0533754bc3f5`. No se deben mezclar archivos de
otras revisiones, ya que invalidaría las referencias de líneas y las pruebas de
concepto del reporte.

