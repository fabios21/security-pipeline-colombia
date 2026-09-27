# Manual de Usuario — Security Pipeline Colombia

**Versión:** v1.1.28
**Qué es:** una GitHub Action que revisa automáticamente tu repositorio en busca de secretos expuestos y vulnerabilidades, y bloquea los cambios que representen un riesgo de seguridad.

---

## 1. ¿Para qué sirve?

Cuando trabajas en un proyecto y subes cambios (mediante un Pull Request), es fácil dejar por error una contraseña, una clave de API o un token dentro del código. Estos "secretos" son un riesgo grave de seguridad.

Este pipeline actúa como un **guardia automático**: cada vez que se abre o actualiza un Pull Request, revisa los cambios y:

- ✅ Si todo está limpio, permite continuar.
- ❌ Si encuentra un secreto o una vulnerabilidad grave, **bloquea la fusión** y avisa qué se encontró y cómo corregirlo.

No necesitas ejecutar nada manualmente: funciona solo, dentro de GitHub.

---

## 2. Requisitos previos

- Un repositorio alojado en **GitHub**.
- Permisos para crear archivos en la carpeta `.github/workflows/`.
- (Recomendado) Tener activada la **protección de rama** para que el bloqueo sea obligatorio.

---

## 3. Instalación paso a paso

### Paso 1 — Crear el archivo del workflow

En tu repositorio, crea el archivo `.github/workflows/security.yml`.

Puedes hacerlo desde la web de GitHub:
1. Entra a la pestaña **Actions**.
2. Haz clic en **"set up a workflow yourself"** (configurar un workflow tú mismo).
3. Nombra el archivo `security.yml`.

### Paso 2 — Pegar el contenido

```yaml
name: Security Pipeline Colombia

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  security:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: fabios21/security-pipeline-colombia@v1.1.28
        with:
          scan-mode: pr-only
          semgrep-config: p/owasp-top-ten
          block-on-secrets: true
```

### Paso 3 — Guardar

Confirma los cambios (commit). ¡Listo! A partir de ahora, el pipeline se ejecutará automáticamente en cada Pull Request y push a las ramas `main` y `develop`.

> **Importante:** el `fetch-depth: 0` es necesario para que el análisis funcione. No lo quites.

---

## 4. ¿Cómo se usa en el día a día?

No hay que hacer nada especial. El flujo normal es:

1. Trabajas en una rama y creas un **Pull Request** hacia `main` o `develop`.
2. GitHub ejecuta el pipeline automáticamente (verás un check llamado **"Security Pipeline Colombia"**).
3. Esperas 1-2 minutos a que termine.
4. Revisas el resultado:
   - **Check verde ✅** → no hay problemas de seguridad, puedes fusionar.
   - **Check rojo ❌** → se detectaron secretos o vulnerabilidades; el merge queda bloqueado.

---

## 5. ¿Qué pasa cuando detecta un problema?

Cuando el pipeline encuentra un secreto, ocurren tres cosas:

### 5.1 El check falla (rojo)

El Pull Request muestra el check en rojo y, si tienes protección de rama activada, el botón de fusionar queda deshabilitado.

### 5.2 Aparece un comentario automático en el PR

Se publica un comentario con una tabla como esta:

| # | Archivo | Línea | Regla | Descripción |
|---|---------|-------|-------|-------------|
| 1 | `config.js` | 5 | `stripe-api-key` | Clave de API de Stripe detectada |

Con una sección de **"Cómo resolver"** que indica los pasos.

### 5.3 Se genera un reporte descargable

En la página del run (pestaña Actions), al final encuentras un artifact llamado **`security-reports`** que puedes descargar. Contiene:

- **`security-report-es_CO.html`** — un reporte visual (ábrelo en tu navegador) con cada hallazgo, su riesgo, la solución técnica recomendada y la normatividad colombiana aplicable.
- **`gitleaks-report.json`** — los datos técnicos detallados.

---

## 6. ¿Cómo corrijo un secreto detectado?

Si el pipeline bloqueó tu PR por un secreto:

1. **Elimina el secreto del código.** Reemplázalo por una variable de entorno o un GitHub Secret.
2. **Considera el secreto comprometido.** Aunque lo borres, ya estuvo expuesto: rota o revoca esa credencial (genera una nueva) en el servicio correspondiente.
3. **Vuelve a subir tus cambios.** El pipeline se ejecutará de nuevo y, si ya no hay secretos, aprobará el PR.

### Ejemplo

❌ **Antes (inseguro):**
```javascript
const apiKey = "<CLAVE_REAL_AQUI>"; // ej: una clave de API pegada directamente
```

✅ **Después (seguro):**
```javascript
const apiKey = process.env.STRIPE_API_KEY;
```

Y la clave real se guarda en **Settings → Secrets and variables → Actions** de tu repositorio.

---

## 7. Personalización básica

Puedes ajustar el comportamiento cambiando los valores en el workflow:

| Quiero... | Cambia esto |
|-----------|-------------|
| Escanear todo el historial, no solo el PR | `scan-mode: full-history` |
| No bloquear por vulnerabilidades altas | `block-on-high: false` |
| Recibir el reporte en inglés | `report-language: en` |
| Usar otras reglas de análisis | `semgrep-config: p/security-audit` |

Si no incluyes un ajuste, el pipeline usa su valor por defecto (recomendado para empezar).

---

## 8. Preguntas frecuentes

**¿Tengo que instalar algo en mi computador?**
No. Todo se ejecuta en los servidores de GitHub.

**¿Ralentiza mi trabajo?**
El análisis tarda 1-2 minutos y corre en paralelo. No afecta tu desarrollo local.

**¿Qué pasa si el secreto era falso o de prueba?**
El pipeline igual lo detecta y bloquea (no distingue reales de falsos). Debes quitarlo del código para poder fusionar.

**¿Funciona en repositorios privados?**
Sí, siempre que referencies la acción por su tag (`@v1.1.28`).

**El check quedó rojo pero igual puedo fusionar, ¿por qué?**
Falta activar la **protección de rama**. Ve a Settings → Branches → Add rule y marca "Require status checks to pass before merging", seleccionando el check de seguridad.

---

## 9. Soporte

Ante cualquier duda o problema:
- Revisa el reporte HTML descargable para entender los hallazgos.
- Consulta el `MANUAL_TECNICO.md` para detalles avanzados.
- Reporta incidencias en la sección **Issues** del repositorio del pipeline.

---

## 10. Aviso legal

Los reportes de este pipeline son una guía técnica automatizada y **no constituyen asesoría legal**. Para casos concretos relacionados con protección de datos o delitos informáticos, consulte a un profesional del derecho.
