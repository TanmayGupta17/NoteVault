# NoteVault 🔐📝

A modern, full-stack note-taking application with advanced features like automatic version history, user authentication, and real-time collaboration capabilities.

![Made with FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Made with Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![Made with TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Made with Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

## ✨ Features

### 🔐 Security & Authentication
- Secure JWT-based authentication
- Argon2 password hashing
- Protected API endpoints
- Token-based session management

### 📝 Note Management
- Create, read, update, and delete notes
- Rich text content support
- Real-time search and filtering
- User-specific note isolation

### 🕐 Version History
- Automatic version snapshots on every edit
- View complete version timeline
- Restore notes to any previous version
- Track who made which changes

### 🎨 Modern UI/UX
- Clean, responsive design
- Tailwind CSS styling
- Smooth animations and transitions
- Mobile-friendly interface

### 🚀 Coming Soon
- Multi-user collaboration
- Activity logs
- Rich text editor
- Note categories and tags
- Dark mode

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Powerful ORM for database operations
- **PostgreSQL/SQLite** - Flexible database options
- **Pydantic** - Data validation and serialization
- **Python-JOSE** - JWT token handling
- **Passlib** - Secure password hashing (Argon2)

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - Promise-based HTTP client
- **Context API** - State management

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/TanmayGupta17/NoteVault.git
cd NoteVault
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[argon2] python-multipart python-dotenv psycopg2-binary
```

4. **Create `.env` file in root directory**
```env
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./notevault.db
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **Run the backend server**
```bash
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create `.env.local` file**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Run development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 🚀 Production Deployment

### Environment Variables (Production)

**Backend (.env)**
```env
SECRET_KEY=<strong-random-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### Backend Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Deployment
```bash
npm run build
npm run start
```

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /register` - Register new user
- `POST /login` - Login and get JWT token

#### Notes
- `GET /note` - Get all user notes
- `POST /note` - Create new note
- `PUT /note/{note_id}` - Update note
- `DELETE /note/{note_id}` - Delete note

#### Version History
- `GET /note/{note_id}/versions` - List all versions
- `GET /note/{note_id}/versions/{version_number}` - Get specific version
- `POST /note/{note_id}/restore/{version_number}` - Restore to version

## 🏗️ Project Structure

```
NoteVault/
├── 📁 backend (root)
│   ├── main.py              # FastAPI application & routes
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── auth.py              # Authentication & JWT logic
│   ├── database.py          # Database configuration
│   ├── .env                 # Environment variables (gitignored)
│   └── requirements.txt     # Python dependencies
│
└── 📁 frontend/
    ├── 📁 app/
    │   ├── page.tsx                    # Login/Register page
    │   ├── layout.tsx                  # Root layout
    │   ├── 📁 dashboard/
    │   │   └── page.tsx                # Notes dashboard
    │   └── 📁 notes/[id]/
    │       └── page.tsx                # Note detail & edit
    ├── 📁 contexts/
    │   └── AuthContext.tsx             # Auth state management
    ├── 📁 lib/
    │   └── api.ts                      # API client
    ├── .env.local                      # Frontend env (gitignored)
    ├── package.json
    └── tsconfig.json
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Tanmay Gupta**
- GitHub: [@TanmayGupta17](https://github.com/TanmayGupta17)

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- Next.js team for the powerful React framework
- Vercel for hosting and deployment solutions

---

⭐ Star this repo if you find it helpful!
