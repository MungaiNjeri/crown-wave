from flask import Flask, jsonify
from flask import Blueprint
from models import  User, Transaction, Package
from mpesa import lipa_na_mpesa_online
from flask import request
from config import app,db
from route import route_app





# Register routes
app.register_blueprint(route_app)

""" @app.route('/mpesa_pay', methods=['POST'])
def mpesa_payment():
    data = request.json
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    
    try:
        response = lipa_na_mpesa_online(phone_number, amount)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 """

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
