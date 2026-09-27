# Manual Técnico — PipelineShield

**Nombre del proyecto:** PipelineShield
**Versión de la acción:** v1.1.28
**Tipo:** GitHub Action (composite)
**Repositorio:** `fabios21/security-pipeline-colombia`
**Licencia:** MIT

---

## 1. Introducción

PipelineShield es una GitHub Action que automatiza el análisis de seguridad en repositorios de código. Su objetivo es **detectar secretos expuestos y vulnerabilidades de código** antes de que un cambio se integre a las ramas principales, bloqueando de forma automática los Pull Requests que incumplan las políticas de seguridad.

Está orientada al contexto colombiano: los reportes se generan en español (`es_CO`), usan la zona horaria `America/Bogota` e incluyen referencias a la normatividad nacional aplicable (Ley 1273 de 2009, Ley 1581 de 2012 y Decreto 1377 de 2013).

### 1.1 Público objetivo de este manual

Personal técnico: desarrolladores, ingenieros DevOps y responsables de seguridad que necesiten instalar, configurar, mantener o extender el pipeline.

---

## 2. Arquitectura

### 2.1 Tipo de acción

Es una **composite action**: un conjunto de pasos declarados en `action.yml` que se ejecutan de forma secuencial dentro de un job del workflow que la invoca. No requiere que el repositorio consumidor instale dependencias manualmente; la acción prepara su propio entorno.

### 2.2 Componentes principales

| Componente | Ruta | Función |
|------------|------|---------|
| Definición de la acción | `action.yml` | Orquesta todos los pasos, inputs y outputs |
| Configuración de secretos | `.gitleaks.toml` | Reglas de detección de secretos de Gitleaks |
| Configuración SAST | `.semgrep.yml` | Reglas de análisis estático (respaldo local) |
| Validador | `.github/scripts/validate_security.py` | Consolida hallazgos y decide el estado (passed/failed/requires_approval) |
| Generador de reporte | `.github/scripts/generate_report.py` | Produce el reporte HTML/Markdown |
| Reporte visual | `.github/scripts/visual_report.py` | Genera el resumen en texto para logs |
| Utilidad de conteo | `.github/scripts/sanitize_count.sh` | Normaliza conteos numéricos de forma segura |

### 2.3 Herramientas integradas

- **Gitleaks v8.18.1** — detección de secretos y credenciales expuestas.
- **Semgrep v1.97.0** — análisis estático de código (SAST) con reglas OWASP Top 10.
- **Python 3** — scripts de validación, consolidación y generación de reportes.

### 2.4 Flujo de ejecución

```
1. Setup Node.js + Python
2. Checkout del código (requiere fetch-depth: 0)
3. Configuración del entorno (idioma, zona horaria, nivel de cumplimiento)
4. Instalación de herramientas (Gitleaks, Semgrep, dependencias Python)
5. Escaneo de secretos con Gitleaks       -> gitleaks-report.json
6. Análisis SAST con Semgrep               -> semgrep-results.sarif
7. Validación de resultados                -> validation-result.json
8. Verificación de cumplimiento
9. Generación de reportes                  -> security-report-es_CO.html
10. Publicación del artifact (security-reports)
11. Verificación final de políticas
12. Resumen final
13. Aplicación del bloqueo (exit 1 si corresponde)
```

### 2.5 Modos de escaneo (`scan-mode`)

- **`pr-only`** (por defecto): escanea solo los cambios entre la base y la cabeza del Pull Request.
- **`commit-only`**: escanea únicamente el último commit.
- **`full-history`**: escanea todo el historial del repositorio.

---

## 3. Referencia de entradas (inputs)

| Input | Por defecto | Descripción |
|-------|-------------|-------------|
| `scan-mode` | `pr-only` | Modo de escaneo: `full-history`, `pr-only`, `commit-only` |
| `config-path` | `.gitleaks.toml` | Ruta a la configuración personalizada de Gitleaks |
| `semgrep-config` | `p/owasp-top-ten` | Ruleset de Semgrep (`p/ci`, `p/security-audit`, etc.) |
| `compliance-level` | `standard` | Nivel de cumplimiento: `standard`, `enhanced`, `strict`, `custom` |
| `timezone` | `America/Bogota` | Zona horaria para los reportes |
| `report-language` | `es_CO` | Idioma del reporte: `es_CO`, `es`, `en` |
| `report-formats` | `html,markdown` | Formatos de reporte a generar |
| `block-on-secrets` | `true` | Bloquear el merge si hay secretos expuestos |
| `block-on-critical` | `true` | Bloquear si hay vulnerabilidades críticas (CVSS ≥ 9.0) |
| `block-on-high` | `true` | Bloquear si hay vulnerabilidades altas (CVSS ≥ 7.0) |
| `require-approval-on-medium` | `true` | Requerir aprobación si hay vulnerabilidades medias (CVSS ≥ 4.0) |
| `slack-webhook` | (vacío) | URL de webhook de Slack para notificaciones |
| `email-notifications` | (vacío) | Lista de correos para notificaciones |
| `security-contact` | (vacío) | Correo del responsable de seguridad |
| `dev-team-contact` | (vacío) | Correo del equipo de desarrollo |

> **Nota:** todos los inputs son opcionales. Si se dejan vacíos, la acción usa el valor por defecto de forma automática.

---

## 4. Referencia de salidas (outputs)

| Output | Descripción |
|--------|-------------|
| `validation-status` | Estado final: `passed`, `failed` o `requires_approval` |
| `secret-count` | Número de secretos detectados |
| `vulnerability-count` | Total de vulnerabilidades detectadas |
| `critical-count` | Vulnerabilidades críticas detectadas |
| `high-count` | Vulnerabilidades altas detectadas |
| `report-url` | Ruta del reporte HTML generado |
| `compliance-status` | Estado de cumplimiento de seguridad |

---

## 5. Políticas de bloqueo

La acción decide el resultado final combinando los hallazgos con los inputs de política:

| Condición | Input que la controla | Resultado por defecto |
|-----------|----------------------|-----------------------|
| Secretos detectados | `block-on-secrets` | ❌ Bloquea el PR |
| Vulnerabilidad crítica (CVSS ≥ 9.0) | `block-on-critical` | ❌ Bloquea el PR |
| Vulnerabilidad alta (CVSS ≥ 7.0) | `block-on-high` | ❌ Bloquea el PR |
| Vulnerabilidad media/baja | `require-approval-on-medium` | ⚠️ Requiere aprobación |
| Sin hallazgos | — | ✅ Aprobado |

Cuando el resultado es de bloqueo, el último paso de la acción finaliza con `exit 1`, lo que hace que el check de GitHub Actions falle y el merge no pueda completarse (si el repositorio tiene protección de rama configurada).

---

## 6. Reportes generados

Al finalizar, la acción publica un artifact llamado **`security-reports`** con:

- **`security-report-es_CO.html`** — reporte visual con hallazgos, ubicación (archivo y línea), riesgo, solución técnica y normatividad aplicable.
- **`gitleaks-report.json`** — salida cruda de Gitleaks con el detalle de cada secreto (regla, archivo, línea, commit, autor).

Además, en cada Pull Request se publica automáticamente un comentario con el resumen de los secretos detectados.

---

## 7. Configuración de reglas

### 7.1 Detección de secretos (`.gitleaks.toml`)

Incluye reglas para contraseñas en texto plano, variables de credenciales en mayúsculas, tokens de GitHub, claves AWS, claves Stripe, webhooks de Slack, claves de Google, tokens JWT y claves privadas, además de reglas específicas del contexto colombiano (tokens de entidades gubernamentales y financieras).

El `[allowlist]` excluye únicamente archivos de ejemplo (`example`, `sample`); **no** excluye archivos con "test" en el nombre, para no dejar pasar secretos en archivos de prueba.

### 7.2 Análisis SAST (`semgrep-config`)

Por defecto usa el ruleset gestionado `p/owasp-top-ten`. Puede cambiarse a otros rulesets de Semgrep (`p/ci`, `p/security-audit`) o a un archivo local de reglas.

---

## 8. Publicación de versiones (mantenimiento)

El versionado se maneja con tags de Git:

1. Aplicar cambios en `action.yml` o en los scripts.
2. Commit y push a `main`.
3. Crear un tag nuevo: `git tag v1.1.XX -m "descripción"` y `git push origin v1.1.XX`.
4. (Opcional) Mover el tag flotante `v1` a la nueva versión para los consumidores que usan `@v1`.
5. Para publicar en el Marketplace: crear un **Release** en la web de GitHub sobre ese tag y marcar la casilla de Marketplace.

> **Importante:** publicar un tag **no** actualiza automáticamente el Marketplace. El Marketplace solo refleja la versión del último Release publicado manualmente con la casilla de Marketplace activada.

---

## 9. Consideraciones y limitaciones

- El paso de checkout del workflow consumidor **debe** usar `fetch-depth: 0`; de lo contrario, el escaneo por rango de commits no funciona.
- Los reportes SARIF de Semgrep pueden ser voluminosos; por eso el artifact publicado se limita al HTML y al JSON de Gitleaks.
- Los secretos detectados se muestran de forma **redactada** (`--redact`) en los logs y reportes.
- La acción "falla cerrado": si un escáner no puede completar el análisis, el resultado se marca como bloqueado para no aprobar con datos no confiables.

---

## 10. Marco normativo colombiano

| Norma | Alcance | Autoridad |
|-------|---------|-----------|
| **Ley 1273 de 2009** | Delitos informáticos; protección de la información y los datos | Fiscalía / Rama Judicial |
| **Ley 1581 de 2012** | Protección de datos personales | Superintendencia de Industria y Comercio (SIC) |
| **Decreto 1377 de 2013** | Reglamenta parcialmente la Ley 1581 | Superintendencia de Industria y Comercio (SIC) |

> Este contenido es una guía técnica automatizada y no constituye asesoría legal.

---

## 11. Solución de problemas comunes

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| "No se encontró la configuración Semgrep:" | Input `semgrep-config` vacío en versión antigua | Actualizar a v1.1.28 o dar valor `p/owasp-top-ten` |
| El escaneo no detecta secretos del PR | Falta `fetch-depth: 0` en el checkout | Agregar `fetch-depth: 0` al paso de checkout |
| El artifact no aparece | El run usó una versión antigua de la acción | Confirmar que el workflow usa `@v1.1.28` y revisar el run más reciente |
| El Marketplace muestra una versión vieja | No se publicó Release de la versión nueva | Publicar Release del tag actual con casilla de Marketplace |
