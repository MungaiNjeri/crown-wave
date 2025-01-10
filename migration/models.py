from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
import enum
from migration.config import db

class MembershipLevel(enum.Enum):
    BASIC = "basic"
    PLATINUM = "platinum"
    GOLD = "gold"

class User(db.Model, UserMixin):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.String(150), nullable=True, default="https://imgv3.fotor.com/images/blog-richtext-image/10-profile-picture-ideas-to-make-you-stand-out.jpg")
    balance = db.Column(db.Float, default=0.0)
    package_id = db.Column(db.Integer, db.ForeignKey("package.id"), nullable=True)
    membership_level = db.Column(db.Enum(MembershipLevel), default=MembershipLevel.BASIC)

    # Relationships
    packages = db.relationship("Package", backref="user", lazy=True)
    referrals = db.relationship("Link", backref="referrer", lazy=True)
    transactions = db.relationship("Transaction", backref="user", lazy=True)
    account_balance = db.relationship("AccountBalance", backref="user", uselist=False)

    def __repr__(self):
        return f"<User {self.username}>"

class AccountBalance(db.Model):
    __tablename__ = "account_balance"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    whatsapp_balance = db.Column(db.Float, default=0.0)
    cashback_balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<AccountBalance user_id={self.user_id}>"

class Link(db.Model):
    __tablename__ = "link"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    link_url = db.Column(db.String(200), unique=True, nullable=False)
    referral_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "link_url": self.link_url,
            "referral_count": self.referral_count,
        }

class Transaction(db.Model):
    __tablename__ = "transaction"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey("package.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Transaction {self.user_id} -> {self.recipient} ({self.amount})>"

class Package(db.Model):
    __tablename__ = "package"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    reward = db.Column(db.Float, nullable=False)

    # Relationships
    transactions = db.relationship("Transaction", backref="package", lazy=True)

class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0)

    #Relationships
    user = db.relationship("User", backref="account", uselist=False)


