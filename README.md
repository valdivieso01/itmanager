## Sofware para gestion de documentacion ti en django

**Install python and this software**
sudo apt-get install install python3 python3-devel python-devel python-pip
sudo apt-get install graphviz libgraphviz-dev graphviz-dev pkg-config

**install django v2**

pip install django==2.1.3

**Copy project on webserver directory**

**Install requirement on requirements file with pip**

pip install -r rquirements

**Run migrations**

python manage.py makemigrations
python amnage.py migrate

**Generate key**

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

**Configurar en settings.py

FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY', 'KEY FOR DATABASE HERE')

SECRET_KEY = 'KEY FOR FILES HERE'

ALLOWED_HOSTS = ["PUBLIC IP","DOMAIN",]

**Si se usa gunicorn**

WSGI_APPLICATION = '"NAME APLICATION".wsgi.application'

**Configuraciond e base de datos**

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

**Configuracion de mail**

EMAIL_BACKEND = "Django.core.mail.backends.filebased.Emailbackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

**Configuracion de almacenamiento para archivos upload de groups y personal keys (no incluye imagenes de group, profile y ckeditor)**

PRIVATE_STORAGE_ROOT = '/"PROJECT DIRECTORY"/media/'
PRIVATE_STORAGE_AUX = '/"PROJECT DIRECTORY"/media'

**Solo activar si se usa certificado ssl**

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

**Reemplazar en /home/"USERNAME"/.local/lib/python3.6/site-packages/private_storage/views.py con el archivo private-storage-views.py**

**Configurar directorio storage en models.py de la app registration**

storage2 = PrivateFileSystemStorage(
    location='/"PROJECT DIRECTORY"/media/user-private/',
    base_url='/user-private/'
)

**Configurar storage directory en models.py de la app core**

storage1 = PrivateFileSystemStorage(
    location='/"PROJECT DIRECTORY"/media/group-private/',
    base_url='/group-private/'
) 
