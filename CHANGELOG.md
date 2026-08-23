# Changelog

Todos los cambios notables en Security Pipeline Colombia serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.15] - 2026-08-23

### Fixed
- Se actualizó la marca de versión incluida dentro del HTML para identificar correctamente el generador publicado.

## [1.1.14] - 2026-08-23

### Fixed
- El análisis de cumplimiento ya no muestra `COMPLIANT` cuando existen vulnerabilidades SAST detectadas.
- Los hallazgos críticos, altos, medios y bajos ahora aparecen reflejados como acciones pendientes en el reporte.
- Se mejoró la redacción del resumen para evitar errores gramaticales con un único hallazgo.

## [1.1.13] - 2026-08-23

### Fixed
- El generador HTML se ejecuta directamente desde `GITHUB_ACTION_PATH`, evitando reutilizar copias antiguas del script.
- Se elimina el HTML previo antes de generar el reporte para impedir artifacts obsoletos.
- El reporte incorpora la versión del generador y el proceso falla si no contiene la sección de hallazgos individuales.
- La copia de scripts y plantillas de la action ahora falla explícitamente si no puede completarse.

## [1.1.12] - 2026-08-22

### Fixed
- El reporte HTML ahora muestra los hallazgos individuales detectados por Gitleaks y Semgrep.
- Cada hallazgo incluye severidad, regla, archivo, línea, descripción, mensaje del analizador cuando existe y recomendación de corrección.
- Los secretos se muestran únicamente enmascarados; nunca se renderiza `secret_full`.

## [1.1.11] - 2026-08-22

### Fixed
- Se corrigió el transporte de inputs con guion en la action (`semgrep-config`, `report-language` y políticas de bloqueo), usando variables de entorno y valores predeterminados seguros.
- Un fallo de Semgrep ya no puede convertirse en un reporte aprobado ni en un merge permitido.
- Los reportes de error siempre conservan el nombre `security-report-es_CO.html` cuando el idioma no llega informado.

## [1.1.10] - 2026-08-22

### Fixed
- Se corrigió la sintaxis YAML del fallback HTML que impedía cargar el manifiesto de la action en `v1.1.9`.

## [1.1.9] - 2026-08-22

### Fixed
- La acción genera siempre un reporte HTML no vacío, incluso cuando el análisis falla, el formato HTML fue omitido o el generador completo presenta un error.
- La generación de reportes se ejecuta tras fallos previos para conservar evidencia descargable en los artifacts.

## [1.1.8] - 2026-08-22

### Fixed
- El reporte visual ahora muestra acciones de remediación para vulnerabilidades altas, evitando una sección de recomendaciones vacía.
- Se aclaran las prioridades de secretos, vulnerabilidades críticas y vulnerabilidades altas.

## [1.1.7] - 2026-08-22

### Fixed
- Se fija Semgrep en `1.97.0` y se valida la configuración seleccionada antes de iniciar el escaneo.
- El log ahora muestra la ruta de configuración y el error de validación de Semgrep en lugar de exponer solo un código de salida.
- Las reglas SQL de prueba e incluidas usan patrones JavaScript completos y válidos para llamadas a `query()`.

## [1.1.6] - 2026-08-22

### Fixed
- Semgrep ya no sobrescribe un archivo `.semgrep.yml` proporcionado por el repositorio consumidor.
- La acción falla de forma explícita si Semgrep no puede ejecutar el análisis o no genera un reporte SARIF válido; no convierte un fallo de escaneo en cero hallazgos.
- Se reemplazó la configuración Semgrep incluida por reglas válidas, incluida la detección de consultas SQL construidas por concatenación.

## [1.1.5] - 2026-08-22

### Fixed
- El gate final ahora bloquea la ejecución cuando existen hallazgos medios o bajos y `require-approval-on-medium: true`.
- Los conteos de hallazgos medios y bajos se conservan en el resumen final y se reutilizan en la decisión de bloqueo.
- Cuando la aprobación no es requerida, el mensaje del gate informa explícitamente que esos hallazgos permiten continuar según la política configurada.

## [1.1.4] - 2026-08-22

### Fixed
- Se corrigió la clasificación de resultados SARIF de Semgrep que usan `level: error`, `warning` o `note` en lugar de `security-severity` numérico.
- Los hallazgos `ERROR` ahora se clasifican como altos y activan `block-on-high`.
- El conteo del resumen y el gate final usan el mismo normalizador de severidad.

## [1.1.3] - 2026-08-22

### Changed
- Se simplificó la presentación de la acción y se conserva el nombre `Security Pipeline Colombia (no install)` en Marketplace.
- Se restauró el checkout interno para que la acción sea autocontenida al ejecutarse como un step.
- Se redujo el README a documentación técnica de producto, configuración y reportes.

### Removed
- Guías, templates, workflows y documentación temporal creados durante el diagnóstico de Marketplace.

## [1.1.1] - 2026-08-16

### Fixed
- **Conteos multilinea en bash**: Corregido error `integer expression expected` cuando `jq` devolvia varias lineas (p. ej. SARIF con multiples runs).
- **GITHUB_ENV invalido**: Normalizacion de contadores antes de escribir `FINAL_SECRETS`, `FINAL_CRITICAL` y `FINAL_HIGH`.
- **Consulta TOTAL_RESULTS**: Reemplazado `.runs[]?.results? | length` por agregacion `[.runs[]?.results[]?] | length`.

## [1.0.6] - 2026-07-20

### Fixed
- **Gitleaks regex panic**: Fixed `regexp: Compile(\`**/test/**\`): error parsing regexp` error
- **Regex patterns**: Converted glob patterns to valid regular expressions in allowlist.paths
- **Python script typo**: Fixed `requires_approbation` typo in validate_security.py
- **Variable initialization**: Added proper initialization for SECRET_COUNT and vulnerability variables
- **Error handling**: Improved error handling in action.yml steps

### Added
- **Presentación visual mejorada**: Reportes gráficos con emojis y colores para hallazgos de seguridad
- **Nuevo script visual_report.py**: Genera reportes en formato visual con barras de progreso y tarjetas
- **CSS mejorado**: Estilos visuales mejorados en reportes HTML con animaciones y gradientes
- **Categorización de secretos**: Clasificación visual por tipo (AWS, Stripe, API keys, etc.)
- **Indicadores de severidad**: Barras visuales y badges de colores para diferentes niveles de riesgo

## [1.0.5] - 2026-07-20

### Fixed
- **Gitleaks regex error**: Fixed `invalid regex secret group 1, max regex secret group 0` error
- **Regex patterns**: Added capture groups for cédula detection rules
- **Pattern precision**: Improved cédula regex to 7-8 digits (standard Colombian ID)
- **Configuration validation**: All rules now properly validate with Gitleaks 8.18.1+

## [1.0.4] - 2026-07-20

### Fixed
- **Gitleaks configuration error**: Fixed `'Allowlist' expected a map, got 'slice'` error
- **TOML format**: Updated allowlist section to correct format for Gitleaks v8.x
- **Configuration compatibility**: Ensured config works with Gitleaks 8.18.1+

## [1.0.3] - 2026-07-20

### Fixed
- **File copy error**: Fixed `cp: '.gitleaks.toml' and '.gitleaks.toml' are the same file` error
- **Configuration handling**: Improved logic for default vs custom configuration files
- **Path comparison**: Added check to avoid copying file onto itself

### Improved
- **Error prevention**: Clear distinction between default and custom config paths
- **User feedback**: Better messages about which configuration is being used

## [1.0.2] - 2026-07-20

### Fixed
- **Gitleaks installation major fix**: Updated to use correct GitHub organization (`zricethezav` instead of `gitleaks`)
- **Multiple download methods**: Added 6 different URL formats and fallback versions
- **Go installation fix**: Corrected module path to `github.com/zricethezav/gitleaks/v8`
- **Error handling**: Action no longer fails if Gitleaks cannot be installed
- **Graceful degradation**: Pipeline continues with reduced functionality if tools missing
- **File validation**: Added fallback empty files for missing analysis results

### Improved
- **Robustness**: Action works even when tools cannot be automatically installed
- **User experience**: Clear error messages and manual installation instructions
- **Compatibility**: Better handling of missing dependencies

## [1.0.1] - 2026-07-20

### Fixed
- **Gitleaks installation**: Fixed 404 error by updating from v8.18.2 to v8.30.1
- **Locale warnings**: Resolved `setlocale: LC_ALL: cannot change locale (es_ES.UTF-8)` errors
- **Node.js version**: Added Node.js 22 setup to avoid Node 20 deprecation warnings
- **Installation robustness**: Added multiple download URL formats and Go installation backup
- **Error handling**: Improved verification and error messages for tool installation

### Security
- **Updated dependencies**: Gitleaks updated to latest secure version v8.30.1

## [1.0.0] - 2024-01-15

### Added
- **Acción principal** de GitHub Marketplace (`action.yml`)
- **Escaneo de secretos** con gitleaks configurado para Colombia
- **Análisis SAST** con Semgrep (OWASP Top Ten)
- **Validación automática** de merges basada en severidad
- **Reportes en español** con cumplimiento Ley 1581
- **Configuración personalizable** para diferentes niveles de cumplimiento
- **Notificaciones** por Slack y email
- **Scripts de instalación** automática
- **Git hooks** pre-commit para análisis local
- **Workflows de CI/CD** para testing y publicación

### Features
- **Adaptación colombiana**: Reglas específicas para cédulas, datos personales
- **Zona horaria**: Configuración automática America/Bogota
- **Idioma**: Reportes en español colombiano (es_CO)
- **Cumplimiento**: Secciones específicas para Ley 1581 y SIC
- **Umbrales configurables**: Bloqueo por severidad personalizable
- **Formatos múltiples**: HTML, Markdown, JSON
- **Artifacts**: Reportes disponibles como artifacts de GitHub Actions

### Configuración Incluida
- `.gitleaks.toml` con reglas para contexto colombiano
- `.semgrep.yml` con configuración base
- `.security-pipeline-config.json` para personalización
- `security-report-template.md` plantilla de reportes

### Technical
- **Composite action** con soporte para múltiples inputs/outputs
- **Dependencias Python** para análisis y reportes
- **Tests automatizados** para validación
- **Build con NCC** para distribución eficiente
- **Documentación completa** en español

---

## [0.1.0] - 2024-01-10

### Added
- **Concepto inicial** del pipeline de seguridad
- **Workflow base** de GitHub Actions
- **Scripts Python** para validación y reportes
- **Configuración básica** de gitleaks y semgrep
- **Documentación inicial** en README.md

### Experimental
- **Primera versión** para testing interno
- **Integración básica** con herramientas de seguridad
- **Plantilla de reportes** inicial
- **Ejemplos** de uso y configuración

---

## [Unreleased]

### Planned
- **Integración con SonarQube**
- **Análisis de dependencias** (SCA)
- **Reportes PDF** profesionales
- **Dashboard** web para monitoreo
- **API** para integraciones externas
- **Más reglas** específicas para sectores colombianos
- **Traducciones** a inglés y portugués
- **Plugin para IDEs** (VS Code, IntelliJ)

---

## Notas de Versión

### Versión 1.0.0
Esta es la primera versión estable lista para GitHub Marketplace. Incluye todas las funcionalidades básicas para un pipeline de seguridad completo adaptado al contexto colombiano.

### Versión 0.1.0
Versión experimental para pruebas internas y validación de concepto.

---

## Formatos de Versionamiento

Este proyecto usa [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles en API
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs compatibles

---

## Actualización Automática

Para actualizar a la última versión:

```yaml
# En tu workflow
uses: tu-usuario/security-pipeline-colombia@v1.0.0
```

O usa la versión mayor para actualizaciones automáticas:

```yaml
uses: tu-usuario/security-pipeline-colombia@v1
```

---

## Migraciones

### De versión experimental a 1.0.0
- Actualizar referencia en workflows
- Revisar cambios en inputs/outputs
- Validar configuración personalizada
- Ejecutar tests de integración

---

## Historial de Publicaciones

| Fecha | Versión | Estado | Notas |
|-------|---------|--------|-------|
| 2026-07-20 | 1.0.4 | Stable | Fixed Gitleaks configuration error, updated TOML format |
| 2026-07-20 | 1.0.3 | Stable | Fixed file copy error, improved configuration handling |
| 2026-07-20 | 1.0.2 | Stable | Major fix for Gitleaks installation, multiple download methods, graceful degradation |
| 2026-07-20 | 1.0.1 | Stable | Fixed critical bugs: Gitleaks 404, locale warnings, Node 20 deprecation |
| 2024-01-15 | 1.0.0 | Stable | Primera publicación en Marketplace |
| 2024-01-10 | 0.1.0 | Beta | Versión experimental interna |

---

*Para preguntas sobre versiones específicas, consulta los issues etiquetados con la versión correspondiente.*