# 📝 TODO Application

A minimalist, distraction-free TODO application built with FastAPI and Svelte.

## 🎯 Features

- ✅ Add, edit, and delete tasks
- ✅ Mark tasks as complete/incomplete  
- ✅ Persistent storage with SQLite
- ✅ Clean, minimalist UI with dark/light themes
- ✅ Responsive design for all devices
- ✅ Kubernetes-ready deployment

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLite (database)
- Pydantic (data validation)

**Frontend:**
- Svelte/SvelteKit (reactive framework)
- Vanilla CSS (no frameworks)
- Modern ES6+ JavaScript

**Deployment:**
- Docker containers
- Kubernetes manifests
- ArgoCD for GitOps

## 🚀 Quick Start

### Development

1. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The application will be available at `http://localhost:5173` with the API at `http://localhost:8000`.

### Production Deployment

1. **Build Docker Images:**
   ```bash
   # Backend
   cd backend
   docker build -t todo-backend:latest .
   
   # Frontend  
   cd frontend
   docker build -t todo-frontend:latest .
   ```

2. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f k8s/
   ```

3. **ArgoCD Deployment:**
   ```bash
   kubectl apply -f k8s/argocd-application.yaml
   ```

## 📁 Project Structure

```
TODO_APP/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── database/       # Database connection
│   │   └── models/         # Pydantic models
│   ├── tests/              # Backend tests
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # Svelte frontend
│   ├── src/
│   │   ├── components/     # Svelte components
│   │   ├── routes/         # SvelteKit routes
│   │   ├── stores/         # State management
│   │   └── lib/           # Utilities
│   ├── static/            # Static assets
│   ├── package.json       # Node dependencies
│   └── Dockerfile        # Frontend container
├── k8s/                   # Kubernetes manifests
├── COPILOT_MVP.md        # Requirements document
└── README.md            # This file
```

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create new task |
| PUT | `/api/tasks/{id}` | Update task |
| PUT | `/api/tasks/{id}/complete` | Mark task complete |
| PUT | `/api/tasks/{id}/reopen` | Reopen completed task |
| DELETE | `/api/tasks/{id}` | Delete task |
| GET | `/health` | Health check |

## 🎨 Design Principles

- **Minimalist**: No clutter, animations, or distractions
- **Fast**: Optimized for performance and quick interactions
- **Accessible**: Keyboard navigation and screen reader friendly
- **Responsive**: Works on all device sizes
- **Privacy-First**: No tracking, analytics, or external dependencies

## 📊 Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(title) > 0 AND length(title) <= 200),
    description TEXT CHECK(description IS NULL OR length(description) <= 1000),
    status TEXT NOT NULL CHECK(status IN ('pending', 'completed')) DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### Environment Variables

**Backend:**
- `DATABASE_PATH`: Path to SQLite database file (default: `/app/data/todo.db`)
- `CORS_ORIGINS`: Allowed CORS origins (default: `*`)

### Kubernetes Configuration

- **Storage**: 1GB PVC for SQLite database
- **Resources**: Configured resource limits for both containers
- **Health Checks**: Liveness and readiness probes
- **LoadBalancer**: MetalLB service for external access

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend  
npm test
```

## 📄 License

This project is open source. See the requirements document for full feature specifications.

## 🤝 Contributing

1. Review the requirements in `COPILOT_MVP.md`
2. Follow the existing code style and patterns
3. Add tests for new features
4. Update documentation as needed

---

Built with ❤️ for simplicity and productivity.