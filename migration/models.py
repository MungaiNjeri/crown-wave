from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
import enum
from migration.config import db


class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0)

    #Relationships
    user = db.relationship("User", backref="account", uselist=False)


