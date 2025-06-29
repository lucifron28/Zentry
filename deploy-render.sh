#!/bin/bash

# Alternative deployment script for Render (free tier available)
set -e

echo "🚀 Setting up Zentry Backend for Render deployment..."

# Ensure we're in the backend directory
cd "$(dirname "$0")"

# Create render.yaml for Render deployment
cat > render.yaml << 'EOF'
services:
  - type: web
    name: zentry-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn zentry_backend.wsgi:application
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: "*.onrender.com"
      - key: CORS_ALLOWED_ORIGINS
        value: "https://zentry-ron-cada-projects.vercel.app/"
  
  - type: pserv
    name: zentry-postgres
    env: postgres
    region: oregon

databases:
  - name: zentry-db
    databaseName: zentry
    user: zentry_user
EOF

echo "✅ Created render.yaml configuration"

# Create build script for Render
cat > build.sh << 'EOF'
#!/bin/bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
EOF

chmod +x build.sh

echo "✅ Created build script for Render"

echo ""
echo "🌐 To deploy on Render (free tier):"
echo "1. Push your code to GitHub"
echo "2. Go to https://render.com and create an account"
echo "3. Connect your GitHub repository"
echo "4. Render will automatically detect the render.yaml configuration"
echo ""
echo "💡 Alternative manual setup on Render:"
echo "1. Create a new 'Web Service' on Render"
echo "2. Connect your GitHub repo"
echo "3. Use these settings:"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn zentry_backend.wsgi:application"
echo "4. Add environment variables in Render dashboard"
echo ""
echo "🔗 Render offers:"
echo "   - 750 hours/month free tier"
echo "   - Automatic SSL certificates"
echo "   - Easy PostgreSQL database setup"
