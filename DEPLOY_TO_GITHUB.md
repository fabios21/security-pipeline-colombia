# Guía para Subir a GitHub y Publicar en Marketplace

## 🔧 Requisitos Previos:
1. Cuenta en GitHub (https://github.com)
2. Git instalado en tu computadora
3. Acceso a línea de comandos (CMD o PowerShell)

## 🚀 Pasos Detallados:

### **Paso 1: Crear Repositorio en GitHub**
1. Ir a https://github.com
2. Click en "+" (esquina superior derecha) → "New repository"
3. Configurar:
   - **Owner**: tu-usuario
   - **Repository name**: `security-pipeline-colombia`
   - **Description**: `Pipeline de seguridad automatizado para GitHub Actions adaptado al contexto colombiano`
   - **Public** (✔️ Marcar)
   - **Initialize this repository with:**
     - ☐ Add a README file (DESMARCAR - ya tienes uno)
     - ☐ Add .gitignore (DESMARCAR - ya tienes uno)
     - ☐ Choose a license (DESMARCAR - ya tienes MIT)
4. Click "Create repository"

### **Paso 2: Obtener URL del Repositorio**
Después de crear, GitHub mostrará una URL como:
```
https://github.com/tu-usuario/security-pipeline-colombia.git
```
¡Cópiala!

### **Paso 3: Configurar Repositorio Local**
**Abre PowerShell o CMD y ejecuta:**

```powershell
# Navegar a tu proyecto
cd "c:\Users\fabio\OneDrive\Documentos\Poyectos Kiro 2026\Sena\Proyecto final SENA"

# Verificar estado actual
git status

# Si hay cambios, agregarlos todos
git add .

# Hacer commit
git commit -m "feat: Prepare Security Pipeline Colombia v1.0.0 for GitHub Marketplace"

# Agregar remoto (si no está configurado)
git remote add origin https://github.com/tu-usuario/security-pipeline-colombia.git

# Subir a GitHub
git push -u origin main
```

### **Paso 4: Si tienes errores de remoto existente:**
```powershell
# Verificar remotos actuales
git remote -v

# Si ya existe 'origin', cambiar nombre o remover:
git remote rename origin old-origin
# O si quieres reemplazarlo:
git remote remove origin
git remote add origin https://github.com/tu-usuario/security-pipeline-colombia.git
```

### **Paso 5: Si necesitas forzar push (primera vez):**
```powershell
git push -u origin main --force
```

### **Paso 6: Crear Release para Marketplace**
```powershell
# Crear tag de versión
git tag v1.0.0

# Subir tag a GitHub
git push origin v1.0.0
```

## 🌐 Publicar en Marketplace:

### **Desde GitHub Web:**
1. Ir a tu repositorio: https://github.com/tu-usuario/security-pipeline-colombia
2. Click en "Releases" (lado derecho)
3. Click en "Draft a new release"
4. En "Choose a tag", seleccionar `v1.0.0`
5. Título: `Security Pipeline Colombia v1.0.0`
6. Descripción: Copiar de CHANGELOG.md
7. **IMPORTANTE**: Marcar ✔️ "Publish this Action to the GitHub Marketplace"
8. Completar formulario de Marketplace
9. Click "Publish release"

### **Formulario de Marketplace:**
- **Name**: Security Pipeline Colombia
- **Description**: Pipeline de seguridad automatizado para proyectos de desarrollo de software con enfoque en cumplimiento Ley 1581 de protección de datos en Colombia
- **Category**: Security
- **Pricing**: Free
- **Badges**: Add relevant badges
- **Screenshots**: Optional (puedes agregar después)

## 🔍 Verificación:

### **Después de publicar:**
1. Verificar que el repositorio está público
2. Verificar que el release `v1.0.0` existe
3. Verificar que la acción aparece en Marketplace
4. Probar la instalación en un repositorio de prueba

### **URLs importantes:**
- Repositorio: `https://github.com/tu-usuario/security-pipeline-colombia`
- Releases: `https://github.com/tu-usuario/security-pipeline-colombia/releases`
- Marketplace: `https://github.com/marketplace/actions/security-pipeline-colombia`

## 🐛 Solución de Problemas Comunes:

### **Error: "remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/tu-usuario/security-pipeline-colombia.git
```

### **Error: "failed to push some refs"**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### **Error: Permisos denegados**
- Verificar que tienes acceso al repositorio
- Verificar token de GitHub (Settings → Developer settings → Personal access tokens)

### **No se ve en Marketplace inmediatamente**
- Esperar 5-10 minutos después de publicar release
- Recargar la página
- Verificar email de GitHub para notificaciones

## 📞 Soporte:

Si tienes problemas:
1. Revisar esta guía paso a paso
2. Buscar error específico en Google
3. Contactar soporte de GitHub
4. Pedir ayuda en foros de desarrollo

---

## ✅ Checklist Final:

- [ ] Repositorio creado en GitHub
- [ ] Archivos subidos correctamente
- [ ] Release v1.0.0 creado
- [ ] Marketplace form completado
- [ ] Acción aparece en Marketplace
- [ ] Puedes instalarla en otro repositorio

---

**¡Buena suerte con la publicación!** 🚀

*Recuerda reemplazar `tu-usuario` con tu nombre de usuario real de GitHub.*