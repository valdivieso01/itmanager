# Changelog 📜

Todos los cambios notables, mejoras arquitectónicas y actualizaciones de este proyecto se registrarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [2.1.1] - 2026-11-23

### ⚡ Corrección de Build en Vercel Moderno (Vercel CLI 66+)
- **Migración a Zero-Config Moderno:** Se eliminó la directiva obsoleta `builds` en `vercel.json` y se adoptó el estándar moderno de `rewrites` hacia `/api/index`.
- **Eliminación del conflicto PEP 668:** Se retiró `build_files.sh`, permitiendo que el motor de construcción nativo de Vercel (`uv`) instale automáticamente `requirements.txt` en un entorno aislado sin errores de `externally-managed-environment`.
- **Resiliencia en Estáticos:** Se configuró WhiteNoise con `CompressedStaticFilesStorage` y `WHITENOISE_USE_FINDERS = True`, eliminando cualquier dependencia de manifiestos previos de `collectstatic`.

---

## [2.1.0] - 2026-11-23

### ⚡ Soporte Plug-and-Play para Vercel
- **Puente WSGI Serverless (`api/index.py`):** Punto de entrada optimizado para el runtime `@vercel/python` con auto-migración en frío para bases de datos SQLite en `/tmp`.
- **Despliegue Zero-Config:** Fallback elástico en `settings.py` que permite arrancar de inmediato en Vercel con cero variables de entorno obligatorias. Si no hay `DATABASE_URL`, utiliza `/tmp/db.sqlite3`.
- **Seguridad y CSRF:** Configuración de `CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app', 'https://*.now.sh']` para permitir autenticación inmediata desde cualquier URL de preview o producción de Vercel sin errores 403.
- **Empaquetado de Estilos Autónomo:** Integración de **WhiteNoise** (`whitenoise.middleware.WhiteNoiseMiddleware` y `WHITENOISE_USE_FINDERS = True`) para servir Bootstrap, CKEditor y recursos estáticos sin requerir buckets externos de S3.
- **Configuración de Vercel (`vercel.json` & `build_files.sh`):** Rutas estandarizadas de Vercel con compilación de estáticos vía `collectstatic`.
- **Optimización de dependencias:** Se incorporó `dj-database-url` y `whitenoise` en `requirements.txt`.

---

## [2.0.0] - 2026-11-22

### 🚀 Modernización a Django 4.2 LTS
- **Actualización de Core:** Migración completa de Django 2.1.3 a **Django 4.2 LTS**, compatible con Python 3.10, 3.11 y 3.12.
- **Resolución de Vulnerabilidades:** Se actualizaron todas las librerías satélite resolviendo las 12 alertas de seguridad de Dependabot.
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
