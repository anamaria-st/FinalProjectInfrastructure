from flask import Flask
from .models import db
import os
import resend

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-me-in-production"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
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
