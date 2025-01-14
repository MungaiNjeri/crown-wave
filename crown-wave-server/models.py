from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import re
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    user_role = db.Column(db.String(32), default="user", nullable=False)
    password = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)


    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3 or len(username) > 20:
            raise ValueError("Username must be between 3 and 20 characters")
        if not re.match(r"^\w+$", username):
            raise ValueError("Username must contain only letters, numbers, and underscores")
        return username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"
    
class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0)

    #Relationships
    user = db.relationship("User", backref="account", uselist=False)

    @validates("user_id")
    def validate_user_id(self, key, user_id):
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user_id. It must be a positive integer.")
        return user_id

    @validates("balance")
    def validate_balance(self, key, balance):
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        return balance

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer,db.ForeignKey("account.id"), unique=True, nullable=False)
    description = db.Column(db.String(64), unique=True, nullable=False)
    amount = db.Column(db.Integer, unique = False , nullable = False)

    def __repr__(self):
        return f"<User {self.username}"
