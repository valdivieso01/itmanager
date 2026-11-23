#!/bin/bash
# Script de construcción para Vercel
echo "=== Instalando dependencias Python ==="
python3 -m pip install -r requirements.txt

echo "=== Recopilando archivos estáticos con collectstatic ==="
python3 manage.py collectstatic --noinput --clear

echo "=== Build completado exitosamente ==="
