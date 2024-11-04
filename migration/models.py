
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from migration.config import db
from flask_login import UserMixin
import enum

class MembershipLevel(enum.Enum):
    BASIC = "basic"
    PLATINUM = "platinum"
    GOLD = "gold"

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.String(150), nullable=True, 
                            default='https://imgv3.fotor.com/images/blog-richtext-image/10-profile-picture-ideas-to-make-you-stand-out.jpg')
    balance = db.Column(db.Float, default=0.0)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=True)
    membership_level = db.Column(db.Enum(MembershipLevel), default=MembershipLevel.BASIC)  # Enum for membership levels
    
    # Relationships
    packages = db.relationship('Package', backref='user', lazy=True)
    referrals = db.relationship('Link', backref='referrer', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link_url = db.Column(db.String(200), unique=True, nullable=False)
    referral_count = db.Column(db.Integer, default=0)  # Track successful sign-ups

    def to_dict(self):
        return {
            "id": self.id,
            "link_url": self.link_url,
            "referral_count": self.referral_count
        }

class Transaction(db.Model):
    __tablename__ = 'transaction'  # Corrected to double underscores
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=True)

    # Establish relationship to User
    user = db.relationship('User', backref='transactions', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.sender_id} -> {self.receiver_id} ({self.amount})>'
    
class Package(db.Model):
    _tablename_ = 'package'  # Optional but good practice to define
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    reward = db.Column(db.Float, nullable=False)

    #relationships
    transactions = db.relationship('Transaction', backref='package', lazy=True) 

   
class AccountBalance(db.Model):
    _tablename_ = 'account_balance'  # Optional but good practice to define
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    whatsapp_balance = db.Column(db.Float, default=0.0)
    cashback_balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<Package {self.name} ({self.price})>'
    