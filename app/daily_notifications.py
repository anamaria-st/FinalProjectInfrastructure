import sys
import os
from datetime import date
import resend

# --- Fix: Add /app to Python path ---
sys.path.append('/app')

from app import create_app, db
from app.models import User, Habit

# Configurar Resend
resend.api_key = os.environ.get("RESEND_API_KEY")


# --- Obtener hábitos de hoy sin usar funciones de Flask ---
def get_habits_for_today(user):
    today = date.today()

    habits_today = []
    weekday = today.strftime("%A").lower()

    for habit in user.habits:
        # every day → siempre
        if habit.periodicity == "everyday":
            habits_today.append(habit)

        # every week → coincide con el día
        elif habit.periodicity == "every week":
            if habit.frequency.lower() == weekday:
                habits_today.append(habit)

        # every month → coincide con la semana del mes
        elif habit.periodicity == "every month":
            # semana actual del mes (1–4)
            week_of_month = (today.day - 1) // 7 + 1
            if habit.frequency.startswith(str(week_of_month)):
                habits_today.append(habit)

    return habits_today


# --- Enviar email ---
def send_habit_email(user, habits_today):
    if not user.email_notifications or not user.notification_email:
        print(f"User {user.username} has notifications disabled.")
        return

    if not habits_today:
        print(f"No habits for today for {user.username}")
        return

    body = "<h2>Your habits for today:</h2><ul>"
    for h in habits_today:
        if h.frequency:
            body += f"<li>{h.name} – {h.frequency}</li>"
        else:
            body += f"<li>{h.name}</li>"
    body += "</ul>"

    try:
        resend.Emails.send({
            "from": "My Habits <onboarding@resend.dev>",
            "to": user.notification_email,
            "subject": "Today's habits 🌱",
            "html": body
        })
        print(f"Email sent to {user.notification_email}")
    except Exception as e:
        print(f"Error sending email to {user.username}: {e}")


# --- Función principal ---
def run_daily_notifications():
    app = create_app()

    with app.app_context():
        users = User.query.all()

        for user in users:
            habits_today = get_habits_for_today(user)
            send_habit_email(user, habits_today)

    print("Daily notifications completed.")


if __name__ == "__main__":
    run_daily_notifications()
