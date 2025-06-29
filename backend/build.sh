#!/bin/bash
# Build script for Render (SQLite version)
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🗄️ Running database migrations..."
python manage.py migrate

echo "👤 Creating superuser if needed..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo "✅ Build completed successfully! Using SQLite database."
