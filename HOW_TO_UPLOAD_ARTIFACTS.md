# Cómo Subir Artifacts de Seguridad Correctamente

## Problema Identificado
Los artifacts no se estaban generando en los despliegues porque la acción de seguridad es una "composite action" y no puede subir artifacts directamente usando `actions/upload-artifact`.

## Solución Implementada
La acción ahora:
1. Genera todos los reportes en el directorio raíz temporalmente
2. Copia todos los archivos al directorio `security-artifacts/` en el paso 10
3. Prepara los archivos para que el workflow principal los suba

## Cómo Usar Correctamente

### Opción 1: Subir artifacts directamente (recomendado para workflows simples)
```yaml
steps:
  - name: Run Security Pipeline Colombia
    uses: fabios21/security-pipeline-colombia@v1.0.7
    # ... configuración ...

  - name: Upload security reports
    if: always()  # Subir incluso si falla el análisis
    uses: actions/upload-artifact@v4
    with:
      name: security-reports
      path: security-artifacts/  # ← IMPORTANTE: Subir todo el directorio
      retention-days: 30
```

### Opción 2: Job separado para upload (recomendado para workflows complejos)
```yaml
jobs:
  security-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: Run Security Pipeline Colombia
        uses: fabios21/security-pipeline-colombia@v1.0.7
        # ... configuración ...
    
    outputs:
      # Puedes usar outputs para pasar información entre jobs
      validation-status: ${{ steps.security.outputs.status }}
      secret-count: ${{ steps.security.outputs.secret-count }}
  
  upload-artifacts:
    needs: security-analysis
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Download security artifacts
        uses: actions/download-artifact@v4
        with:
          name: security-artifacts
          path: ./security-artifacts
          
      - name: Upload security reports as artifacts
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: security-artifacts/  # ← IMPORTANTE
          retention-days: 30
```

## Archivos Generados
La acción genera los siguientes archivos en `security-artifacts/`:
- `gitleaks-report.json` - Resultados del escaneo de secretos
- `semgrep-results.sarif` - Resultados del análisis SAST
- `validation-result.json` - Resultado de validación con estado final
- `visual-report.txt` - Reporte visual con emojis
- `security-report-es_CO.html` - Reporte HTML formateado
- `security-report-es_CO.md` - Reporte Markdown
- `security-report-es_CO.json` - Reporte JSON (si se configura)

## Ejemplos Actualizados
Todos los archivos de ejemplo han sido actualizados:
- `examples/basic-usage.yml` - Uso básico
- `examples/complete-workflow.yml` - Workflow completo
- `examples/complete-workflow-with-artifacts.yml` - Workflow con job separado para artifacts
- `examples/advanced-configuration.yml` - Configuración avanzada

## Notas Importantes
1. La acción NO sube artifacts automáticamente - el workflow principal debe hacerlo
2. Usar `if: always()` para subir artifacts incluso si el análisis falla
3. Los artifacts se guardan en GitHub por 90 días por defecto (configurable)
4. Para acceder a los artifacts: Actions → Ejecución → Artifacts

## Verificación
Para verificar que los artifacts se están subiendo correctamente:
1. Ejecuta el workflow
2. Ve a la pestaña "Actions"
3. Haz clic en la ejecución
4. Busca la sección "Artifacts" al final de la página
5. Deberías ver "security-reports" disponible para descarga