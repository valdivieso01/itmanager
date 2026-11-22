# Changelog 📜

Todos los cambios notables, mejoras arquitectónicas y actualizaciones de este proyecto se registrarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [2.0.0] - 2026-11-22

### 🚀 Modernización a Django 4.2 LTS
- **Actualización de Core:** Migración completa de Django 2.1.3 a **Django 4.2 LTS** (Long Term Support), compatible con Python 3.10, 3.11 y 3.12.
- **Resolución de Vulnerabilidades:** Se actualizaron todas las librerías satélite (`cryptography`, `Pillow`, `django-ckeditor`, `django-qr-code`, `django-simple-history`, `django-private-storage`, `django-extensions`) resolviendo las 12 alertas de seguridad reportadas por Dependabot.
- **Migración de URLs legacy:** Se eliminaron las importaciones deprecadas de `django.conf.urls.url`, reemplazándolas por el estándar moderno `django.urls.re_path` y `path` en `tesis/urls.py`, `core/urls.py` y `registration/urls.py`.
- **Compatibilidad con Crispy Forms v2:** Incorporación del paquete `crispy-bootstrap4` y configuración de `CRISPY_ALLOWED_TEMPLATE_PACKS` en `settings.py`.
- **Estandarización de IDs:** Configuración de `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'` en `settings.py` para compatibilidad con bases de datos modernas.

### 🐳 Contenedorización Moderna
- **Dockerfile optimizado:** Imagen basada en `python:3.11-slim` con instalación automática de bibliotecas de C requeridas (`graphviz`, `libgraphviz-dev`, `libpq-dev`).
- **docker-compose.yml:** Configuración de servicios orquestados (`web` + `db` PostgreSQL 15) con healthcheck de base de datos y persistencia en volúmenes.

---

## [1.1.0] - 2026-11-22

### 🌟 Arquitectura y Configuración
- **Reconstrucción del archivo central `tesis/settings.py`:** Se recuperó e implementó la configuración integral del proyecto Django.
- **Control de versiones:** Se retiró `tesis/settings.py` de `.gitignore` para garantizar portabilidad inmediata al clonar.
- **Portabilidad de almacenamiento privado:** Rutas dinámicas en `core/models.py` y `registration/models.py` basadas en `settings.BASE_DIR` y `PRIVATE_STORAGE_ROOT`.
- **Documentación:** Creación de `README.md` formal de Tesis de Grado y plantilla `.env.example`.
