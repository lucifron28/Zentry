#!/bin/bash

# Clean Django Backend Setup Script for SQLite

echo "🧹 Cleaning up Django backend for SQLite deployment..."

cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Make migrations
echo "🗄️ Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "⚡ Applying migrations..."
python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
echo "👤 Creating superuser (optional)..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo "✅ Django backend setup complete!"
echo ""
echo "🧪 Test locally with:"
echo "  python manage.py runserver"
echo ""
echo "🚀 Deploy to Render with:"
echo "  git push origin main"
