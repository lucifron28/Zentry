#!/bin/bash

# Railway Deployment Script for Zentry Backend
set -e

echo "🚀 Deploying Zentry Backend to Railway..."

# Ensure we're in the backend directory
cd "$(dirname "$0")"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Check if we're linked to a Railway project
if ! railway status &> /dev/null; then
    echo "❌ Not linked to a Railway project. Please run 'railway link' first."
    exit 1
fi

echo "📋 Current Railway project status:"
railway status

# Set required environment variables
echo "🔧 Setting environment variables..."

# Generate a secure secret key if not provided
SECRET_KEY=${SECRET_KEY:-$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')}

railway variables set SECRET_KEY="$SECRET_KEY"
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS="*.railway.app"
railway variables set DATABASE_URL='${{Postgres.DATABASE_URL}}'

# Frontend URL (update this after Vercel deployment)
FRONTEND_URL=${FRONTEND_URL:-"https://your-frontend.vercel.app"}
railway variables set CORS_ALLOWED_ORIGINS="$FRONTEND_URL"

echo "✅ Environment variables set successfully!"

# Display current variables
echo "📊 Current environment variables:"
railway variables

# Deploy the application
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment completed!"
echo "🌐 Your backend will be available at: https://your-service.railway.app"
echo ""
echo "📝 Next steps:"
echo "1. Note down your backend URL from Railway dashboard"
echo "2. Update VITE_API_BASE_URL in Vercel to point to your Railway backend"
echo "3. Update CORS_ALLOWED_ORIGINS with your Vercel frontend URL"
echo ""
echo "🔗 Useful commands:"
echo "  railway logs        - View application logs"
echo "  railway status      - Check deployment status"
echo "  railway variables   - View/manage environment variables"
