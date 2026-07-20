# 📋 Plantilla de Reporte de Seguridad - Colombia

## Información del Proyecto
**Nombre del Proyecto:** `{{project_name}}`  
**Repositorio:** `{{repository_url}}`  
**Fecha del Análisis:** `{{analysis_date}}`  
**Responsable de Seguridad:** `{{security_lead}}`  

## 🎯 Objetivo del Reporte
Este documento presenta los resultados del análisis de seguridad automatizado realizado como parte del pipeline de desarrollo continuo. El objetivo es identificar riesgos de seguridad, evaluar el cumplimiento de la Ley 1581 de Protección de Datos, y proporcionar recomendaciones específicas para el contexto empresarial colombiano.

## 📊 Metodología de Análisis

### Herramientas Utilizadas
1. **gitleaks** - Detección de secretos expuestos
2. **Semgrep** - Análisis estático de código (SAST)
3. **Scripts personalizados** - Validación y generación de reportes

### Alcance del Análisis
- ✅ Código fuente de la aplicación
- ✅ Configuraciones y archivos de entorno
- ✅ Dependencias y librerías
- ❌ Infraestructura y despliegue (fuera de alcance)

## 🔍 Hallazgos por Categoría

### 1. Secretos Expuestos
**Estado:** `{{secrets_status}}`

**Hallazgos:**
{{#secrets_findings}}
- **{{rule}}** en `{{file}}:{{line}}`
  - Tipo: {{type}}
  - Riesgo: {{risk_level}}
{{/secrets_findings}}

{{^secrets_findings}}
✅ No se detectaron secretos expuestos
{{/secrets_findings}}

### 2. Vulnerabilidades de Seguridad
**Estado:** `{{vulnerabilities_status}}`

**Resumen por Severidad:**
- Críticas: `{{critical_count}}`
- Altas: `{{high_count}}`
- Medias: `{{medium_count}}`
- Bajas: `{{low_count}}`

**Detalles:**
{{#vulnerability_findings}}
#### {{severity_emoji}} {{severity}} - {{rule}}
- **Archivo:** `{{file}}:{{line}}`
- **Descripción:** {{description}}
- **Recomendación:** {{recommendation}}
- **Categoría OWASP:** {{owasp_category}}
{{/vulnerability_findings}}

{{^vulnerability_findings}}
✅ No se detectaron vulnerabilidades
{{/vulnerability_findings}}

## 🏛️ Análisis de Cumplimiento Normativo

### Ley 1581 de Protección de Datos
**Estado de Cumplimiento:** `{{ley_1581_status}}`

**Evaluación:**
1. **Principio de Seguridad:** `{{security_principle_status}}`
2. **Confidencialidad de Datos:** `{{confidentiality_status}}`
3. **Notificación de Incidentes:** `{{incident_notification_status}}`

**Hallazgos Específicos:**
{{#ley_1581_findings}}
- {{finding}}
{{/ley_1581_findings}}

**Obligaciones Identificadas:**
{{#ley_1581_obligations}}
- {{obligation}}
{{/ley_1581_obligations}}

### Superintendencia de Industria y Comercio (SIC)
**Consideraciones:**
{{#sic_considerations}}
- {{consideration}}
{{/sic_considerations}}

## 📈 Evaluación de Riesgo Empresarial

### Impacto Potencial
**Nivel de Riesgo:** `{{business_risk_level}}`

**Áreas Afectadas:**
- Reputación corporativa: `{{reputation_impact}}`
- Continuidad del negocio: `{{business_continuity_impact}}`
- Responsabilidad legal: `{{legal_liability_impact}}`
- Costos financieros: `{{financial_cost_impact}}`

### Factores del Contexto Colombiano
1. **Marco regulatorio:** Ley 1581, Circular Externa SIC
2. **Expectativas del mercado:** Estándares de seguridad en servicios financieros
3. **Capacidad organizacional:** Recursos disponibles para gestión de seguridad

## 🎯 Plan de Acción Recomendado

### Acciones Inmediatas (0-7 días)
{{#immediate_actions}}
1. **{{title}}**
   - Responsable: {{owner}}
   - Plazo: {{deadline}}
   - Recursos: {{resources}}
{{/immediate_actions}}

### Acciones a Mediano Plazo (8-30 días)
{{#medium_term_actions}}
1. **{{title}}**
   - Objetivo: {{objective}}
   - Indicador de éxito: {{success_indicator}}
{{/medium_term_actions}}

### Acciones Estratégicas (31-90 días)
{{#strategic_actions}}
1. **{{title}}**
   - Impacto esperado: {{expected_impact}}
   - Inversión requerida: {{required_investment}}
{{/strategic_actions}}

## 📋 Métricas de Seguridad

### Indicadores Clave (KPIs)
1. **Tasa de detección de secretos:** `{{secrets_detection_rate}}%`
2. **Tiempo medio de remediación:** `{{mean_remediation_time}} días`
3. **Cumplimiento de plazos normativos:** `{{regulatory_compliance_rate}}%`
4. **Inversión en seguridad vs. riesgo:** `{{security_investment_ratio}}`

### Tendencias y Análisis Histórico
{{#historical_analysis}}
- **Período:** {{period}}
- **Mejoras observadas:** {{improvements}}
- **Áreas de oportunidad:** {{opportunity_areas}}
{{/historical_analysis}}

## 🤝 Responsabilidades y Gobernanza

### Comité de Seguridad
- **Presidente:** {{security_committee_chair}}
- **Miembros:** {{security_committee_members}}
- **Frecuencia de reuniones:** {{meeting_frequency}}

### Canales de Comunicación
1. **Reportes técnicos:** {{technical_reports_channel}}
2. **Alertas de seguridad:** {{security_alerts_channel}}
3. **Consultas legales:** {{legal_queries_channel}}
4. **Comunicación a stakeholders:** {{stakeholders_communication_channel}}

## 📎 Anexos

### A. Glosario de Términos
- **SAST:** Análisis Estático de Seguridad de Aplicaciones
- **Secretos:** Credenciales, tokens, claves expuestas en código
- **Ley 1581:** Ley colombiana de protección de datos personales
- **SIC:** Superintendencia de Industria y Comercio de Colombia

### B. Referencias Normativas
1. Ley 1581 de 2012 - Protección de datos personales
2. Circular Externa 002 de 2021 - Ciberseguridad SIC
3. Estándar ISO/IEC 27001 - Sistemas de gestión de seguridad de la información

### C. Contactos de Emergencia
- **Equipo de seguridad:** {{security_team_contact}}
- **Asesor legal:** {{legal_advisor_contact}}
- **Autoridades:** {{authorities_contact}}

---

## ✅ Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Responsable de Seguridad | {{security_lead}} | | |
| Líder Técnico | {{technical_lead}} | | |
| Representante Legal | {{legal_representative}} | | |
| Gerente de Proyecto | {{project_manager}} | | |

---

**Fecha de próxima revisión:** `{{next_review_date}}`  
**Versión del reporte:** `{{report_version}}`  

*Este documento es confidencial y para uso exclusivo de los destinatarios autorizados.*