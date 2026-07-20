# Guía de Contribución

¡Gracias por tu interés en contribuir al Security Pipeline Colombia! Este documento proporciona una guía para contribuir al proyecto.

## ¿Cómo puedo contribuir?

### Reportar Bugs
Si encuentras un bug, por favor crea un issue con la siguiente información:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Capturas de pantalla si aplica
- Versión del pipeline y entorno

### Solicitar Características
Las solicitudes de características son bienvenidas. Por favor:
- Explica por qué la característica sería útil
- Describe el uso esperado
- Si es posible, propón una implementación

### Mejorar Documentación
La documentación siempre puede mejorarse. Puedes:
- Corregir errores tipográficos
- Mejorar ejemplos
- Agregar secciones faltantes
- Traducir a otros idiomas

### Contribuir Código
1. **Fork** el repositorio
2. **Crea una rama** con un nombre descriptivo
   ```bash
   git checkout -b feature/nombre-caracteristica
   ```
3. **Haz tus cambios** siguiendo las convenciones del proyecto
4. **Escribe tests** para tus cambios
5. **Ejecuta tests** locales
   ```bash
   npm test
   ```
6. **Commit** tus cambios
   ```bash
   git commit -m "feat: descripción de los cambios"
   ```
7. **Push** a tu fork
   ```bash
   git push origin feature/nombre-caracteristica
   ```
8. **Abre un Pull Request**

## Convenciones del Proyecto

### Estructura del Código
```
security-pipeline-colombia/
├── src/                    # Código fuente JavaScript/TypeScript
├── dist/                   # Builds compilados
├── .github/
│   ├── workflows/          # GitHub Actions workflows
│   └── scripts/           # Scripts Python auxiliares
├── docs/                   # Documentación
└── tests/                  # Tests
```

### Convenciones de Código
- **JavaScript/TypeScript**: Seguir ESLint/Prettier configurados
- **Python**: Seguir PEP 8, usar type hints
- **YAML**: 2 espacios de indentación
- **Commits**: Conventional Commits (feat, fix, docs, style, refactor, test, chore)
- **Documentación**: Español (es_CO) con opciones en inglés

### Tests
- **Coverage mínimo**: 80%
- **Escribir tests** para nuevas funcionalidades
- **Tests unitarios** para funciones individuales
- **Tests de integración** para flujos completos

## Entorno de Desarrollo

### Requisitos
- Node.js 16+ (para action build)
- Python 3.8+ (para scripts)
- Git
- GitHub CLI (opcional)

### Configuración Local
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/security-pipeline-colombia.git
cd security-pipeline-colombia

# Instalar dependencias
npm install

# Instalar dependencias Python
pip install -r requirements.txt

# Configurar pre-commit hooks
npm run prepare
```

### Build y Testing
```bash
# Ejecutar tests
npm test

# Ejecutar linting
npm run lint

# Ejecutar formateo
npm run format

# Build action
npm run build
```

## Proceso de Revisión

### Criterios de Aceptación
1. **Código limpio** y bien estructurado
2. **Tests completos** y pasando
3. **Documentación actualizada**
4. **Sin regresiones** en funcionalidad existente
5. **Alineado** con objetivos del proyecto

### Flujo de Revisión
1. **Etiquetado automático**: Los PRs son etiquetados automáticamente
2. **Revisión de código**: Al menos un mantenedor debe aprobar
3. **Checks CI**: Todos los workflows deben pasar
4. **Aprobación**: Requiere approvals de mantenedores
5. **Merge**: Solo después de cumplir todos los criterios

## Comunicación

### Canales
- **Issues**: Para bugs y solicitudes de características
- **Discussions**: Para preguntas y discusiones
- **Pull Requests**: Para contribuciones de código
- **Email**: seguridad@empresa.co (solo para asuntos privados)

### Expectativas
- Ser respetuoso y profesional
- Proporcionar contexto suficiente
- Responder a comentarios de revisión
- Mantener conversaciones enfocadas

## Reconocimientos

Las contribuciones son reconocidas de varias maneras:
- **Contribuidores listados** en README.md
- **Menciones** en release notes
- **Badges** para contribuidores frecuentes
- **Invitaciones** al equipo de mantenedores para contribuciones significativas

## Preguntas Frecuentes

### ¿Necesito firmar un CLA?
No, este proyecto usa la licencia MIT que no requiere CLA.

### ¿Puedo contribuir si no hablo español?
Sí, aunque la documentación principal está en español, aceptamos contribuciones en inglés y las traduciremos.

### ¿Cómo manejan la seguridad?
- Reporta vulnerabilidades de seguridad directamente a seguridad@empresa.co
- No publiques vulnerabilidades en issues públicos
- Usamos dependabot para actualizaciones de seguridad

### ¿Qué sucede si mi PR no es aceptado?
- Se proporcionará retroalimentación constructiva
- Puedes modificar y reenviar
- Puedes discutir en el issue relacionado

## Recursos Adicionales

- [Documentación oficial](README.md)
- [Código de Conducta](CODE_OF_CONDUCT.md)
- [Licencia](LICENSE)
- [Changelog](CHANGELOG.md)

---

*Última actualización: Enero 2024*

¡Gracias por ayudar a hacer el desarrollo de software más seguro en Colombia! 🇨🇴🔒