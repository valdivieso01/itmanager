# IT Manager 🏢💻

### Sistema Web de Gestión Centralizada de Documentación Técnica y Activos de TI

Plataforma empresarial de grado de producción desarrollada como **Tesis de Grado**, diseñada para organizar, auditar y proteger la infraestructura tecnológica, documentación de procedimientos, manuales de servidores y credenciales de departamentos de Tecnologías de la Información.

Construida con **Django**, **Python**, **PostgreSQL / SQLite**, **Docker**, **Bootstrap** y un robusto esquema de **seguridad criptográfica (Fernet / AES)** y **almacenamiento privado de archivos**.

---

## 🌟 Módulos y Capacidades del Sistema

### 1. 🔐 Cifrado de Datos y Credenciales en Reposo
- Los campos confidenciales (contraseñas de infraestructura, API keys, tokens de acceso a switches/routers) se almacenan en la base de datos mediante **cifrado simétrico AES/Fernet** con `django-encrypted-model-fields`.
- Imposibilita la lectura de credenciales críticas incluso ante un volcado no autorizado de la base de datos.

### 2. 📁 Almacenamiento Seguro con Descarga Privada (`django-private-storage`)
- Los manuales, diagramas de red y archivos confidenciales **no se exponen públicamente en una carpeta estática** de Nginx/Apache.
- Cada solicitud de archivo pasa por el motor de vistas privadas de Django, que valida la sesión del usuario, su membresía a grupos técnicos y sus roles antes de transmitir el archivo mediante streaming seguro.

### 3. 🏷️ Gestión de Activos Físicos con Códigos QR (`django-qr-code`)
- Generación automática de etiquetas QR para cada servidor, rack, equipo de red o puesto de trabajo registrado.
- Permite a los técnicos de campo escanear el QR desde su dispositivo móvil para acceder instantáneamente a la ficha técnica, historial de mantenimiento y documentación asociada del equipo.

### 4. 📝 Editor de Documentación y Procedimientos Enriquecido (CKEditor)
- Elaboración de guías técnicas, runbooks de contingencia y protocolos de soporte utilizando **CKEditor**, con soporte de tablas, bloques de código, formateo avanzado e inserción de imágenes.

### 5. 📜 Auditoría Integral y Versionado de Cambios (`django-simple-history`)
- Registro histórico automático de cada creación, modificación o baja de documentos y activos.
- Permite auditar qué usuario realizó un cambio, en qué fecha y hora, y qué valores específicos fueron modificados, garantizando trazabilidad y cumplimiento normativo (ISO 27001 / ITIL).

### 6. 💬 Mensajería Interna y Gestión de Grupos Técnicos (`messenger`, `profiles`, `registration`)
- Canales de comunicación directa entre administradores de sistemas y técnicos de soporte.
- Segmentación por grupos de trabajo (Redes, Seguridad, Desarrollo, Soporte N1/N2) con permisos granulares.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnologías |
| :--- | :--- |
| **Backend & Framework** | [Django 2.x](https://www.djangoproject.com/) • Python 3 |
| **Bases de Datos** | PostgreSQL (Producción) / SQLite (Desarrollo) |
| **Seguridad & Criptografía** | `cryptography` (Fernet), `django-encrypted-model-fields` |
| **Control de Archivos** | `django-private-storage` |
| **Auditoría & Trazabilidad** | `django-simple-history` |
| **UI & Formularios** | Bootstrap, `django-crispy-forms`, CKEditor |
| **Etiquetado de Activos** | `django-qr-code`, `Pillow` |
| **Contenedores** | Docker, Docker Compose |

---

## 🏛️ Estructura del Proyecto

```
itmanager/
├── core/                   # Modelos centrales, documentación técnica, activos y QR
├── messenger/              # Sistema de mensajería interna entre técnicos
├── profiles/               # Perfiles de usuario, roles de soporte y avatares
├── registration/           # Autenticación, registro y recuperación de cuentas
├── tesis/                  # Configuración global del proyecto Django (settings, urls, wsgi)
├── media/                  # Almacenamiento privado de archivos cifrados
├── private-storage-views.py# Custom views para el streaming autenticado de archivos
├── start.sh                # Script de arranque y migraciones para entornos Linux
├── requirements            # Dependencias del proyecto Python
└── manage.py               # CLI de administración de Django
```

---

## 🚀 Despliegue y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/valdivieso01/itmanager.git
cd itmanager
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\Activate.ps1

pip install -r requirements
```

### 3. Generar la clave de cifrado Fernet
Para el cifrado de campos sensibles en la base de datos, genera tu clave con:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:
```env
DEBUG=True
SECRET_KEY=tu_clave_secreta_de_django
FIELD_ENCRYPTION_KEY=tu_clave_fernet_generada_en_el_paso_3
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Ejecutar migraciones y crear superusuario
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Iniciar el servidor
```bash
python manage.py runserver
```
Accede al portal en [http://localhost:8000](http://localhost:8000) y al panel de administración en [http://localhost:8000/admin](http://localhost:8000/admin).

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos y de investigación como Proyecto de Tesis de Grado en Tecnologías de la Información. Licencia MIT.
