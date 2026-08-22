c# 🔒 Security Pipeline Colombia - DEMO (No instalar)

> ⚠️ **AVISO CRÍTICO PARA USUARIOS DE GITHUB MARKETPLACE:**
> 
> **El código que GitHub Marketplace muestra abajo está INCOMPLETO y CAUSARÁ ERROR:**
> ```
> - name: Security Pipeline Colombia
> uses: fabios21/security-pipeline-colombia@v1.1.2
> ```
> 
> **❌ Este código solo es UN PASO, no un workflow completo.**
> 
> **✅ PARA INSTALAR CORRECTAMENTE:**
> 1. **NO copies el código del Marketplace**
> 2. **USA el código completo de la sección "INSTALACIÓN CORRECTA" más abajo**
> 3. **O copia el archivo `examples/basic-usage.yml`**

---

> ⚠️ **AVISO IMPORTANTE:** Este es un proyecto DEMO de demostración para fines educativos y de aprendizaje. **NO debe ser instalado en producción** o usado en proyectos reales. Es solo un ejemplo de cómo podría implementarse un pipeline de seguridad para GitHub Actions.

[![Security Pipeline Colombia](https://img.shields.io/badge/DEMO_Solo_para_aprendizaje-red)](https://github.com/marketplace/actions/security-pipeline-colombia)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Compatible-blue)](https://github.com/features/actions)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![Demo Version](https://img.shields.io/badge/Version-DEMO_1.0.0-yellow)](https://github.com/tu-usuario/security-pipeline-colombia/releases)

**DEMO de pipeline de seguridad automatizado para GitHub Actions adaptado al contexto colombiano**, creado para fines educativos y de aprendizaje. Este proyecto muestra cómo podría implementarse un pipeline de seguridad, con enfoque en baja fricción para desarrolladores, cumplimiento de Ley 1581 de protección de datos, y generación de reportes en español para stakeholders no técnicos. **Este es solo un ejemplo y no debe usarse en producción.**

## 🎯 Características Principales

### 🔍 Detección Automatizada
- **Secret Scanner:** Detección de secretos expuestos (API keys, contraseñas) usando `gitleaks`
- **SAST Scanner:** Análisis estático de código para vulnerabilidades OWASP Top 10 usando `Semgrep`
- **Validación Inteligente:** Bloqueo automático de merges con vulnerabilidades críticas/altas

### 📄 Reportes en Español
- **Para no técnicos:** Lenguaje claro y comprensible para gerentes y personal administrativo
- **Cumplimiento normativo:** Secciones específicas sobre Ley 1581 y regulaciones SIC
- **Múltiples formatos:** HTML, PDF y Markdown disponibles

### 🇨🇴 Adaptación Local
- **Contexto colombiano:** Reglas personalizadas para servicios financieros locales
- **Zona horaria:** Configuración `America/Bogota`
- **Normativas:** Referencias a legislación colombiana aplicable

### 💰 Optimización de Costos
- **Totalmente gratuito** para PoC (prueba de concepto)
- **Ejecución selectiva:** Solo en PRs hacia ramas principales
- **Caching inteligente:** Reduce tiempo de ejecución y consumo de recursos

## �️ INSTALACIÓN CORRECTA (DEMO educativo)

> ⚠️ **NO uses el código que GitHub Marketplace muestra arriba. Está incompleto.**

### ✅ **Código CORRECTO - Copia TODO esto:**

**Archivo:** `.github/workflows/security.yml`

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
        fetch-depth: 0
        
    - name: Run Security Pipeline Colombia (DEMO)
      id: security
      uses: fabios21/security-pipeline-colombia@v1.1.2
      with:
        compliance-level: 'standard'
        timezone: 'America/Bogota'
        report-language: 'es_CO'
        block-on-secrets: true
        block-on-critical: true
        block-on-high: true
        require-approval-on-medium: true
        
    - name: Upload security reports
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: security-reports
        path: |
          gitleaks-report.json
          semgrep-results.sarif
          validation-result.json
          visual-report.txt
          security-report-*.html
          security-report.*.md
        retention-days: 7
```

### 📋 **Pasos de instalación:**

1. **Crear directorio:** `mkdir -p .github/workflows`
2. **Crear archivo:** `.github/workflows/security.yml`
3. **Copiar TODO el código YAML de arriba**
4. **Commit y push**

**¿Error "A sequence was not expected"?** → Usaste el código incompleto del Marketplace.

## �🚀 INFORMACIÓN DE DEMO - No instalar

> 🚫 **ESTE ES UN PROYECTO DEMO - NO INSTALAR**
>
> **⚠️ Advertencia importante:** Este proyecto fue creado exclusivamente para fines educativos y de aprendizaje. No es una herramienta real disponible en GitHub Marketplace y **no debe ser instalado o usado en producción**.

## 🛠️ ADVERTENCIA CRÍTICA SOBRE INSTALACIÓN

> ⚠️ **PROBLEMA CONOCIDO:** El código de instalación que GitHub Marketplace muestra automáticamente está **INCOMPLETO** y **CAUSA ERRORES**.
>
> GitHub Marketplace genera automáticamente este snippet **INCORRECTO**:
> ```yaml
> - name: Security Pipeline Colombia
> uses: fabios21/security-pipeline-colombia@v1.1.0
> with:
>   # Parámetros...
> ```
>
> **¿POR QUÉ FALLA?**
> 1. ❌ **Falta la estructura completa** del workflow
> 2. ❌ **Comienza con `- name:`** en lugar de `name:` 
> 3. ❌ **No incluye el step de checkout**
> 4. ❌ **No tiene triggers (`on:`)** ni estructura `jobs:`
> 5. ❌ **Causa error:** "A sequence was not expected (Line: 1, Col: 1)"

### ✅ **CÓDIGO CORRECTO PARA APRENDIZAJE:**
Si quieres aprender cómo se usa correctamente (solo para fines educativos):

```yaml
name: 🔒 Security Pipeline Colombia - DEMO (Solo aprendizaje)

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
        fetch-depth: 0
        
    - name: Run Security Pipeline Colombia (DEMO)
      id: security
      uses: fabios21/security-pipeline-colombia@v1.1.0
      with:
        compliance-level: 'standard'
        timezone: 'America/Bogota'
        report-language: 'es_CO'
        block-on-secrets: true
        block-on-critical: true
        block-on-high: true
        require-approval-on-medium: true
```

> **⚠️ RECUERDA:** Este es solo un DEMO para aprendizaje. **NO lo instales en repositorios reales**.

### Objetivos educativos de este demo:
> 1. **Aprender sobre pipelines de seguridad** en GitHub Actions
> 2. **Entender cómo funcionan** las herramientas SAST y secret scanning
> 3. **Ver ejemplos** de configuración de `.gitleaks.toml` y `.semgrep.yml`
> 4. **Estudiar cómo generar reportes** de seguridad automatizados
> 5. **Analizar la estructura** de un GitHub Action complejo
>
> ### 🎓 Uso recomendado para estudiantes:
> 1. **Explorar el código fuente** para entender la arquitectura
> 2. **Revisar los scripts de Python** para aprender sobre automatización
> 3. **Estudiar los workflows de GitHub Actions** como ejemplos educativos
> 4. **Adaptar conceptos** a tus propios proyectos de aprendizaje
> 5. **No ejecutar** en entornos de producción
>
> **📚 Este demo forma parte de un proyecto educativo del SENA (Servicio Nacional de Aprendizaje)**

## 📁 Estructura del Proyecto

```
.github/
├── workflows/
│   └── security.yml          # Workflow principal de GitHub Actions
└── scripts/
    ├── validate_security.py  # Validador de decisiones de merge
    └── generate_report.py    # Generador de reportes en español

.gitleaks.toml                # Configuración de detección de secretos
security-report-template.md   # Plantilla de reportes
README.md                     # Esta documentación
```

## ⚙️ Configuración

### Configuración de Contactos (Opcional)
Para personalizar los contactos que aparecen en los reportes de seguridad:

```yaml
- name: Security Pipeline Colombia
  uses: fabios21/security-pipeline-colombia@main
  with:
    # Contactos personalizados (opcional)
    security-contact: 'security@tu-empresa.com'
    dev-team-contact: 'devops@tu-empresa.com'
    email-notifications: 'security@tu-empresa.com,lead@tu-empresa.com'
    
    # Otras configuraciones
    compliance-level: 'standard'
    block-on-secrets: true
```

Si no configuras contactos específicos, se usarán valores genéricos que referencian la configuración del repositorio.

### Archivo `.gitleaks.toml`
Configuración personalizada para contexto colombiano:
- Detección de API keys de servicios bancarios (PSE, ACH)
- Reglas para cédulas de ciudadanía y datos personales
- Exclusiones para falsos positivos comunes

### Variables de Entorno
```yaml
# Configuración automática en el workflow
TIMEZONE: America/Bogota
LANG: es_CO.UTF-8
LC_ALL: es_CO.UTF-8
```

## 🔧 Uso

### Flujo de Trabajo Automático
1. **Crear Pull Request** hacia `main` o `master`
2. **Ejecución automática** del pipeline de seguridad
3. **Validación en tiempo real** de secretos y vulnerabilidades
4. **Generación de reportes** en español
5. **Decisión automática** de merge (bloqueo/aprobación)

### Estados Posibles del Pipeline
- ✅ **PASÓ:** No se detectaron problemas críticos
- ⚠️ **APROBACIÓN REQUERIDA:** Vulnerabilidades medias/bajas detectadas
- ❌ **FALLÓ:** Secretos expuestos o vulnerabilidades críticas/altas

### 📍 Acceso a Reportes Generados

#### 📁 **Dónde se guardan los reportes:**
Los reportes se generan durante la ejecución del pipeline y se guardan como **artifacts** en GitHub Actions:

1. **Durante la ejecución:** Se crean archivos temporales en el runner
2. **Como artifacts:** Se suben al final del workflow para su descarga
3. **En la consola:** Se muestran visualmente durante la ejecución

#### 📊 **Archivos generados:**
- `gitleaks-report.json` → Resultados del escaneo de secretos
- `semgrep-results.sarif` → Resultados del análisis SAST
- `validation-result.json` → Resultado final de validación
- `visual-report.txt` → 📱 **NUEVO**: Reporte visual con emojis y gráficos
- `security-report-es_CO.html` → Reporte HTML en español
- `security-report-es_CO.md` → Reporte Markdown en español

#### 📥 **Cómo acceder a los reportes:**
1. **Navegar** a la ejecución del workflow en GitHub Actions
2. **Hacer clic** en "Artifacts" (al final de la ejecución)
3. **Descargar** el artifact llamado `security-artifacts`
4. **Extraer** los archivos para revisar todos los reportes

#### 👁️ **Visualización en tiempo real:**
Durante la ejecución, puedes ver:
- ✅ Resumen visual con emojis en la consola
- 🔴 Alertas críticas con indicadores de color
- 📈 Barras de progreso para vulnerabilidades
- 🏛️ Secciones específicas sobre cumplimiento Ley 1581

#### 📚 **Documentación completa:**
Para información detallada sobre todos los reportes generados, consulta:
[📍 REPORTES_GENERADOS.md](REPORTES_GENERADOS.md) - Guía completa sobre dónde quedan y cómo acceder a los reportes

## 📊 Ejemplo de Reporte

### Secciones del Reporte HTML
```html
1. 📋 Resumen Ejecutivo
2. 📊 Resumen de Hallazgos
3. 🏛️ Cumplimiento Ley 1581
4. 🎯 Recomendaciones para Colombia
5. 📈 Evaluación de Riesgo
```

### Ejemplo de Salida en PR
```markdown
## 🔒 Resultado del Análisis de Seguridad

**Estado:** REQUIERE APROBACIÓN

### 🚨 Secretos Detectados
- API_KEY_PSE en config/database.yml:45

### ⚠️ Vulnerabilidades Detectadas
#### MEDIUM
- SQL_INJECTION en app/controllers/users_controller.rb:23

⚠️ **Se requiere aprobación manual.**
Se detectaron vulnerabilidades de nivel medio o bajo.

---
*Pipeline ejecutado en zona horaria America/Bogota*
```

## 🏛️ Cumplimiento Normativo

### Ley 1581 de Protección de Datos
El pipeline incluye análisis específico para:
- **Detección de datos personales** expuestos
- **Evaluación de controles** de seguridad
- **Recomendaciones** para cumplimiento SIC

### Beneficios para Auditorías
- **Evidencia documentada** de due diligence en seguridad
- **Procesos automatizados** para gestión de vulnerabilidades
- **Reportes comprensibles** para stakeholders no técnicos

## 💡 Mejores Prácticas

### Para Desarrolladores
1. **Verificar antes de commit:** Usar hooks pre-commit con las mismas reglas
2. **Gestionar secretos:** Usar variables de entorno o gestores de secretos
3. **Revisar reportes:** Corregir vulnerabilidades antes de solicitar revisión

### Para Líderes Técnicos
1. **Monitorizar métricas:** Tasa de detección, tiempo de remediación
2. **Actualizar reglas:** Mantener configuraciones actualizadas con normativas
3. **Capacitar equipos:** Concientización en seguridad y protección de datos

### Para Gerentes/Administrativos
1. **Revisar reportes trimestrales:** Evaluar estado de cumplimiento
2. **Asignar recursos:** Para corrección de vulnerabilidades críticas
3. **Documentar decisiones:** Para evidenciar gestión de riesgos

## 🔍 Personalización Avanzada

### Agregar Reglas Personalizadas
```toml
# En .gitleaks.toml
[[rules]]
description = "Token de servicio colombiano específico"
id = "mi-servicio-token"
regex = '''mi-servicio-[_-]?token[_-]?[0-9a-f]{32}'''
tags = ["api-key", "colombia", "custom"]
```

### Modificar Umbrales de Validación
```python
# En .github/scripts/validate_security.py
# Ajustar niveles de severidad
CRITICAL_THRESHOLD = 9.0  # CVSS score
HIGH_THRESHOLD = 7.0
```

### Extender Generación de Reportes
```python
# En .github/scripts/generate_report.py
# Agregar nuevas secciones al reporte
def generate_custom_section(self):
    return {
        "titulo": "Sección Personalizada",
        "contenido": "Información adicional..."
    }
```

## 🐛 Solución de Problemas

### Problemas Comunes

| Problema | Solución |
|----------|----------|
| Workflow no se ejecuta | Verificar triggers en `security.yml` |
| Falsos positivos en secretos | Agregar exclusiones en `.gitleaks.toml` |
| Tiempo de ejecución excesivo | Ajustar `timeout-minutes` o usar caching |
| Reportes no generados | Verificar permisos de escritura de artifacts |

### Logs y Depuración
```bash
# Ver logs completos del workflow
# En GitHub: Actions → Security Pipeline → job → View workflow run

# Probar componentes individualmente
python .github/scripts/validate_security.py --secrets test.json --sast test.sarif
```

## 📈 Métricas y Monitoreo

### KPIs Recomendados
1. **Tiempo medio de remediación:** Objetivo < 7 días para críticas
2. **Tasa de falsos positivos:** Objetivo < 10%
3. **Cobertura de análisis:** Objetivo 100% de PRs analizados
4. **Cumplimiento normativo:** Objetivo 100% de reportes generados

### Dashboard Sugerido
- **Gráfico 1:** Vulnerabilidades por severidad (histórico)
- **Gráfico 2:** Tiempo de remediación por categoría
- **Gráfico 3:** Cumplimiento de plazos normativos
- **Tabla:** Top 10 vulnerabilidades más comunes

## 🤝 Contribución

### Cómo Contribuir
1. Fork el proyecto
2. Crear branch de feature (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -m 'Agrega mejora X'`)
4. Push al branch (`git push origin feature/mejora`)
5. Abrir Pull Request

### Estándares de Código
- **Python:** PEP 8, type hints, docstrings
- **YAML:** indentación de 2 espacios, comentarios en español
- **Documentación:** Markdown con ejemplos prácticos

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License** - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte y Contacto

### Canales de Soporte
- **Email:** Configurar en el workflow (ver sección de configuración)
- **GitHub Issues:** Para reportar bugs o solicitar features  
- **GitHub Discussions:** Para preguntas y mejores prácticas

### Mantenimiento
- **Actualizaciones de seguridad:** Mensuales
- **Actualizaciones de normativa:** Según cambios en legislación colombiana
- **Soporte activo:** Lunes a Viernes 8am-6pm (hora Colombia)

---

## 🎖️ Reconocimientos

- **GitHub Actions** por la plataforma de CI/CD
- **gitleaks** y **Semgrep** por las herramientas de análisis
- **Comunidad DevSecOps Colombia** por las mejores prácticas locales
- **Superintendencia de Industria y Comercio (SIC)** por el marco normativo

---

**¿Listo para mejorar la seguridad de tus aplicaciones?** 🚀

[![Security Pipeline Colombia](https://img.shields.io/badge/Empezar_Ahora-Configurar_Pipeline-blue?style=for-the-badge)](https://github.com/tu-usuario/tu-repo/actions/workflows/security.yml)

*"La seguridad no es un producto, es un proceso" - Bruce Schneier*


## 📦 PROYECTO DEMO EDUCATIVO

> 🚫 **NO DISPONIBLE EN MARKETPLACE - PROYECTO DE APRENDIZAJE**

### 🎯 Propósito Educativo de este Demo:
Este proyecto fue creado como **material de aprendizaje** para estudiantes de desarrollo de software y seguridad informática. Su objetivo es:

1. **Mostrar cómo se estructura** un pipeline de seguridad en GitHub Actions
2. **Proporcionar ejemplos reales** de configuración de herramientas SAST y secret scanning
3. **Enseñar mejores prácticas** de DevSecOps adaptadas al contexto colombiano
4. **Servir como referencia** para proyectos educativos y de investigación

### 🔍 Qué puedes aprender de este demo:
- **GitHub Actions**: Cómo crear workflows complejos
- **SAST**: Configuración de Semgrep para análisis estático de código
- **Secret Scanning**: Uso de gitleaks con reglas personalizadas
- **Generación de reportes**: Creación de reportes automatizados en español
- **Automatización**: Scripts en Python para validación y generación de reportes

### 📚 Cómo usar este demo para aprender:
1. **Explora el código fuente** para entender la arquitectura
2. **Estudia los workflows** en `.github/workflows/`
3. **Analiza los scripts de Python** en `.github/scripts/`
4. **Examina las configuraciones** de seguridad (`.gitleaks.toml`, `.semgrep.yml`)
5. **Adapta conceptos** a tus propios proyectos de aprendizaje

### ⚠️ Advertencias importantes:
- **No instalar**: Este demo no está disponible en GitHub Marketplace
- **No usar en producción**: No está diseñado para uso real
- **Solo para aprendizaje**: Su propósito es exclusivamente educativo
- **Proyecto SENA**: Desarrollado como parte de actividades de aprendizaje del Servicio Nacional de Aprendizaje

---

## 🏫 Contexto Educativo

### Institución:
- **SENA** - Servicio Nacional de Aprendizaje de Colombia

### Objetivos de Aprendizaje:
- Entender pipelines de seguridad en entornos CI/CD
- Aprender sobre herramientas SAST y secret scanning
- Desarrollar habilidades en automatización de seguridad
- Aplicar conceptos de DevSecOps en contextos reales

### Herramientas Utilizadas (con fines educativos):
- **GitHub Actions** - Para aprendizaje de CI/CD
- **gitleaks** - Para entender detección de secretos
- **Semgrep** - Para aprender análisis estático de código
- **Python** - Para desarrollar scripts de automatización

---

## 🎓 Recursos para Estudiantes

### Para continuar tu aprendizaje:
1. **Documentación oficial** de las herramientas:
   - [GitHub Actions Documentation](https://docs.github.com/en/actions)
   - [Semgrep Documentation](https://semgrep.dev/docs/)
   - [gitleaks Documentation](https://github.com/gitleaks/gitleaks)

2. **Cursos recomendados**:
   - DevSecOps Fundamentals
   - GitHub Actions for CI/CD
   - Application Security Testing

3. **Comunidades**:
   - Comunidad DevSecOps Colombia
   - GitHub Community
   - Foros de seguridad informática

---

**🎯 Este demo es parte de un esfuerzo educativo para formar desarrolladores con habilidades en seguridad** 🇨🇴🔒

*"La educación es el arma más poderosa que puedes usar para cambiar el mundo" - Nelson Mandela*