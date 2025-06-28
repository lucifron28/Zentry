# Zentry Backend Deployment Guide

This guide covers deployment options for the Zentry Django backend with free and paid hosting alternatives.

## 🌟 Deployment Options

### Option 1: Railway (Recommended - Paid)
Railway offers excellent Django support with PostgreSQL, but requires a paid plan.

**Pros:**
- Excellent Django/PostgreSQL support
- Easy environment variable management
- Automatic deployments from Git
- Built-in metrics and logging

**Cons:**
- No free tier (trial expired)
- Requires payment after trial

### Option 2: Render (Free Tier Available)
Render provides a generous free tier perfect for development and small projects.

**Pros:**
- 750 hours/month free tier
- Automatic SSL certificates
- PostgreSQL database included
- Git-based deployments

**Cons:**
- Free tier has some limitations
- Spins down after inactivity

### Option 3: Railway (Alternative Setup)
If you get Railway access, this is still the preferred option.

## 🚀 Quick Deployment

### For Render (Free)

1. **Run the setup script:**
   ```bash
   cd backend
   ./deploy-render.sh
   ```

2. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

3. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Create account and connect GitHub
   - Create "New Web Service"
   - Select your repository
   - Render will detect the `render.yaml` configuration automatically

4. **Manual Render Setup** (if render.yaml doesn't work):
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn zentry_backend.wsgi:application`
   - Add environment variables (see below)

### For Railway (Paid)

1. **Ensure Railway CLI is linked:**
   ```bash
   cd backend
   railway status
   ```

2. **Deploy:**
   ```bash
   ./deploy-railway.sh
   ```

## ⚙️ Environment Variables

Set these environment variables in your hosting platform:

### Required Variables
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.your-host.com
DATABASE_URL=postgresql://...  # Auto-provided by host
```

### CORS Configuration
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Optional Variables
```bash
# Email settings (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Discord webhook (optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Teams webhook (optional)
TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/...
```

## 🔧 Manual Environment Variable Setup

### For Render:
1. Go to your service dashboard
2. Navigate to "Environment" tab
3. Add each variable with its value

### For Railway:
```bash
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS="*.railway.app"
railway variables set CORS_ALLOWED_ORIGINS="https://your-frontend.vercel.app"
```

## 📦 Database Setup

### Render:
- Create a PostgreSQL database service
- Link it to your web service
- DATABASE_URL is automatically provided

### Railway:
- Add PostgreSQL plugin to your project
- DATABASE_URL is automatically injected

## 🔍 Verification

After deployment, verify your backend is working:

1. **Health check:**
   ```bash
   curl https://your-backend-url.com/admin/
   ```

2. **API endpoints:**
   ```bash
   curl https://your-backend-url.com/api/tasks/
   ```

3. **Check logs:**
   - Render: View logs in dashboard
   - Railway: `railway logs`

## 🔄 Connecting Frontend

After backend deployment:

1. **Note your backend URL** (e.g., `https://zentry-backend.onrender.com`)

2. **Update frontend environment variable** in Vercel:
   ```bash
   # In Vercel dashboard or via CLI
   vercel env add VITE_API_BASE_URL production
   # Enter: https://your-backend-url.com
   ```

3. **Update CORS settings** on backend:
   - Add your Vercel URL to `CORS_ALLOWED_ORIGINS`
   - Redeploy backend if needed

## 🏃‍♂️ Next Steps

1. Deploy backend using preferred method
2. Update frontend environment variables
3. Test full stack integration
4. Set up webhooks for Discord/Teams
5. Configure domain names (optional)

## 🆘 Troubleshooting

### Common Issues:

1. **Static files not loading:**
   - Check `STATIC_ROOT` and `STATIC_URL` settings
   - Ensure `collectstatic` runs during deployment

2. **Database connection errors:**
   - Verify `DATABASE_URL` is set correctly
   - Check if migrations ran successfully

3. **CORS errors:**
   - Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`
   - Check `ALLOWED_HOSTS` includes your domain

4. **502/503 errors:**
   - Check application logs
   - Verify Gunicorn is starting correctly
   - Ensure all dependencies are installed

### Useful Commands:

```bash
# View deployment logs
railway logs              # Railway
# Check logs in Render dashboard

# Check environment variables
railway variables         # Railway
# Check in Render dashboard under Environment tab

# Local testing
python manage.py runserver
python manage.py check --deploy
```

## 🔗 Resources

- [Render Django Tutorial](https://render.com/docs/deploy-django)
- [Railway Django Guide](https://docs.railway.app/guides/django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
