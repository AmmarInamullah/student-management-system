# 📚 Student Management System

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![SQLite](https://img.shields.io/badge/SQLite-3-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive, production-ready **Student Management System** for schools, colleges, and educational institutions. Built with Django, this system provides separate dashboards for Students, Teachers, and Administrators.

## 🚀 Live Demo

*Demo coming soon*

## 📸 Screenshots

### 🔐 Login Page
![Login Page](screenshots/login-page.png)

### 👑 Admin Dashboard
![Admin Dashboard](screenshots/admin-dashboard.png)

### 👨‍🏫 Teacher Dashboard
![Teacher Dashboard](screenshots/teacher-dashboard.png)

### 👨‍🎓 Student Dashboard
![Student Dashboard](screenshots/student-dashboard.png)

### 📝 Create Assignment
![Create Assignment](screenshots/create-assignment.png)

### 📊 Grades View
![Grades View](screenshots/grades-view.png)

### 💰 Salary Management
![Salary Management](screenshots/salary-management.png)

## ✨ Features

### 👑 Administrator Features
- Complete dashboard with real-time statistics
- Manage students (Add/Edit/Delete)
- Manage teachers (Add/Edit/Delete)
- Process teacher salary payments
- Generate reports (PDF/Excel)
- View all system data

### 👨‍🏫 Teacher Features
- View students by subject
- Create and manage assignments
- Upload grades with automatic GPA calculation
- View salary history and payment status
- Mark daily attendance
- Track pending grades

### 👨‍🎓 Student Features
- View enrolled subjects
- Check grades with letter grades (A-F)
- Calculate and view GPA
- Track attendance percentage
- View pending assignments
- Download grade reports

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Backend | Django 4.2 |
| Frontend | Bootstrap 5, HTML5, CSS3 |
| Database | SQLite3 / PostgreSQL |
| Authentication | Django Auth System |
| Icons | Font Awesome 6 |
| Charts | Chart.js |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional)

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/AmmarInamullah/student-management-system.git
cd student-management-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
python manage.py migrate

# 6. Create superuser (admin account)
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver

# 8. Open your browser and go to:
# http://127.0.0.1:8000/
