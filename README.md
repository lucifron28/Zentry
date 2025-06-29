# Zentry Backend

Django REST API backend for Zentry project management application.

## 🚀 Quick Deploy to Render

This branch is optimized for Render deployment with Django backend as root.

### Deployment Configuration

- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: SQLite (production-ready for small to medium apps)
- **Static Files**: WhiteNoise for serving static files
- **CORS**: Configured for frontend integration

### Auto-Deploy Setup

1. **Connect Repository**: Link this `render-deploy` branch to Render
2. **Service Type**: Web Service
3. **Build Command**: `./build.sh`
4. **Start Command**: `gunicorn zentry_backend.wsgi:application --bind 0.0.0.0:$PORT`

### Environment Variables

Set these in Render dashboard:

```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=*
CORS_ALLOW_ALL_ORIGINS=True
```

### Features

- 📋 **Task Management**: Create, assign, and track project tasks
- 👥 **User Management**: User profiles and team collaboration
- 🏆 **Achievements**: Badge system for gamification
- 🔔 **Notifications**: Webhook integrations (Discord, Teams)
- 📊 **Analytics**: Task completion stats and project insights

### API Endpoints

- `/admin/` - Django admin interface
- `/api/tasks/` - Task and project management
- `/api/users/` - User profiles and authentication
- `/api/achievements/` - Badge and achievement system
- `/api/notifications/` - Webhook integrations

### Local Development

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Deployment Status

- ✅ SQLite database configured
- ✅ Static files handling with WhiteNoise
- ✅ CORS configured for frontend
- ✅ Production settings optimized
- ✅ Automatic superuser creation (`admin`/`admin123`)

---

**Backend URL**: `https://your-app.onrender.com`  
**Admin Login**: `admin` / `admin123`
