import os
import sys

# Configurar módulo de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tesis.settings')

# Añadir directorio raíz al path si es necesario
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Inicializar Django
import django
django.setup()

# Auto-migración en frío en Vercel para SQLite en /tmp (despliegue zero-config)
if os.environ.get('VERCEL') == '1':
    db_path = os.environ.get('DB_NAME', '')
    if '/tmp/' in db_path or not os.environ.get('DATABASE_URL'):
        try:
            from django.core.management import call_command
            call_command('migrate', interactive=False)
        except Exception as e:
            print(f'[Vercel Startup] Migration notice: {e}')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
