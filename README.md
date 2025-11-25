📘 README – Mini Habits App (Final Project, Modern Infrastructure)
1. Overview

Mini Habits is a lightweight habit-tracking web application developed as the final project for the Modern Infrastructure course.
It demonstrates the integration of containerized services, scheduled background tasks, automated email notifications, persistent storage, and CI/CD workflows while maintaining a clean and user-friendly design.

The system allows users to:

Register and authenticate securely

Create, edit, and categorize habits

Track daily, weekly, and monthly routines

Visualize habits on a calendar

Mark habits as completed

Receive automated daily email reminders

Deploy the full application using Docker and Render

2. System Architecture
2.1 Technologies
Component	Technology
Backend	Python 3.12, Flask
Database	SQLite (SQLAlchemy ORM)
Frontend	HTML5, CSS3, Jinja2
Email Service	Resend API
Scheduling	Cron inside Docker
Containerization	Docker & Docker Compose
Deployment	Render (Docker)
3. Features
3.1 User Authentication

Registration with password confirmation

Login using secure password hashing (Werkzeug)

Prevention of duplicate usernames

Optional email registration for notifications

3.2 Dashboard

Four habit categories: Physical, Mental, Social, Hobbies

Visual cards representing each category

List of user-specific habits per category

3.3 Habit Management

Each habit includes:

Title/description

Category

Periodicity:

Every day

Every week (weekday selector)

Every month (week of month selector)

Dynamic frequency UI selector based on periodicity

Editing and deletion options

3.4 Calendar Module

Monthly calendar automatically generated

Each day displays color-coded dot indicators for habits due that day

Right-side panel lists all habits scheduled for the current day

Habits can be marked as completed directly from the calendar

Visual legend explaining color codes

Scrollable layout for long lists

3.5 Email Notification System

Daily notification containing that day’s habits

Implemented via:

A Python worker (daily_notifications.py)

Cron executing inside the container

Resend API for sending transactional emails

Optional toggle in the interface to enable/disable notifications

3.6 CI/CD

GitHub Actions pipeline includes:

Dependency installation

Tests via pytest

Docker image build

Render automatically redeploys on changes to the main branch

4. Project Structure
FinalProjectInfrastructure/
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
├── pytest.ini
├── tests/
└── README.md

5. Deployment Instructions
5.1 Local Execution (Docker)
1. Clone the repository:
git clone <repository_url>
cd FinalProjectInfrastructure

2. Create an .env file:
RESEND_API_KEY=re_xxxxxxxxxxxxx

3. Build and run:
docker compose up --build


The application will be available at:

http://localhost:5000

5.2 Deployment on Render

Create a new Web Service

Select Deploy from Dockerfile

Add environment variable:

RESEND_API_KEY

Connect the GitHub repository

Render triggers automatic deployments on push

6. Cron-Based Email Notifications
Cronjob File (cronjob):
RESEND_API_KEY=re_xxxxxxxxxxxx
00 05 * * * /usr/local/bin/python /app/app/daily_notifications.py >> /var/log/cron.log 2>&1

Execution Flow

The container starts cron in foreground (cron -f)

Cron loads the job file and executes the script at the scheduled hour

The script:

Creates an app context

Queries user habits

Sends email reminders using Resend

Output is logged at /var/log/cron.log

7. Testing

Run all tests:

pytest -v


Included tests validate:

Registration

Login

Duplicate user handling

Habit creation

Dashboard and routes

8. Security Considerations

Passwords hashed using Werkzeug

API keys stored in environment variables

Cronjob explicitly loads required variables

No secrets stored in the codebase

Form validation both client and server side

9. Limitations and Future Work

SQLite used for simplicity; production should support PostgreSQL

Email frequency is fixed (daily)

UI could be extended for mobile optimization

Potential for analytics and habit streaks

10. Author

Ana María Alvarez
Óbuda University
Computer Science MSc Student
Modern Infrastructure — Final Project (2025)