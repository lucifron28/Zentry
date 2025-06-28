#!/bin/bash

# Setup script for Render environment variables

echo "🔧 Environment Variables for Render Dashboard"
echo "=============================================="
echo ""
echo "📝 Add these in your Render service Environment tab:"
echo ""

# Generate a new secret key
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

echo "SECRET_KEY=${SECRET_KEY}"
echo "DEBUG=False"
echo "ALLOWED_HOSTS=localhost,127.0.0.1,*.onrender.com,zentry-oyyo.onrender.com"
echo "CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app"
echo ""
echo "📍 Your backend is deployed at: https://zentry-oyyo.onrender.com"
echo ""
echo "🔄 After setting these variables:"
echo "1. Go to your Render dashboard"
echo "2. Navigate to your 'zentry-oyyo' service"  
echo "3. Click on 'Environment' tab"
echo "4. Add each variable above"
echo "5. Click 'Manual Deploy' to redeploy with new settings"
echo ""
echo "🌐 Then update your frontend environment variable:"
echo "   VITE_API_BASE_URL=https://zentry-oyyo.onrender.com"
