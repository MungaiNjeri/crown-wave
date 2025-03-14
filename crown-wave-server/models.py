from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import re
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal
from datetime import datetime





class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(32),  nullable=False)
    userType = db.Column(db.String(128), default = "user" ,nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    referralCode = db.Column(db.String,default = "Null", nullable = False)
    referredBy = db.Column(db.Integer, default = "Null", nullable = False)
    accountTokenId = db.Column(db.Integer, db.ForeignKey("token.id"),default=0, nullable = True)


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
    account_type = db.Column(db.String(50), nullable=False) 
   
  
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

class TransactionUser(db.Model, SerializerMixin):
    __tablename__ = 'transactionUser'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer,db.ForeignKey("account.id"), unique=True, nullable=False)
    description = db.Column(db.String(64), unique=True, nullable=False)
    image = db.Column(db.String,nullable=True)
    amount = db.Column(db.Integer, unique = False , nullable = False)
    price = db.Column(db.Float, nullable=False)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow())



class Customercare(db.Model):
    __tablename__ = 'customercare'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False )
    time = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='pending')

    @validates('message')
    def validate_message(self, key, message):

        if len(message) < 10 or len(message) > 500:
            raise ValueError("Message must be between 10 and 500 characters")
        return message
    @validates('time')
    def validate_time(self, key, time):
        if not re.match(r"^\d{2}:\d{2}:\d{2}$", time):
            raise ValueError("Time must be in HH:MM:SS format")
        return time
    
    def __repr__(self):
        return f"<Customercare {self.id}>"
    

class Package(db.Model):
    __tablename__ = 'package'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 3 or len(name) > 20:
            raise ValueError("Name must be between 3 and 20 characters")
        return name
    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        return price
    
    def __repr__(self):
        return f"<Package {self.id}>"
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }


class Token(db.Model, SerializerMixin):
    __tablename__ = "token"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Float, nullable = False)


class Product(db.Model, SerializerMixin):
    __tablename__ = "Product"
    id = db.Column(db.Integer,primary_key = True)
    description = db.Column(db.String(200),  nullable = False)
    price = db.Column(db.Float, nullable = False)
    units = db.Column(db.Integer, default = 0, nullable = False)
    category = db.Column(db.String(20), nullable = False) 


class Transaction(db.Model):
    __tablename__ = "Transaction"
    id = db.Column(db.Integer, primary_key=True)
    checkout_request_id = db.Column(db.String(100), nullable=True)
    result_code = db.Column(db.Integer, nullable=False)
    result_desc = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=True)
    mpesa_receipt_number = db.Column(db.String(100), nullable=True)
    transaction_date = db.Column(db.String(20), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)

    def __init__(
        self,
        checkout_request_id,
        result_code,
        result_desc,
        amount=None,
        mpesa_receipt_number=None,
        transaction_date=None,
        phone_number=None,
    ):
        self.checkout_request_id = checkout_request_id
        self.result_code = result_code
        self.result_desc = result_desc
        self.amount = amount
        self.mpesa_receipt_number = mpesa_receipt_number
        self.transaction_date = transaction_date
        self.phone_number = phone_number




