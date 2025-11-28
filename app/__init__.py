from flask import Flask
from .models import db
import os
import resend
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    db_password = os.getenv("DB_PASSWORD")
    database_url = f"postgresql://habits_user:{db_password}@db:5432/habits_db"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "change-me"
    resend.api_key = os.getenv("RESEND_API_KEY")

    db.init_app(app)

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
