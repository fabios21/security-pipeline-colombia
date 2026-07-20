# Script para desplegar Security Pipeline Colombia a GitHub
# Ejecutar en PowerShell como administrador si es necesario

Write-Host "🚀 Security Pipeline Colombia - Deployment Script" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Yellow

# Configuración
$repoName = "security-pipeline-colombia"
$githubUser = "TU_USUARIO_AQUI"  # <-- REEMPLAZAR con tu usuario de GitHub
$version = "v1.0.0"

Write-Host "`n📋 Configuración actual:" -ForegroundColor Cyan
Write-Host "Repositorio: $repoName"
Write-Host "Usuario GitHub: $githubUser"
Write-Host "Versión: $version"

# Paso 1: Verificar que estamos en el directorio correcto
$currentDir = Get-Location
Write-Host "`n📍 Directorio actual: $currentDir" -ForegroundColor Cyan

# Paso 2: Verificar archivos esenciales
Write-Host "`n🔍 Verificando archivos esenciales..." -ForegroundColor Cyan
$essentialFiles = @("action.yml", "README.md", "LICENSE", ".gitleaks.toml", ".semgrep.yml")
$missingFiles = @()

foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file encontrado" -ForegroundColor Green
    } else {
        Write-Host "❌ $file NO encontrado" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "`n⚠️  Archivos esenciales faltantes: $($missingFiles -join ', ')" -ForegroundColor Red
    Write-Host "Por favor, asegúrate de que todos los archivos estén presentes."
    exit 1
}

# Paso 3: Verificar Git
Write-Host "`n🔧 Verificando Git..." -ForegroundColor Cyan
try {
    $gitVersion = git --version
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git no encontrado. Instala Git primero." -ForegroundColor Red
    Write-Host "Descarga: https://git-scm.com/download/win"
    exit 1
}

# Paso 4: Verificar estado del repositorio
Write-Host "`n📊 Estado del repositorio Git..." -ForegroundColor Cyan
try {
    git status
} catch {
    Write-Host "ℹ️  No parece ser un repositorio Git inicializado" -ForegroundColor Yellow
}

# Paso 5: Mostrar comandos para ejecutar manualmente
Write-Host "`n🎯 COMANDOS PARA EJECUTAR MANUALMENTE:" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Yellow

Write-Host "`n1️⃣  PRIMERO: Crea el repositorio en GitHub Web:" -ForegroundColor Cyan
Write-Host "   - Ve a: https://github.com/new" -ForegroundColor White
Write-Host "   - Nombre: $repoName" -ForegroundColor White
Write-Host "   - Descripción: Pipeline de seguridad automatizado para GitHub Actions adaptado al contexto colombiano" -ForegroundColor White
Write-Host "   - Público: ✅ SÍ" -ForegroundColor White
Write-Host "   - README: ❌ NO (ya tenemos)" -ForegroundColor White
Write-Host "   - .gitignore: ❌ NO (ya tenemos)" -ForegroundColor White
Write-Host "   - Licencia: ❌ NO (ya tenemos MIT)" -ForegroundColor White

Write-Host "`n2️⃣  SEGUNDO: Configura el remoto (ejecuta estos comandos):" -ForegroundColor Cyan
Write-Host "   git add ." -ForegroundColor White
Write-Host "   git commit -m `"feat: Initial commit - Security Pipeline Colombia $version`"" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/$githubUser/$repoName.git" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White

Write-Host "`n3️⃣  TERCERO: Crea el release:" -ForegroundColor Cyan
Write-Host "   git tag $version" -ForegroundColor White
Write-Host "   git push origin $version" -ForegroundColor White

Write-Host "`n4️⃣  CUARTO: Publica en Marketplace:" -ForegroundColor Cyan
Write-Host "   - Ve a: https://github.com/$githubUser/$repoName/releases" -ForegroundColor White
Write-Host "   - Click en 'Draft new release'" -ForegroundColor White
Write-Host "   - Tag: $version" -ForegroundColor White
Write-Host "   - Título: Security Pipeline Colombia $version" -ForegroundColor White
Write-Host "   - MARCA: 'Publish this Action to the GitHub Marketplace'" -ForegroundColor White
Write-Host "   - Completa el formulario" -ForegroundColor White

Write-Host "`n📝 NOTAS IMPORTANTES:" -ForegroundColor Yellow
Write-Host "----------------------" -ForegroundColor Yellow
Write-Host "1. Reemplaza 'TU_USUARIO_AQUI' con tu usuario real de GitHub" -ForegroundColor White
Write-Host "2. Si ya tienes un remoto 'origin', usa:" -ForegroundColor White
Write-Host "   git remote remove origin" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/$githubUser/$repoName.git" -ForegroundColor White
Write-Host "3. Si encuentras errores, revisa DEPLOY_TO_GITHUB.md" -ForegroundColor White

Write-Host "`n🎉 ¡Listo para desplegar! Buena suerte. 🚀" -ForegroundColor Green