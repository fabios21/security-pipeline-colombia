# Design Document

## Introduction

Este documento describe el diseño del pipeline de seguridad automatizado para aplicaciones web en GitHub, adaptado al contexto colombiano. El diseño implementa los requisitos especificados en el documento de requisitos, enfocándose en baja fricción para desarrolladores y cumplimiento de la Ley 1581 de protección de datos.

## Architecture Overview

El pipeline se implementa como un workflow de GitHub Actions compuesto por los siguientes componentes:

1. **Secret Scanner (gitleaks)**: Detecta secretos expuestos en el código
2. **SAST Scanner (Semgrep)**: Analiza vulnerabilidades OWASP Top 10
3. **Validation Gate**: Decide si un merge puede proceder basado en severidad
4. **Report Generator**: Crea reportes en español para stakeholders
5. **Configuration Manager**: Maneja configuraciones optimizadas para Colombia

## Component Design

### 1. Secret Scanner Component

**Implementation**: gitleaks-action en contenedor Docker
**Configuration**: Reglas personalizadas para tipos de secretos comunes en Colombia
**Output**: JSON con detecciones y metadatos

### 2. SAST Scanner Component

**Implementation**: semgrep-action con reglas OWASP Top 10
**Configuration**: Reglas específicas para Java Spring, Node.js, Python Django
**Output**: SARIF formato con severidades y ubicaciones

### 3. Validation Gate Component

**Implementation**: Lógica en bash/Python que analiza resultados
**Decision Matrix**:
- Crítico/High → Bloquear merge
- Medium/Low → Requerir aprobación manual
- Ninguna → Permitir merge automático

### 4. Report Generator Component

**Implementation**: Script Python que procesa JSON/SARIF y genera reporte español
**Output**: PDF/HTML con lenguaje no técnico y secciones de Ley 1581

### 5. Configuration Manager

**Implementation**: Variables de entorno y archivos YAML
**Optimizations**: Caching, ejecución selectiva, timeouts configurables

## Correctness Properties

### Requirement 1: Detección de Secretos Expuestos

**Property 1.1 (File Coverage)**: Para cualquier conjunto de archivos en un repositorio, el Secret Scanner debe procesar todos los archivos con extensión reconocida (.java, .js, .py, .ts, etc.).

**Property 1.2 (Secret Detection)**: Dado un archivo que contiene un patrón conocido de secreto (API key, contraseña, token), el Secret Scanner debe detectarlo y reportarlo con tipo correcto.

**Property 1.3 (Performance Bound)**: Para repositorios con menos de 1000 archivos y tamaño total < 100MB, el escaneo debe completarse en < 60 segundos.

### Requirement 2: Análisis Estático de Vulnerabilidades

**Property 2.1 (OWASP Coverage)**: El SAST Scanner debe detectar al menos una instancia de cada categoría OWASP Top 10 en código de prueba específicamente vulnerable.

**Property 2.2 (Severity Classification)**: Vulnerabilidades con CVSS score ≥ 9.0 deben clasificarse como "críticas", score 7.0-8.9 como "altas", 4.0-6.9 como "medias", < 4.0 como "bajas".

**Property 2.3 (Framework Detection)**: Código que contiene vulnerabilidades específicas de Spring, Node.js o Django debe ser detectado cuando se usan las reglas correspondientes.

### Requirement 3: Validación de Merge Seguro

**Property 3.1 (Critical Block)**: Si el conjunto de vulnerabilidades contiene al menos una con severidad "crítica", el Validation Gate debe bloquear el merge.

**Property 3.2 (High Block)**: Si el conjunto de vulnerabilidades contiene al menos una con severidad "alta", el Validation Gate debe bloquear el merge.

**Property 3.3 (Approval Flow)**: Si el conjunto contiene solo vulnerabilidades "medias" o "bajas", el merge debe requerir aprobación manual antes de proceder.

**Property 3.4 (No Approval Block)**: Si hay vulnerabilidades "medias" o "bajas" y no se obtiene aprobación manual, el merge debe bloquearse.

**Property 3.5 (Block Reason)**: Cuando se bloquea un merge, el output debe incluir lista de vulnerabilidades problemáticas y razón clara del bloqueo.

### Requirement 4: Generación de Reportes en Español

**Property 4.1 (Spanish Output)**: Todos los textos en el reporte generado deben estar en español, incluyendo títulos, descripciones y recomendaciones.

**Property 4.2 (Non-Technical Language)**: Términos técnicos como "SQL injection", "XSS", "CSRF" deben tener explicaciones en lenguaje comprensible para no técnicos.

**Property 4.3 (Ley 1581 Section)**: El reporte debe incluir una sección titulada "Cumplimiento Ley 1581 de Protección de Datos" que explique cómo los hallazgos se relacionan con esta ley.

**Property 4.4 (Colombian Context)**: Las recomendaciones deben incluir referencias al contexto empresarial colombiano (ejemplo: "Según la normativa SIC, se recomienda...").

### Requirement 5: Optimización de Costos y Rendimiento

**Property 5.1 (Trigger Logic)**: El pipeline solo debe ejecutarse en eventos de pull request hacia main/master, no en cada commit individual.

**Property 5.2 (Caching Behavior)**: Ejecuciones consecutivas en el mismo código base deben usar cache cuando sea posible para reducir tiempo de ejecución.

**Property 5.3 (Fallback Configuration)**: Si la configuración optimizada falla, el pipeline debe continuar con configuración estándar sin fallar completamente.

**Property 5.4 (Performance Bound)**: Para repositorios estándar (< 500 archivos, < 50MB), el pipeline completo debe ejecutarse en < 5 minutos.

### Requirement 6: Integración con GitHub Actions

**Property 6.1 (File Structure)**: El workflow debe existir en .github/workflows/security.yml con sintaxis YAML válida.

**Property 6.2 (Trigger Configuration)**: El workflow debe configurarse para ejecutarse en eventos "pull_request" hacia ramas "main" y "master".

**Property 6.3 (Badge Generation)**: El pipeline debe generar un badge de estado que pueda incluirse en README.md con formato [![Security Scan](https://github.com/...)](...)

**Property 6.4 (Colombian Settings)**: La configuración debe incluir zona horaria "America/Bogota" y referencias a regulaciones colombianas.

## Implementation Details

### Workflow Structure

```yaml
name: Security Pipeline Colombia
on:
  pull_request:
    branches: [main, master]
    
jobs:
  secret-scan:
    # Detección de secretos con gitleaks
    
  sast-scan:
    # Análisis estático con Semgrep
    
  validate-gate:
    # Validación de merge seguro
    needs: [secret-scan, sast-scan]
    
  generate-report:
    # Generación de reporte español
    needs: [secret-scan, sast-scan]
    
  security-badge:
    # Generación de badge
    needs: [validate-gate]
```

### Configuration Files

1. **.github/workflows/security.yml** - Workflow principal
2. **.gitleaks.toml** - Configuración de detección de secretos
3. **.semgrep.yml** - Reglas de análisis estático
4. **security-report-template.md** - Plantilla de reporte en español
5. **colombian-compliance.md** - Referencias a Ley 1581 y normativa SIC

### Dependencies

- **gitleaks**: v8.18.0 o superior
- **semgrep**: v1.0.0 o superior  
- **python**: 3.9+ para generación de reportes
- **gh**: CLI de GitHub para interacciones con API

## Testing Strategy

### Property-Based Tests

1. **Secret Scanner Tests**: Generar archivos con/sin secretos y verificar detección
2. **Validation Logic Tests**: Combinaciones de vulnerabilidades y verificaciones de bloqueo
3. **Performance Tests**: Repositorios de diferentes tamaños y mediciones de tiempo

### Example-Based Tests

1. **Framework-Specific Tests**: Código de muestra con vulnerabilidades de Spring, Node.js, Django
2. **Report Generation Tests**: Verificar formato y contenido de reportes en español
3. **Integration Tests**: Flujo completo de PR → Scan → Decision → Report

### Integration Tests

1. **GitHub Actions Simulation**: Ejecución local del workflow con act
2. **API Integration**: Interacción con GitHub API para estados de PR
3. **Badge Service**: Verificación de generación y disponibilidad de badges

## Security Considerations

1. **Secret Handling**: El scanner de secretos debe ejecutarse en modo "read-only" sin riesgo de exponer secretos
2. **Access Control**: Solo permisos necesarios para leer código y actualizar estados de PR
3. **Data Privacy**: Reportes no deben contener código fuente real, solo metadatos y estadísticas
4. **Rate Limiting**: Considerar límites de API de GitHub en ejecuciones frecuentes

## Compliance with Colombian Regulations

### Ley 1581 de Protección de Datos

El diseño incluye:
1. **Detección proactiva** de fugas de datos personales (secretos)
2. **Reportes comprensibles** para responsables de tratamiento de datos
3. **Documentación de controles** de seguridad para auditorías SIC
4. **Recomendaciones específicas** para el contexto normativo colombiano

### Superintendencia de Industria y Comercio (SIC)

1. **Evidencia de due diligence** en seguridad de aplicaciones
2. **Procesos documentados** para gestión de vulnerabilidades
3. **Comunicación clara** de riesgos a stakeholders no técnicos
4. **Adaptación a circular externas** de ciberseguridad

## Performance Optimization

1. **Caching Layer**: Cache de dependencias y resultados intermedios
2. **Selective Execution**: Análisis solo en archivos modificados en PR
3. **Parallel Jobs**: Ejecución concurrente de secret scan y SAST scan
4. **Resource Limits**: Timeouts y memory limits para prevenir costos excesivos

## Monitoring and Maintenance

1. **Execution Logs**: Registro detallado para debugging
2. **Success Metrics**: Tasa de detección, falsos positivos, tiempo de ejecución
3. **Rule Updates**: Proceso para actualizar reglas de gitleaks y semgrep
4. **Compliance Updates**: Adaptación a cambios en normativa colombiana