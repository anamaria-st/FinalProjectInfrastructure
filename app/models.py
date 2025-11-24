from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Login
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Email notifications
    notification_email = db.Column(db.String(120))
    email_notifications = db.Column(db.Boolean, default=False)

    # Relationship
    habits = db.relationship("Habit", backref="user", lazy=True)

    # Password utils
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)



class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # physical / mental / social / hobbies
    category = db.Column(db.String(20), nullable=False)

    # descripción del hábito
    name = db.Column(db.String(255), nullable=False)

    # ejemplo: "every week", "every month", "everyday"
    periodicity = db.Column(db.String(50), nullable=False)

    # ejemplo: "Monday", "3rd week", "7pm", "8am"
    frequency = db.Column(db.String(50), nullable=False)
    completions = db.relationship(
        "HabitCompletion",
        backref="habit",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

class HabitCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'))
    date = db.Column(db.Date, nullable=False)

