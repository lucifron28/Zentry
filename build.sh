#!/bin/bash
# Build script for Render (SQLite version)
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "📁 Creating staticfiles directory..."
mkdir -p staticfiles

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "👤 Creating superuser if needed..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zentry_backend.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
"

echo "✅ Build completed successfully! Using SQLite database."
