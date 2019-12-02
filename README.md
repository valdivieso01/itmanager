## Sofware para gestion de documentacion ti en django

**Isntalar python y demas programas**
sudo apt-get install install python3 python3-devel python-devel python-pip
sudo apt-get install graphviz libgraphviz-dev graphviz-dev pkg-config

**Instalar django v2**

pip install django==2.1.3

**Descargar repositorio en directorio de servidor web**

git clone https://github.com/valdivieso01/itmanager

**Instalar requerimientos con pip**

pip install -r rquirements

**Correr migraciones**

python manage.py makemigrations
python amnage.py migrate

**Generar key de cifrado**

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

**Configurar en settings.py

FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY', 'KEY FOR DATABASE HERE')

SECRET_KEY = 'KEY FOR FILES HERE'

ALLOWED_HOSTS = ["PUBLIC IP","DOMAIN",]

**Si se usa gunicorn configurar en settings.py**

WSGI_APPLICATION = '"NAME APLICATION".wsgi.application'

**Para correr gunicorn usar comando dentro del directorio del servidor web (el comando incluye certificados ssl)**

sudo gunicorn --certfile /etc/letsencrypt/live/itmanager.website/fullchain.pem --keyfile /etc/letsencrypt/live/itmanager.website/privkey.pem --bind 0.0.0.0:8000 tesis.wsgi:application

**Configuracion de base de datos**

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

**El servidor web (en este caso nginx) se configura de esta manera**
<
server {
        listen 443 ssl;
        server_name itmanager.com 
        root /var/www/html/tesis/;
        ssl_certificate      /etc/letsencrypt/live/itmanager/fullchain.pem;
        ssl_certificate_key  /etc/letsencrypt/live/itmanager/privkey.pem;
        index index.html index.htm;
        location /static/ {
                alias /home/ubuntu/.../static/;
        }
        location /media/ {
                alias /home/ubuntu/.../media/;
        }

        location / {
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_redirect off;
            proxy_pass https://itmanager.com:8000;
        }
}
>
