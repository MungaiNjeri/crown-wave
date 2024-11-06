import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail, Message

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["SECRET_KEY"] = (
    "SECRET_KEY"  # Necessary for session management with Flask-Login
)

# Flask-Mail Configuration
app.config["MAIL_SERVER"] = (
    "smtp.gmail.com"  # Replace with your mail server (e.g., Gmail's SMTP server)
)
app.config["MAIL_PORT"] = 587  # TLS port (for Gmail)
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = (
    "maria123mungai@gmail.com"  # Store this in your environment variables
)
app.config["MAIL_PASSWORD"] = (
    "mupd asww alcl nqkg"  # Store this in your environment variables
)
app.config["MAIL_DEFAULT_SENDER"] = (
    "CrownWave",
    "maria123mungai@gmail.com",
)  # Optional
app.config["RESET_TOKEN_EXPIRATION"] = 3600
# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = (
    "login"  # Redirect to login page if user is not authenticated
)
