# 🎓 Aursikho — Online Course Enrollment System

An online course enrollment platform built with **Python Flask** that enables instructors to create courses with video lessons and quizzes, while students can enroll, learn, and earn verifiable certificates upon completion.

> Built as a semester-end project for Python Web Development.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Authentication** | Register/Login with roles: Student, Instructor, Admin |
| 📚 **Course Management** | Instructors create courses with lessons & MCQ quizzes |
| 🎥 **YouTube Integration** | Embed YouTube video lessons directly in the platform |
| 🎓 **Enrollment System** | Students browse, search, filter, and enroll in courses |
| 📊 **Progress Tracking** | Per-lesson completion tracking with progress bars |
| 📝 **Quiz System** | MCQ quizzes with auto-grading and pass/fail |
| 🏆 **Certificate Generation** | Auto-generated PNG certificates using Pillow |
| ✅ **Certificate Verification** | Public verification page with unique certificate UID |
| 👨‍💼 **Admin Panel** | Manage users, courses, and platform statistics |
| 📱 **Responsive Design** | Bootstrap 5 for mobile-friendly layouts |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.9+, Flask 3.x |
| Database | SQLite (via Flask-SQLAlchemy) |
| Authentication | Flask-Login + Werkzeug |
| Frontend | Jinja2 + Bootstrap 5 + Custom CSS |
| Certificate Gen | Pillow (PIL) |
| Forms | Flask-WTF (CSRF protection) |
| Migrations | Flask-Migrate (Alembic) |

---

## 📁 Project Structure

```
OCESdemu/
├── app/
│   ├── __init__.py              # App factory, extensions
│   ├── config.py                # Configuration
│   ├── models.py                # Database models (9 models)
│   ├── forms.py                 # WTForms definitions
│   ├── routes/                  # Blueprints
│   │   ├── auth.py              # Login, Register, Logout
│   │   ├── main.py              # Home, Browse, About
│   │   ├── courses.py           # Enrollment, Lessons, Quizzes
│   │   ├── student.py           # Student dashboard
│   │   ├── instructor.py        # Course CRUD
│   │   ├── admin.py             # Admin panel
│   │   └── certificate.py       # Certificate generation
│   ├── templates/               # Jinja2 HTML templates
│   ├── static/                  # CSS, JS, certificates
│   └── utils/
│       ├── decorators.py        # Role-based access control
│       └── certificate_generator.py
├── requirements.txt
├── run.py                       # Entry point
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OCESdemu
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS/Linux
   # venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

### Default Admin Account
- **Email:** admin@aursikho.com
- **Password:** admin123

---

## 📊 Database Schema (ERD)

The application uses **9 database models** with proper relationships:

- **User** — Supports student, instructor, admin roles
- **Course** — Title, description, category, difficulty, publish status
- **Lesson** — Video (YouTube embed) or text content
- **Quiz** — Associated with a course, configurable passing score
- **QuizQuestion** — MCQ with 4 options (A/B/C/D)
- **Enrollment** — Links students to courses (many-to-many)
- **LessonProgress** — Tracks individual lesson completion
- **QuizAttempt** — Records quiz scores and pass/fail
- **Certificate** — Generated with unique UUID for verification

---

## 👥 User Roles

| Role | Capabilities |
|---|---|
| **Student** | Browse courses, enroll, watch lessons, take quizzes, earn certificates |
| **Instructor** | Create/edit/delete courses, add lessons & quizzes, view enrolled students |
| **Admin** | Manage all users, change roles, view platform stats, oversee courses |

---

## 🏆 Certificate System

1. Student completes all lessons in a course
2. Student passes the course quiz (if one exists)
3. Student generates a certificate from the course page
4. Certificate is created as a PNG image using **Pillow**
5. Each certificate has a **unique UUID** for verification
6. Anyone can verify a certificate at `/verify/<certificate-uid>`

---

## 🧪 Testing the Application

### Quick Test Flow
1. Register as an **Instructor** → Create a course → Add lessons → Add quiz → Publish
2. Register as a **Student** → Browse → Enroll → Complete lessons → Pass quiz → Get certificate
3. Login as **Admin** (admin@aursikho.com) → View platform stats → Manage users

---

## 📝 License

This project was built for educational purposes as a semester-end project.

---

## 👨‍💻 Team

Built with ❤️ using Python & Flask
