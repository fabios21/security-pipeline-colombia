# 🛡️ PipeShield

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Compatible-blue)](https://github.com/features/actions)

**PipeShield** es un pipeline de seguridad automatizado para GitHub Actions, orientado a detectar secretos expuestos, vulnerabilidades SAST y generar reportes en español con contexto colombiano.

## Características

- Detección de secretos con Gitleaks.
- Análisis estático SAST con Semgrep y reglas OWASP Top 10.
- Validación de hallazgos críticos, altos y medios.
- Bloqueo automático de PRs con secretos expuestos.
- Reporte HTML en español + datos crudos en JSON.
- Reglas y referencias alineadas con la Ley 1273, Ley 1581 y la SIC.
- Configuración de zona horaria `America/Bogota` e idioma `es_CO`.

## Uso

Agrega este paso a tu workflow (por ejemplo en `.github/workflows/security.yml`):

```yaml
name: PipeShield

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  security:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: PipeShield
        uses: fabios21/security-pipeline-colombia@v1.1.28
        with:
          scan-mode: pr-only
          semgrep-config: p/owasp-top-ten
          block-on-secrets: true
```

> **Nota:** el paso de checkout debe usar `fetch-depth: 0` para que el escaneo de secretos pueda comparar el historial del PR. Si dejas los inputs vacíos, la acción usa sus valores por defecto automáticamente.

## Configuración

La acción admite configuración para el modo de escaneo, reglas de Gitleaks y Semgrep, nivel de cumplimiento, formatos de reporte, umbrales de bloqueo y contactos de notificación. La referencia completa de entradas y salidas está disponible en [action.yml](action.yml).

## Reportes

Al finalizar el análisis, la acción publica automáticamente un artifact llamado **`security-reports`** que contiene:

- **`security-report-es_CO.html`** — reporte visual con los hallazgos, su ubicación, riesgo, solución técnica y referencias a la normatividad colombiana (Ley 1273, Ley 1581, Decreto 1377).
- **`gitleaks-report.json`** — salida cruda de Gitleaks con el detalle de cada secreto detectado (regla, archivo, línea, commit).

Además, en cada Pull Request se publica un comentario automático con el resumen de los secretos encontrados.

## Desarrollo

- [CONTRIBUTING.md](CONTRIBUTING.md): guía de contribución.
- [CHANGELOG.md](CHANGELOG.md): historial de versiones.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): código de conducta.

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).