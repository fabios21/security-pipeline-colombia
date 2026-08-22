# 🚨 PROBLEMA CONOCIDO: Instalación desde GitHub Marketplace

## 📋 Descripción del Problema

**GitHub Marketplace muestra automáticamente un snippet de instalación INCOMPLETO** que causa el error:

```
Check failure on line 1 in .github/workflows/main.yml
GitHub Actions/ .github/workflows/main.yml
Invalid workflow file
(Line: 1, Col: 1): A sequence was not expected
```

## 🔍 Código Problemático (Automáticamente Generado)

GitHub Marketplace genera esto:

```yaml
- name: Security Pipeline Colombia
uses: fabios21/security-pipeline-colombia@v1.1.0
with:
  # Modo de escaneo de secretos: full-history, pr-only, commit-only
  scan-mode: # optional, default is pr-only
  # Ruta al archivo de configuración personalizado de gitleaks (.gitleaks.toml)
  config-path: # optional, default is .gitleaks.toml
  # Configuración de Semgrep a utilizar (p/owasp-top-ten, p/ci, p/security-audit, etc.)
  semgrep-config: # optional, default is p/owasp-top-ten
  # Nivel de cumplimiento de seguridad
  compliance-level: # optional, default is standard
  # Zona horaria para reportes
  timezone: # optional, default is America/Bogota
  # Idioma de los reportes generados
  report-language: # optional, default is es_CO
  # Formatos de reporte a generar
  report-formats: # optional, default is html,markdown
  # Bloquear merge si se detectan secretos expuestos
  block-on-secrets: # optional, default is true
  # Bloquear merge si se detectan vulnerabilidades críticas (CVSS >= 9.0)
  block-on-critical: # optional, default is true
  # Bloquear merge si se detectan vulnerabilidades altas (CVSS >= 7.0)
  block-on-high: # optional, default is true
  # Requerir aprobación manual si se detectan vulnerabilidades medias (CVSS >= 4.0)
  require-approval-on-medium: # optional, default is true
  # URL de webhook de Slack para notificaciones (opcional)
  slack-webhook: # optional, default is 
  # Lista de emails para notificaciones (separados por coma)
  email-notifications: # optional, default is 
  # Email del responsable de seguridad
  security-contact: # optional, default is 
  # Email del equipo de desarrollo
  dev-team-contact: # optional, default is 
```

## ❌ ¿Por qué falla?

Este código NO FUNCIONA porque:

1. **Comienza con `- name:`** - En YAML, esto indica una secuencia/lista
2. **GitHub Actions espera un documento YAML completo** que empiece con `name:` (sin guión)
3. **Falta la estructura completa** del workflow:
   - `name:` (nombre del workflow)
   - `on:` (triggers)
   - `jobs:` (definición de trabajos)
   - `steps:` con checkout y otros pasos necesarios

## ✅ Solución: Código Correcto

### Para fines educativos (DEMO):

```yaml
name: 🔒 Security Pipeline Colombia - DEMO

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]

jobs:
  security-scan:
    name: 🛡️ Security Analysis
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Necesario para análisis de secretos
        
    - name: Run Security Pipeline Colombia (DEMO)
      id: security
      uses: fabios21/security-pipeline-colombia@v1.1.0
      with:
        # Modo de escaneo de secretos: full-history, pr-only, commit-only
        scan-mode: pr-only  # optional, default is pr-only
        
        # Ruta al archivo de configuración personalizada de gitleaks (.gitleaks.toml)
        config-path: .gitleaks.toml  # optional, default is .gitleaks.toml
        
        # Configuración de Semgrep a utilizar
        semgrep-config: p/owasp-top-ten  # optional, default is p/owasp-top-ten
        
        # Nivel de cumplimiento de seguridad
        compliance-level: standard  # optional, default is standard
        
        # Zona horaria para reportes
        timezone: America/Bogota  # optional, default is America/Bogota
        
        # Idioma de los reportes generados
        report-language: es_CO  # optional, default is es_CO
        
        # Formatos de reporte a generar
        report-formats: html,markdown  # optional, default is html,markdown
        
        # Bloquear merge si se detectan secretos expuestos
        block-on-secrets: true  # optional, default is true
        
        # Bloquear merge si se detectan vulnerabilidades críticas (CVSS >= 9.0)
        block-on-critical: true  # optional, default is true
        
        # Bloquear merge si se detectan vulnerabilidades altas (CVSS >= 7.0)
        block-on-high: true  # optional, default is true
        
        # Requerir aprobación manual si se detectan vulnerabilidades medias (CVSS >= 4.0)
        require-approval-on-medium: true  # optional, default is true
```

## 📁 Estructura Correcta

### 1. Crear archivo workflow:
```
.github/workflows/security.yml
```

### 2. Contenido mínimo requerido:
```yaml
name: Nombre del Workflow        # ✅ Sin guión (-)
on:                              # ✅ Triggers
  pull_request:
jobs:                            # ✅ Trabajos
  job-name:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout             # ✅ Con guión (-) dentro de steps
      uses: actions/checkout@v4
      
    - name: Usar Acción          # ✅ Otro step con guión (-)
      uses: usuario/accion@version
```

## 🔧 Solución Técnica en la Fuente

### ¿Por qué GitHub Marketplace genera código incorrecto?

1. **Generación automática:** GitHub lee el archivo `action.yml` y genera un snippet automático
2. **Solo muestra el "step":** Muestra solo la parte `uses:` de la acción
3. **No incluye contexto:** No incluye el workflow completo necesario

### ¿Cómo corregirlo permanentemente?

**No se puede desactivar** la generación automática de GitHub Marketplace.

**Soluciones disponibles:**

1. **Documentación clara:** Incluir advertencias en el README
2. **Ejemplos completos:** Proporcionar workflows completos en `examples/`
3. **Instrucciones paso a paso:** Guiar a los usuarios para crear workflows correctos

## 📝 Recomendaciones para Futuras Versiones

### En el archivo README.md:
```markdown
## ⚠️ ADVERTENCIA DE INSTALACIÓN

El código que GitHub Marketplace muestra está INCOMPLETO. 
**NO COPIES Y PEGUES DIRECTAMENTE.**

En su lugar:
1. **Usa el ejemplo completo** de `examples/basic-usage.yml`
2. **Sigue las instrucciones** en esta sección
3. **Verifica** que tu archivo YAML comience con `name:` (sin guión)
```

### En la descripción de la acción:
```yaml
# action.yml
name: 'Security Pipeline Colombia'
description: '🔒 Pipeline de seguridad... ⚠️ IMPORTANTE: NO uses el snippet del marketplace directamente. Ve a examples/ para workflow completo.'
```

## 🎯 Resumen

1. **PROBLEMA:** GitHub Marketplace genera snippet incompleto
2. **CAUSA:** Muestra solo el "step" sin estructura de workflow
3. **SOLUCIÓN:** Usar ejemplos completos de `examples/` directory
4. **PREVENCIÓN:** Documentar claramente en README.md
5. **EDUCACIÓN:** Enseñar estructura correcta de GitHub Actions workflows

---

**✅ Esta documentación debe incluirse en futuras versiones para prevenir errores de instalación.**