"""
WSGI config for tesis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tesis.settings")

# Auto-migración y creación del primer superusuario en Vercel si no existen
if os.environ.get('VERCEL') == '1':
    try:
        import django
        django.setup()
        from django.core.management import call_command
        call_command('migrate', interactive=False)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@itmanager.local')
            admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin1234!')
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            print(f'[Vercel Startup] Superuser {admin_username} created successfully.')
    except Exception as e:
        print(f'[Vercel Startup] Setup notice: {e}')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application
