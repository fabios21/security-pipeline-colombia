# 🔒 Security Pipeline Colombia

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Compatible-blue)](https://github.com/features/actions)

Pipeline de seguridad automatizado para GitHub Actions, orientado a detectar secretos expuestos, vulnerabilidades SAST y generar reportes en español con contexto colombiano.

## Características

- Detección de secretos con Gitleaks.
- Análisis estático SAST con Semgrep y reglas OWASP Top 10.
- Validación de hallazgos críticos, altos y medios.
- Reportes HTML, Markdown y JSON en español.
- Reglas y referencias alineadas con la Ley 1581 y la SIC.
- Configuración de zona horaria `America/Bogota` e idioma `es_CO`.

## Configuración

La acción admite configuración para el modo de escaneo, reglas de Gitleaks y Semgrep, nivel de cumplimiento, formatos de reporte, umbrales de bloqueo y contactos de notificación. La referencia completa de entradas y salidas está disponible en [action.yml](action.yml).

## Reportes

Al finalizar el análisis se generan, según la configuración, los archivos `gitleaks-report.json`, `semgrep-results.sarif`, `validation-result.json`, `visual-report.txt` y reportes de seguridad en HTML, Markdown o JSON. Consulta [REPORTES_GENERADOS.md](REPORTES_GENERADOS.md) para conocer su contenido.

## Desarrollo

- [CONTRIBUTING.md](CONTRIBUTING.md): guía de contribución.
- [CHANGELOG.md](CHANGELOG.md): historial de versiones.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): código de conducta.

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).