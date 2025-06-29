#!/bin/bash

# Test script for deployed Zentry backend

echo "🧪 Testing Zentry Backend Deployment"
echo "====================================="

# Update this URL after deploying to Render
BACKEND_URL="https://your-app.onrender.com"

echo "📍 Testing backend: $BACKEND_URL"
echo ""

echo "1️⃣ Testing admin login page..."
ADMIN_RESPONSE=$(curl -s -w "%{http_code}" "$BACKEND_URL/admin/" -o /dev/null)
if [ "$ADMIN_RESPONSE" = "200" ]; then
    echo "✅ Admin page accessible (HTTP $ADMIN_RESPONSE)"
    echo "   Login with: admin / admin123"
else
    echo "❌ Admin page failed (HTTP $ADMIN_RESPONSE)"
fi

echo ""
echo "2️⃣ Testing API endpoints..."

# Test projects endpoint
echo "📋 Testing projects API..."
PROJECTS_RESPONSE=$(curl -s "$BACKEND_URL/api/tasks/projects/" | head -c 100)
if echo "$PROJECTS_RESPONSE" | grep -q "Authentication credentials"; then
    echo "✅ Projects API responding (requires auth as expected)"
elif echo "$PROJECTS_RESPONSE" | grep -q "results"; then
    echo "✅ Projects API responding with data"
else
    echo "❌ Projects API failed"
    echo "Response: $PROJECTS_RESPONSE"
fi

# Test users endpoint  
echo "👥 Testing users API..."
USERS_RESPONSE=$(curl -s "$BACKEND_URL/api/users/users/" | head -c 100)
if echo "$USERS_RESPONSE" | grep -q "Authentication credentials"; then
    echo "✅ Users API responding (requires auth as expected)"
elif echo "$USERS_RESPONSE" | grep -q "results"; then
    echo "✅ Users API responding with data"
else
    echo "❌ Users API failed"
    echo "Response: $USERS_RESPONSE"
fi

# Test notifications endpoint
echo "🔔 Testing notifications API..."
NOTIF_RESPONSE=$(curl -s "$BACKEND_URL/api/notifications/webhook-integrations/" | head -c 100)
if echo "$NOTIF_RESPONSE" | grep -q "Authentication credentials"; then
    echo "✅ Notifications API responding (requires auth as expected)"
elif echo "$NOTIF_RESPONSE" | grep -q "results"; then
    echo "✅ Notifications API responding with data"
else
    echo "❌ Notifications API failed"
    echo "Response: $NOTIF_RESPONSE"
fi

echo ""
echo "🎉 Backend testing completed!"
echo ""
echo "📝 Next steps:"
echo "1. Update frontend VITE_API_BASE_URL to: $BACKEND_URL"
echo "2. Test full integration with Vercel frontend"
echo "3. Configure webhook integrations via admin panel"
echo "4. Set up proper SECRET_KEY in production"