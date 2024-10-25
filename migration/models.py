from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


db = SQLAlchemy()

class User(db.Model):
    _tablename_ = 'user'  # Optional but good practice to define
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=True)

    #relatioships
    packages = db.relationship('Package', backref='user', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    

class Transaction(db.Model):
    _tablename_ = 'transaction'  # Optional but good practice to define
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=True)

    #relationships
    User = db.relationship('User',backref='transactions')
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

    def __repr__(self):
        return f'<Package {self.name} ({self.price})>'
    