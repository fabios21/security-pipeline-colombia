# 🔒 Security Pipeline Colombia - GitHub Action

[![Security Pipeline Colombia](https://img.shields.io/badge/GitHub_Marketplace-Security_Pipeline_Colombia-blue)](https://github.com/marketplace/actions/security-pipeline-colombia)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Compatible-blue)](https://github.com/features/actions)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![Release](https://img.shields.io/github/v/release/tu-usuario/security-pipeline-colombia)](https://github.com/tu-usuario/security-pipeline-colombia/releases)

**Pipeline de seguridad automatizado para GitHub Actions adaptado al contexto colombiano**, disponible en GitHub Marketplace. Con enfoque en baja fricción para desarrolladores, cumplimiento de Ley 1581 de protección de datos, y generación de reportes en español para stakeholders no técnicos.

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

## 🚀 Instalación desde GitHub Marketplace

### Opción 1: Instalación con un clic (Recomendado)
1. Visita [GitHub Marketplace - Security Pipeline Colombia](https://github.com/marketplace/actions/security-pipeline-colombia)
2. Haz clic en **"Install"**
3. Selecciona los repositorios donde quieres usar la acción
4. ¡Listo! Ya puedes usar la acción en tus workflows

### Opción 2: Uso manual en workflow
```yaml
- name: Security Pipeline Colombia
  uses: tu-usuario/security-pipeline-colombia@v1.0.4
  with:
    compliance-level: 'ley_1581'
    report-language: 'es_CO'
    block-on-secrets: true
    block-on-critical: true
```

### Opción 3: Instalación avanzada
Para configuraciones personalizadas o instalación en múltiples repositorios, usa nuestro script de instalación:
```bash
# Usar script de instalación automática
curl -s https://raw.githubusercontent.com/tu-usuario/security-pipeline-colombia/main/setup_auto.py | python3
```

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
- **Issues de GitHub:** Para reportar bugs o solicitar features
- **Discusiones:** Para preguntas y mejores prácticas
- **Email:** seguridad@empresa.co (configurar según organización)

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


## 📦 Publicación en GitHub Marketplace

### Para Usuarios:
- **Instalación fácil**: Un clic desde Marketplace
- **Actualizaciones automáticas**: Siempre tienes la última versión
- **Soporte centralizado**: Issues y documentación en un solo lugar
- **Confianza**: Acciones verificadas por GitHub

### Para Desarrolladores:
Para contribuir o publicar nuevas versiones:

1. **Crear release**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Publicar en Marketplace**:
   - Ir a Releases en GitHub
   - Click "Edit" en el release
   - Marcar "Publish this Action to GitHub Marketplace"
   - Completar formulario requerido

3. **Mantener actualizado**:
   - Actualizar CHANGELOG.md
   - Incrementar versión en package.json
   - Ejecutar tests antes de publicar

### Requisitos del Marketplace:
- ✅ Licencia MIT
- ✅ README completo
- ✅ Action.yml correctamente configurado
- ✅ Releases versionados
- ✅ Tests automatizados
- ✅ Documentación clara

---

## 🏪 Disponible en GitHub Marketplace

[![Instalar desde GitHub Marketplace](https://img.shields.io/badge/Instalar_desde_Marketplace-Instalar_ahora-blue?style=for-the-badge&logo=github)](https://github.com/marketplace/actions/security-pipeline-colombia)

**Beneficios de usar la versión de Marketplace:**
- ✅ Instalación con un clic
- ✅ Actualizaciones automáticas
- ✅ Soporte garantizado
- ✅ Integración nativa con GitHub Actions
- ✅ Mayor visibilidad y adopción

---

## 📞 Soporte y Comunidad

### Canales Oficiales:
- **Marketplace**: [GitHub Marketplace Listing](https://github.com/marketplace/actions/security-pipeline-colombia)
- **Documentación**: [README Completo](README.md)
- **Issues**: [Reportar Bugs](https://github.com/tu-usuario/security-pipeline-colombia/issues)
- **Discusiones**: [Preguntas y Ayuda](https://github.com/tu-usuario/security-pipeline-colombia/discussions)

### Para Empresas:
- **Soporte empresarial**: Disponible para organizaciones
- **Customización**: Adaptaciones específicas para tu empresa
- **Capacitación**: Entrenamiento en seguridad DevSecOps
- **Consultoría**: Implementación y optimización

---

## 🎖️ Reconocimientos y Partners

### Herramientas Utilizadas:
- **GitHub Actions** - Plataforma de CI/CD
- **gitleaks** - Detección de secretos
- **Semgrep** - Análisis estático de código
- **Python** - Scripts y automatización

### Partners Institucionales:
- **SENA** - Servicio Nacional de Aprendizaje
- **Comunidad DevSecOps Colombia**
- **Superintendencia de Industria y Comercio (SIC)**

### Colaboradores:
Agradecemos a todos los colaboradores que han hecho posible este proyecto. ¡Tu contribución es valiosa!

[![Contribuidores](https://contrib.rocks/image?repo=tu-usuario/security-pipeline-colombia)](https://github.com/tu-usuario/security-pipeline-colombia/graphs/contributors)

---

**¿Listo para mejorar la seguridad de tus aplicaciones con un clic?** 🚀

[![Instalar Ahora](https://img.shields.io/badge/Instalar_Ahora-GitHub_Marketplace-6e40c9?style=for-the-badge&logo=github)](https://github.com/marketplace/actions/security-pipeline-colombia)

*"La seguridad en el desarrollo de software no es un lujo, es una necesidad" - Adaptado para Colombia* 🇨🇴🔒