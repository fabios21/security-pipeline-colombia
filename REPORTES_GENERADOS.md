# 📍 Dónde quedan los reportes de los despliegues con hallazgos

## 🚀 Flujo Completo del Pipeline

### 1. **DURANTE LA EJECUCIÓN (Runner de GitHub Actions)**
Cuando el Security Pipeline Colombia se ejecuta en un repositorio:

```
📁 Directorio del runner:
├── 📄 gitleaks-report.json          ← Resultados del escaneo de secretos
├── 📄 semgrep-results.sarif         ← Resultados del análisis SAST  
├── 📄 validation-result.json        ← Resultado final de validación
├── 📱 visual-report.txt            ← Reporte visual con emojis (NUEVO)
├── 🌐 security-report-es_CO.html   ← Reporte HTML en español
└── 📝 security-report-es_CO.md     ← Reporte Markdown en español
```

### 2. **EN LA CONSOLA DE GITHUB ACTIONS**
Durante la ejecución, puedes ver en tiempo real:

```
🔒 RESULTADO DE ANÁLISIS DE SEGURIDAD - COLOMBIA
════════════════════════════════════════════════════════════════════════════════

❌ ESTADO DE VALIDACIÓN: FAILED
────────────────────────────────────────

🔴 SECRETOS EXPUESTOS: 2
┌─ SECRETO #1
│  📄 ARCHIVO: README.md
│  📍 LÍNEA: 22  
│  ☁️ TIPO: AWS Keys
│  🔖 REGLA: aws-access-key-id
│  ⚠️ SEVERIDAD: ALTA
└─ 🚨 ACCIÓN: ELIMINAR INMEDIATAMENTE
```

### 3. **COMO ARTIFACTS (Para descarga posterior)**
Al final del workflow, los archivos se suben como **artifacts**:

## 📥 Cómo acceder a los reportes paso a paso

### **Opción 1: Desde la interfaz web de GitHub**

1. **Ve a la pestaña "Actions"** de tu repositorio
2. **Haz clic en la ejecución** específica que quieres revisar
3. **Desplázate hacia abajo** hasta la sección "Artifacts"
4. **Descarga** el artifact llamado `security-reports-complete`
5. **Extrae el archivo ZIP** para ver todos los reportes

### **Opción 2: En el mismo Pull Request**

Si configuras comentarios automáticos (como en nuestro ejemplo completo):

1. **Ve al Pull Request** que activó el pipeline
2. **Busca el comentario automático** del Security Pipeline
3. **Revisa el resumen** directamente en el comentario
4. **Sigue el enlace** a la ejecución de GitHub Actions

### **Opción 3: Desde la línea de comandos**

```bash
# Descargar artifacts usando GitHub CLI
gh run download <RUN_ID> --name security-reports-complete

# Ver reporte visual directamente
cat visual-report.txt

# Abrir reporte HTML en navegador
open security-report-es_CO.html
```

## 📊 Tipos de reportes generados

### **1. Reporte Visual (`visual-report.txt`)**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   🔒 ANÁLISIS DE SEGURIDAD - REPORTE VISUAL                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
- ✅ Formato gráfico con emojis y bordes
- ✅ Ideal para revisiones rápidas en consola
- ✅ Categorización visual por tipo de secreto

### **2. Reporte HTML (`security-report-es_CO.html`)**
```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .severity-critical { background: linear-gradient(135deg, #f44336, #d32f2f); }
      .secret-finding { border-left: 6px solid #ff9800; }
    </style>
  </head>
  <body>
    <div class="header">🔒 Reporte de Seguridad Informática</div>
  </body>
</html>
```
- ✅ Diseño moderno con gradientes y animaciones
- ✅ Responsive (se ve bien en móvil y desktop)
- ✅ Gráficos de barras para severidad

### **3. Reporte JSON (`validation-result.json`)**
```json
{
  "status": "failed",
  "summary": {
    "total_secrets": 2,
    "total_vulnerabilities": 1,
    "critical_vulnerabilities": 1
  },
  "secret_findings": [
    {
      "rule": "aws-access-key-id",
      "file": "README.md",
      "line": 22,
      "severity": "high"
    }
  ]
}
```
- ✅ Formato estructurado para integraciones
- ✅ Fácil de parsear por otras herramientas
- ✅ Contiene datos completos para análisis

### **4. Reportes técnicos crudos**
- `gitleaks-report.json` → Resultados detallados de Gitleaks
- `semgrep-results.sarif` → Resultados en formato SARIF estándar

## 🔍 Ejemplo real de hallazgos

### **Caso 1: Secretos detectados en README.md**
```
📄 ARCHIVO: README.md
📍 LÍNEA: 22
☁️ TIPO: AWS Keys  
🔖 REGLA: aws-access-key-id
🕵️ SECRETO: AKIAIOSFODNN7EXAMPLE...
```

**Archivos generados:**
- `gitleaks-report.json` → Contiene el secreto completo y metadata
- `visual-report.txt` → Muestra el hallazgo de manera gráfica
- `security-report-es_CO.html` → Incluye recomendaciones de acción

### **Caso 2: Vulnerabilidad crítica de SQL Injection**
```
📄 ARCHIVO: src/database.py
📍 LÍNEA: 45
🔴 SEVERIDAD: CRÍTICA
📝 DESCRIPCIÓN: Possible SQL injection vulnerability
```

**Archivos generados:**
- `semgrep-results.sarif` → Detalles técnicos de la vulnerabilidad
- `validation-result.json` → Marca el estado como "failed"
- Todos los reportes mostrarán alertas críticas

## 🚨 Sección especial: Alertas de seguridad crítica

Cuando se detectan credenciales sensibles expuestas:

```
🚨 ALERTA DE SEGURIDAD - RIESGO CRÍTICO
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

🔴 CREDENCIALES SENSIBLES EXPUESTAS
   ├─ 📞 Contactar equipo de seguridad inmediatamente
   ├─ 📄 Documentar incidente según protocolo de seguridad
   └─ ⏰ Revisar e implementar controles de seguridad
```

## 🔧 Configuración para diferentes escenarios

### **Para equipos pequeños:**
```yaml
- name: Upload security reports
  uses: actions/upload-artifact@v4
  with:
    name: security-reports
    path: |
      visual-report.txt
      security-report-es_CO.html
```

### **Para equipos enterprise:**
```yaml
- name: Upload ALL security artifacts
  uses: actions/upload-artifact@v4
  with:
    name: security-analysis-${{ github.run_id }}
    path: |
      gitleaks-report.json
      semgrep-results.sarif  
      validation-result.json
      visual-report.txt
      security-report-es_CO.*
    retention-days: 90  # Guardar por 3 meses
```

### **Para integración con SIEM/SOAR:**
```yaml
- name: Send to security dashboard
  run: |
    # Enviar validation-result.json a tu dashboard
    curl -X POST https://dashboard.tuempresa.co/security-events \
      -H "Content-Type: application/json" \
      -d @validation-result.json
```

## 📈 Retención y gestión de reportes

### **Por defecto en GitHub Actions:**
- ✅ **Artifacts**: Se guardan por 90 días (configurable)
- ✅ **Logs de ejecución**: Disponibles indefinidamente
- ✅ **Comentarios en PR**: Permanecen con el PR

### **Recomendaciones de retención:**
- **Hallazgos críticos**: Guardar por 1 año (requisitos de auditoría)
- **Hallazgos medios/bajos**: 90 días es suficiente
- **Reportes de cumplimiento**: 2 años (requisitos legales)

## 🚨 Qué hacer cuando encuentras hallazgos

### **Paso 1: Revisar el reporte visual**
```bash
# Ver el resumen rápido
cat visual-report.txt | head -50
```

### **Paso 2: Analizar detalles específicos**
```bash
# Ver todos los secretos detectados
jq '.secret_findings[] | "\(.file):\(.line) - \(.rule)"' validation-result.json

# Ver vulnerabilidades críticas
jq '.vulnerability_findings[] | select(.severity == "critical")' validation-result.json
```

### **Paso 3: Tomar acción**
1. **Secretos expuestos**: Eliminar inmediatamente del código
2. **Vulnerabilidades críticas**: Corregir en máximo 7 días
3. **Revisión de seguridad**: Consultar con equipo de seguridad

### **Paso 4: Documentar la resolución**
```bash
# Actualizar el issue de seguridad
# Cerrar el hallazgo en tu sistema de tracking
# Actualizar el dashboard de seguridad
```

## 🔗 Enlaces útiles

- 📖 [Documentación oficial de GitHub Actions Artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
- 🛠️ [GitHub CLI para descargar artifacts](https://cli.github.com/manual/gh_run_download)
- 📊 [Ejemplo completo de workflow](examples/complete-workflow-with-artifacts.yml)
- 🔧 [Ejemplo básico de uso](examples/basic-usage.yml)

---

**📌 Resumen final:** Los reportes de hallazgos de seguridad quedan disponibles como **artifacts descargables** en cada ejecución de GitHub Actions, además de mostrarse **visualmente en la consola** durante la ejecución y (opcionalmente) como **comentarios en los Pull Requests**.