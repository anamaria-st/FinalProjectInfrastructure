# 🌱 Mini habits — Final Project (Modern Infrastructure)

## 1. Overview
Mini habits is a lightweight habit-tracking web application built as the final project for the *Modern Infrastructure* course at Óbuda University.  
The system demonstrates modern software deployment strategies including containerization, cron-based background jobs, automated email notifications, CI/CD pipelines, and a fully functioning Flask web application.

The app provides:
- User registration and authentication  
- A dashboard for managing habits across multiple categories  
- Creation, editing, and deletion of daily, weekly, and monthly habits  
- A visual calendar with category-based color coding  
- Completion tracking for each day  
- Automated daily email notifications using Resend  
- Full Dockerization and deployment to Render  

---

## 2. System Architecture

### Technologies Used
| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, Flask |
| Frontend | HTML, CSS, Jinja2 |
| Database | SQLite (SQLAlchemy ORM) |
| Notifications | Resend API |
| Scheduling | Linux Cron inside Docker |
| Deployment | Docker & Docker Compose |
| CI/CD | GitHub Actions |
| Hosting | Render (Docker Deployment) |

### High-Level Architecture
```
Client  →  Flask Application  →  SQLite Database
                 ↑
                 |
           Cron + Resend
         (Email Scheduler)
```

---

## 3. Application Features

### 3.1 Authentication
- User registration with password confirmation  
- Secure login using hashed passwords (Werkzeug)  
- Prevention of duplicate usernames  
- Optional email entry for notifications  

### 3.2 Habits Dashboard
- Four categories: Physical Health, Mental, Social, Hobbies  
- Visual cards representing each category  
- List of all habits per category  

### 3.3 Habit Management
Each habit includes:
- Description  
- Category  
- Periodicity:
  - Every day  
  - Every week (weekday selector)  
  - Every month (week-of-month selector)  
- Dynamic frequency selector (UI updates automatically)  
- Editing and deletion capabilities  

### 3.4 Calendar View
- Automatically generated monthly calendar  
- Color-coded dots for each category  
- Today’s habits listed on the right side  
- Checkbox system to mark habits as completed  
- Scrollable layout for many habits  
- Category legend included for clarity  

### 3.5 Email Notifications
- Automated daily emails summarizing that day's habits  
- Sent using Resend API  
- Implemented through a cron-scheduled Python script  
- Users can enable/disable notifications in the UI  

---

## 4. Project Structure
```
/FinalProjectInfrastructure
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── daily_notifications.py
│   ├── templates/
│   └── static/
│
├── Dockerfile
├── docker-compose.yml
├── cronjob
├── requirements.txt
├── tests/
│   └── test_app.py
└── README.md
```

---

## 5. Running the Application Locally (Docker)

### 5.1 Clone the Repository
```
git clone <repository_url>
cd FinalProjectInfrastructure
```

### 5.2 Create a `.env` File
```
RESEND_API_KEY=re_xxxxxxxxxxxxx
```

### 5.3 Start Containers
```
docker compose up --build
```
The application is available at:
```
http://localhost:5000
```

---

## 6. Deployment (Render)

1. Create a new **Web Service**  
2. Select **Deploy from Dockerfile**  
3. Add an environment variable:
```
RESEND_API_KEY=re_xxxxxx
```
4. Connect GitHub repository  
5. Deployment triggers automatically on pushes to `main`  

---

## 7. Cron-Based Email Scheduler

### Cronjob File
```
RESEND_API_KEY=re_xxxxxxxxxxxxx
10 07 * * * /usr/local/bin/python /app/app/daily_notifications.py >> /var/log/cron.log 2>&1
```

### Execution Flow
1. Docker container launches `cron -f`  
2. Cron executes `daily_notifications.py` at the scheduled hour  
3. Script loads user habits, builds an email, and sends via Resend  
4. Logs are stored in `/var/log/cron.log`  

---

## 8. Testing
Run all tests:
```
pytest -v
```

Tests include:
- Registration  
- Login  
- Habit creation  
- Dashboard loading  
- Basic model validation  

---

## 9. Security Considerations
- Passwords hashed with Werkzeug  
- Secrets stored in environment variables  
- Cron explicitly loads environment before execution  
- Input validation in forms  
- No hard-coded credentials  

---

## 10. Future Improvements
- Replace SQLite with PostgreSQL (production-ready)  
- Add mobile-responsive UI  
- Streak tracking and analytics  
- Push notifications  
- Multi-language support  

---

## 11. Author
**Ana María**  
Óbuda University  
Modern Infrastructure — Final Project (2025)

---

## 12. License
MIT License
