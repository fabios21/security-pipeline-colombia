@echo off
echo.
echo ==================================================
echo    🚀 Security Pipeline Colombia - Deployment
echo ==================================================
echo.

REM Configuración - EDITAR ESTA LINEA
set GITHUB_USER=fabios21
set REPO_NAME=security-pipeline-colombia
set VERSION=v1.0.6

echo 📋 Configuración:
echo   Usuario GitHub: %GITHUB_USER%
echo   Repositorio: %REPO_NAME%
echo   Versión: %VERSION%
echo.

echo 🔍 Verificando archivos esenciales...
if exist action.yml (
    echo ✅ action.yml encontrado
) else (
    echo ❌ action.yml NO encontrado
    goto :error
)

if exist README.md (
    echo ✅ README.md encontrado
) else (
    echo ❌ README.md NO encontrado
    goto :error
)

if exist LICENSE (
    echo ✅ LICENSE encontrado
) else (
    echo ❌ LICENSE NO encontrado
    goto :error
)

echo.
echo 🎯 PASOS A SEGUIR:
echo ==================
echo.
echo 1. CREA el repositorio en GitHub:
echo    - Ve a: https://github.com/new
echo    - Nombre: %REPO_NAME%
echo    - Descripción: Pipeline de seguridad automatizado para GitHub Actions
echo    - Publico: SI
echo    - NO agregar README, .gitignore o licencia
echo.
echo 2. EJECUTA estos comandos en CMD:
echo    git add .
echo    git commit -m "feat: Initial commit - Security Pipeline Colombia %VERSION%"
echo    git branch -M main
echo    git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
echo    git push -u origin main
echo.
echo 3. CREA el release:
echo    git tag %VERSION%
echo    git push origin %VERSION%
echo.
echo 4. PUBLICA en Marketplace:
echo    - Ve a: https://github.com/%GITHUB_USER%/%REPO_NAME%/releases
echo    - Click 'Draft new release'
echo    - Tag: %VERSION%
echo    - MARCA: 'Publish this Action to the GitHub Marketplace'
echo.
echo 📝 NOTA: Reemplaza TU_USUARIO_AQUI con tu usuario real de GitHub
echo.
echo Presiona cualquier tecla para salir...
pause > nul
exit /b 0

:error
echo.
echo ⚠️  Error: Archivos esenciales faltantes
echo Revisa que todos los archivos estén en el directorio
echo.
echo Presiona cualquier tecla para salir...
pause > nul
exit /b 1