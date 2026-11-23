import os
import sys

# Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Configurar módulo de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tesis.settings')

# Auto-migración en Vercel para SQLite en /tmp en el primer arranque
if os.environ.get('VERCEL') == '1' and not os.path.exists('/tmp/db.sqlite3'):
    try:
        import django
        django.setup()
        from django.core.management import call_command
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f'[Vercel Startup] Auto-migration notice: {e}')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
