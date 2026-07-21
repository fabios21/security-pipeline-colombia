# Cómo Subir Artifacts de Seguridad Correctamente

## Problema Identificado
Las "composite actions" de GitHub NO pueden subir artifacts directamente usando `actions/upload-artifact`. Esta es una limitación de la plataforma GitHub Actions.

## Solución Implementada
La acción ahora:
1. Genera todos los reportes en el directorio raíz del workspace
2. Los archivos quedan disponibles para que el workflow principal los suba
3. El workflow principal usa `actions/upload-artifact` para subirlos

## Cómo Usar Correctamente

### Opción 1: Subir artifacts directamente (recomendado)
```yaml
steps:
  - name: Run Security Pipeline Colombia
    uses: fabios21/security-pipeline-colombia@main
    # ... configuración ...

  - name: Upload security reports
    if: always()  # IMPORTANTE: Subir incluso si falla el análisis
    uses: actions/upload-artifact@v4.3.1
    with:
      name: security-reports
      path: |
        gitleaks-report.json
        semgrep-results.sarif
        validation-result.json
        visual-report.txt
        security-report-*.html
        security-report-*.md
        security-report-*.json
      retention-days: 30
```

### Opción 2: Job separado para upload (para workflows complejos)
```yaml
jobs:
  security-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Run Security Pipeline Colombia
        uses: fabios21/security-pipeline-colombia@main
        # ... configuración ...
        
      # Los archivos quedan en el workspace, disponibles para el siguiente job
    
  upload-artifacts:
    needs: security-analysis
    runs-on: ubuntu-latest
    if: always()  # IMPORTANTE: Ejecutar incluso si security-analysis falla
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Upload security reports
        uses: actions/upload-artifact@v4.3.1
        with:
          name: security-reports
          path: |
            gitleaks-report.json
            semgrep-results.sarif
            validation-result.json
            visual-report.txt
            security-report-*.html
            security-report-*.md
            security-report-*.json
          retention-days: 30
```

## Archivos Generados
La acción genera los siguientes archivos en el directorio raíz:
- `gitleaks-report.json` - Resultados del escaneo de secretos
- `semgrep-results.sarif` - Resultados del análisis SAST
- `validation-result.json` - Resultado de validación con estado final
- `visual-report.txt` - Reporte visual con emojis
- `security-report-es_CO.html` - Reporte HTML formateado
- `security-report-es_CO.md` - Reporte Markdown
- `security-report-es_CO.json` - Reporte JSON (si se configura)

## CLAVE: Usar if: always()
```yaml
- name: Upload security reports
  if: always()  # ← CRUCIAL: Subir incluso si la acción de seguridad falla
  uses: actions/upload-artifact@v4
```

**¿Por qué `if: always()`?**
- La acción de seguridad FALLA intencionalmente si detecta secretos/vulnerabilidades críticas
- Sin `if: always()`, el paso de upload no se ejecutaría
- Con `if: always()`, los artifacts se suben incluso si hay problemas de seguridad

## Limitaciones de GitHub Actions
- ❌ Las composite actions NO pueden subir artifacts internamente
- ✅ Las composite actions SÍ pueden generar archivos para que el workflow los suba
- ✅ El workflow principal SÍ puede subir artifacts generados por composite actions

## Verificación
Para verificar que los artifacts se están subiendo correctamente:
1. Ejecuta el workflow
2. Ve a la pestaña "Actions" 
3. Haz clic en la ejecución
4. Busca la sección "Artifacts" al final de la página
5. Deberías ver "security-reports" disponible para descarga

## Ejemplos Actualizados
Todos los archivos de ejemplo han sido actualizados para usar el nuevo formato:
- `examples/basic-usage.yml` - Uso básico
- `examples/complete-workflow.yml` - Workflow completo
- `examples/complete-workflow-with-artifacts.yml` - Workflow con job separado para artifacts
- `examples/advanced-configuration.yml` - Configuración avanzada