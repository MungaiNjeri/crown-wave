from app import app, db
from models import User, Token, Transaction, Account


print(" started seeding database ")
with app.app_context():
    db.drop_all()
    db.create_all()
print(" finished seeding database" )
