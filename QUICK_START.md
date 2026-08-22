# ⚡ QUICK START - Instalación Correcta

## 🚨 ADVERTENCIA

**El código que GitHub Marketplace muestra está INCOMPLETO.**

No copies y pegues directamente. Sigue esta guía en su lugar.

---

## ✅ 3 Pasos para Instalar Correctamente

### 1️⃣ Crear la estructura de directorios

```bash
mkdir -p .github/workflows
```

### 2️⃣ Crear el archivo `.github/workflows/security.yml`

Copia EXACTAMENTE este código completo:

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
      uses: fabios21/security-pipeline-colombia@v1.1.0
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
          security-report-*.md
        retention-days: 7
```

### 3️⃣ Commit y push

```bash
git add .github/workflows/security.yml
git commit -m "Add Security Pipeline Colombia workflow"
git push
```

---

## ✔️ Verificar que Funciona

1. **Crear un Pull Request** en tu repositorio
2. **Ir a la pestaña "Actions"** 
3. **Verificar que el workflow se ejecute** (deberías ver el workflow en ejecución)

Si ves el workflow ejecutándose, ¡está instalado correctamente! ✅

---

## ❌ Si aparece error "A sequence was not expected"

**Significa que copiaste el código incompleto del Marketplace.**

**Solución:**
1. Elimina el archivo `.github/workflows/main.yml`
2. Crea `.github/workflows/security.yml` con el código completo de esta guía
3. Haz un nuevo push

---

## 📚 Más Información

- **Documentación completa:** [README.md](README.md)
- **Ejemplos avanzados:** `examples/` folder
- **Problema detallado:** [PROBLEMA_MARKETPLACE_FIX.md](PROBLEMA_MARKETPLACE_FIX.md)

---

## 🎯 Resumen

| Problema | Solución |
|----------|----------|
| "A sequence was not expected" | Usar el código completo de QUICK_START.md |
| Código del Marketplace no funciona | NO copies directamente del Marketplace |
| No sé qué significa el error | Lee PROBLEMA_MARKETPLACE_FIX.md |
| Quiero instalación avanzada | Mira `examples/` en el repositorio |

---

**⚠️ RECUERDA:** Este es un proyecto DEMO educativo. No está diseñado para producción.