# Changelog 📜

Todos los cambios notables, mejoras arquitectónicas y actualizaciones de este proyecto se registrarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [2.2.0] - 2026-11-23

### 🎨 Rediseño Visual (UI/UX), Bóveda de Credenciales y Persistencia Cloud
- **Centro de Control TI (`home.html`):** Rediseño completo de la pantalla principal como un Dashboard interactivo con tarjetas de acceso directo a *Grupos & Infraestructura*, *Bóveda de Credenciales*, *Base de Conocimiento*, *Notas Rápidas*, *Mensajería Interna* y *Gestión de Usuarios*.
- **Pantalla de Acceso (`login.html`):** Nuevo diseño centrado tipo tarjeta con identidad visual oscura (`#0f172a`), iconografía integrada en campos y alertas estilizadas.
- **Bóveda de Credenciales Mejorada (`key_detail.html`, `key_form.html`, `key_update_form.html`):**
  - Ocultación de contraseñas por defecto (`type="password"`) con botón de alternancia visual (`Mostrar / Ocultar`).
  - Copiado rápido al portapapeles en 1 clic para *Usuario*, *Contraseña* y *URL* con confirmación dinámica (`✓ ¡Copiado!`).
  - **Generador de Contraseñas Seguras integrado:** Botón `✨ Generar Segura` que utiliza `window.crypto.getRandomValues` para producir claves criptográficas de 16 caracteres alfanuméricos y símbolos.
- **Editor de Documentación Técnica (`CKEditor`):**
  - Expansión al **100% del ancho** disponible y ampliación del área de escritura a **420px de altura** en `main.css` y `settings.py`.
- **Navegación, Acordeones y Botones de Acción Directa (1-Clic):**
  - Integración del botón de apertura/cierre de menú lateral (`[ ☰ ]`) dentro de la barra de navegación superior con desplazamiento fluido (`padding-left: 260px`) en escritorio y *overlay* en móviles, eliminando superposiciones y duplicación de perfil.
  - Conversión de los botones flotantes (`+`) en vistas de acción única (*Llaves*, *Notas*, *Guías*, *Usuarios*, *Grupos* y *Conjuntos*) en enlaces directos de 1 solo clic, acompañados de botones superiores y estados vacíos interactivos.
  - Rediseño de vistas de Conjunto (`set_detail.html`) y Relevamiento (`survey_detail.html`) con contadores en tiempo real, estados vacíos con acción directa y desacoplamiento de la regla legacy `.modalDialog .close`.
- **Base de Datos Cloud Persistente (Neon PostgreSQL):**
  - Soporte automático para variables `POSTGRES_URL`, `POSTGRES_PRISMA_URL` y `DATABASE_URL` en `tesis/settings.py`.
  - Detección nativa **Zero-Config Django** de Vercel a través de `tesis/wsgi.py` con auto-migración y aprovisionamiento automático del superusuario inicial.

---

## [2.1.1] - 2026-11-23

### ⚡ Corrección de Build en Vercel Moderno (Vercel CLI 66+)
- **Migración a Zero-Config Moderno:** Se eliminó la directiva obsoleta `builds` en `vercel.json` y se adoptó el soporte nativo de Django en Vercel.
- **Eliminación del conflicto PEP 668:** Se retiró `build_files.sh`, permitiendo que el motor de construcción nativo de Vercel (`uv`) instale automáticamente `requirements.txt` en un entorno aislado sin errores de `externally-managed-environment`.
- **Resiliencia en Estáticos:** Se configuró WhiteNoise con `CompressedStaticFilesStorage` y `WHITENOISE_USE_FINDERS = True`, eliminando cualquier dependencia de manifiestos previos de `collectstatic`.

---

## [2.1.0] - 2026-11-23

### ⚡ Soporte Plug-and-Play para Vercel
- **Puente WSGI Serverless:** Punto de entrada optimizado para el runtime `@vercel/python` con auto-migración en frío.
- **Despliegue Zero-Config:** Fallback elástico en `settings.py` que permite arrancar de inmediato en Vercel con cero variables de entorno obligatorias. Si no hay `DATABASE_URL` o `POSTGRES_URL`, utiliza `/tmp/db.sqlite3`.
- **Seguridad y CSRF:** Configuración de `CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app', 'https://*.now.sh']` para permitir autenticación inmediata desde cualquier URL de preview o producción de Vercel sin errores 403.
- **Empaquetado de Estilos Autónomo:** Integración de **WhiteNoise** (`whitenoise.middleware.WhiteNoiseMiddleware` y `WHITENOISE_USE_FINDERS = True`) para servir Bootstrap, CKEditor y recursos estáticos sin requerir buckets externos de S3.
- **Optimización de dependencias:** Se incorporó `dj-database-url` y `whitenoise` en `requirements.txt`.

---

## [2.0.0] - 2026-11-22

### 🚀 Modernización a Django 4.2 LTS
- **Actualización de Core:** Migración completa de Django 2.1.3 a **Django 4.2 LTS**, compatible con Python 3.10, 3.11 y 3.12.
- **Resolución de Vulnerabilidades:** Se actualizaron todas las librerías satélite resolviendo las alertas de seguridad de Dependabot.
- **Migración de URLs legacy:** Eliminación de `url()` deprecado por `re_path()` y `path()` en `tesis/urls.py`, `core/urls.py` y `registration/urls.py`.
- **Crispy Forms v2:** Incorporación de `crispy-bootstrap4` y `CRISPY_ALLOWED_TEMPLATE_PACKS`.
- **IDs de 64 bits:** `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`.

---

## [1.1.0] - 2026-11-22

### 🌟 Arquitectura y Configuración
- **Reconstrucción del archivo central `tesis/settings.py`:** Se recuperó e implementó la configuración integral del proyecto Django.
- **Control de versiones:** Se retiró `tesis/settings.py` de `.gitignore` para garantizar portabilidad inmediata al clonar.
- **Portabilidad de almacenamiento privado:** Rutas dinámicas en `core/models.py` y `registration/models.py`.
- **Documentación:** Creación de `README.md` formal de Tesis de Grado y plantilla `.env.example`.
