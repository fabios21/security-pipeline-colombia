# Changelog

Todos los cambios notables en Security Pipeline Colombia serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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