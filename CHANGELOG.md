# Changelog 📜

Todos los cambios notables, mejoras arquitectónicas y correcciones de este proyecto se registrarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [1.1.0] - 2026-11-22

### 🌟 Arquitectura y Configuración
- **Reconstrucción del archivo central `tesis/settings.py`:** Se recuperó e implementó la configuración integral del proyecto Django (desacoplada con lectura de variables de entorno y fallback seguro para desarrollo local en SQLite o PostgreSQL).
- **Control de versiones:** Se retiró `tesis/settings.py` de `.gitignore` para garantizar que cualquier clon del repositorio sea ejecutable de inmediato sin requerir configuración manual opaca.
- **Portabilidad de almacenamiento privado:** Se eliminaron las rutas absolutas fijas a `/home/ubuntu/tesis/media/` en `core/models.py` y `registration/models.py`, reemplazándolas por rutas dinámicas basadas en `settings.BASE_DIR` y configurables vía `PRIVATE_STORAGE_ROOT`.

### 📦 Dependencias y Estandarización
- **Creación de `requirements.txt`:** Se estandarizó el archivo de dependencias de Python bajo el formato canónico `requirements.txt`, incluyendo `Django` y `cryptography`.
- **Plantilla de entorno:** Inclusión de `.env.example` con variables de entorno para claves criptográficas Fernet y bases de datos.

### 📚 Documentación
- Creación de este archivo `CHANGELOG.md`.
- Redacción completa del `README.md` formalizando la presentación académica y empresarial del proyecto de Tesis de Grado.
