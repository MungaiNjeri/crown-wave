from flask import Flask, jsonify
from flask_migrate import Migrate
from flask import Blueprint
from models import db, User, Transaction, Package
import os, requests
from mpesa import lipa_na_mpesa_online
from flask import request
app = Flask(__name__)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret'


# Apply config
app.config.from_object(Config)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Blueprint
route_app = Blueprint('route_app', __name__)

@app.route('/some_route', methods=['GET'])
def some_route():
    return "Hello, World!"

# Register routes
app.register_blueprint(route_app)

@app.route('/mpesa_pay', methods=['POST'])
def mpesa_payment():
    data = request.json
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    
    try:
        response = lipa_na_mpesa_online(phone_number, amount)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
