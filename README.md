# 🚀 Zentry - Gamified Project Management

A modern, gamified project management web application that motivates teams through streaks, levels, badges, and AI coaching.

![Zentry Screenshot](https://img.shields.io/badge/Status-MVP_Ready-green)
![Tech Stack](https://img.shields.io/badge/Stack-SvelteKit%20%2B%20Django-blue)

## ✨ Features

### 🎮 Gamification System
- **Level Progression**: Earn XP and level up by completing tasks
- **Streak Tracking**: Daily streaks with fire emojis and rewards
- **Badge System**: Unlock achievements for various milestones
- **Leaderboards**: Compare progress with team members

### 📋 Project Management
- **Kanban Board**: Drag-and-drop task management
- **Team Collaboration**: Assign tasks to team members
- **Project Overview**: Track progress and milestones
- **Priority System**: High, medium, low priority tasks

### 🤖 AI Coach - Zenturion
- **Smart Insights**: Personalized productivity recommendations
- **Chat Interface**: Interactive AI assistant
- **Team Analysis**: Identify team patterns and suggest improvements
- **Motivational Messages**: Keep the team engaged and motivated

### 🎨 Modern UI/UX
- **Dark Gaming Theme**: Purple and teal gradient design
- **Responsive Design**: Works on desktop and mobile
- **Smooth Animations**: Engaging user experience
- **Clean Interface**: Intuitive navigation and layout

## 🛠️ Tech Stack

### Frontend
- **SvelteKit** - Modern web framework
- **TailwindCSS v4** - Utility-first CSS framework
- **Lucide Svelte** - Beautiful icons

### Backend
- **Django REST Framework** - Python web framework
- **SQLite3** - Database (easily upgradeable to PostgreSQL)
- **Django CORS Headers** - Cross-origin resource sharing

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/lucifron28/Zentry.git
cd Zentry
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv backend_env
source backend_env/bin/activate  # On Windows: backend_env\Scripts\activate

# Install dependencies
cd backend
pip install django djangorestframework django-cors-headers

# Run migrations
python manage.py migrate

# Create initial data (demo users, tasks, badges)
python manage.py create_initial_data

# Start backend server
python manage.py runserver 8000
```

### 3. Frontend Setup
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## 🎯 Demo Accounts

The initial data includes demo accounts:

| Username | Password | Role | Level |
|----------|----------|------|-------|
| admin | admin123 | Project Manager | 1 |
| alex_dev | demo123 | Frontend Developer | 3 |
| sarah_designer | demo123 | UI/UX Designer | 4 |
| mike_backend | demo123 | Backend Developer | 5 |

## 📱 Pages & Features

### 🏠 Dashboard
- Level progress bar with XP tracking
- Current streak counter with fire animations
- Task status overview (Todo/In Progress/Done)
- Recent activity feed
- AI coach insights and quick actions

### 📋 Tasks
- Kanban-style board with three columns
- Task creation with emoji, priority, and assignment
- Progress tracking and XP rewards
- Status toggle functionality

### 👥 Team
- Dynamic leaderboards (XP, Tasks, Streaks, Level)
- Team statistics overview
- Member profiles with avatars and roles
- Achievement highlights

### 🏆 Achievements
- Badge collection with progress tracking
- Achievement categories (Tasks, Streaks, Levels, Special)
- Claimable rewards system
- Progress bars for locked badges

### 🤖 AI Coach (Zenturion)
- Interactive chat interface
- Personalized insights and recommendations
- Suggested prompts for common questions
- Team analysis and motivational advice

## 🔧 API Endpoints

### Users
- `GET /api/users/profile/` - Get current user profile
- `POST /api/users/login/` - User authentication
- `GET /api/users/leaderboard/` - Get leaderboard data

### Tasks
- `GET /api/tasks/tasks/` - List all tasks
- `POST /api/tasks/tasks/` - Create new task
- `PATCH /api/tasks/tasks/{id}/` - Update task
- `POST /api/tasks/tasks/{id}/complete/` - Complete task

### Projects
- `GET /api/tasks/projects/` - List projects
- `POST /api/tasks/projects/` - Create project

### Achievements
- `GET /api/achievements/badges/` - List all badges
- `GET /api/achievements/user-badges/` - Get user's earned badges

## 🎨 Design System

### Colors
- **Background**: `hsl(222.2 84% 4.9%)` - Dark blue-gray
- **Text**: `hsl(210 40% 98%)` - Off-white
- **Primary**: `hsl(217.2 91.2% 59.8%)` - Bright blue
- **Accent**: Purple (`#a855f7`) to Teal (`#14b8a6`) gradients

### Gradients
- **Main Background**: `bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900`
- **Logo**: `bg-gradient-to-r from-purple-500 to-teal-500`
- **Text**: `bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent`

## 🚦 Development Status

### ✅ Completed Features
- [x] Django REST API with all endpoints
- [x] User authentication and profiles
- [x] Task management with CRUD operations
- [x] Gamification system (levels, XP, streaks)
- [x] Badge and achievement system
- [x] Team leaderboards
- [x] SvelteKit frontend with all pages
- [x] Responsive design with dark theme
- [x] AI coach interface (frontend)

### 🔄 In Progress
- [ ] Real-time updates with WebSockets
- [ ] Drag-and-drop task reordering
- [ ] File attachments for tasks
- [ ] Advanced AI coach integration

### 📋 Future Enhancements
- [ ] Mobile app (React Native/Flutter)
- [ ] Discord/Slack integrations
- [ ] Advanced analytics dashboard
- [ ] Custom badge creation
- [ ] Team chat functionality
- [ ] Calendar integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SvelteKit** team for the amazing framework
- **Django** community for the robust backend
- **TailwindCSS** for the beautiful styling system
- **Heroicons** and **Lucide** for the icon libraries

## 📞 Support

If you have any questions or need help:

1. Check the [Issues](https://github.com/lucifron28/Zentry/issues) page
2. Create a new issue if your problem isn't listed
3. Join our community discussions

---

**Built with ❤️ for the developer community**

*Making project management fun, one task at a time!* 🚀
