from config import app,db
from models import User, Token,  Transaction, Account, Customercare, Package,Product,TransactionUser
from flask import Flask, request, make_response, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager,create_access_token, jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os 
import logging
import json
from typing import Dict, Any



# Configure upload folder and allowed extensions


app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your_secret_key")  # Load from env


api = Api(app)
jwt = JWTManager(app)




@app.route('/')
def index():
    return '<h1>Welcome to crown-wave-server</h1>'


@app.route("/signup", methods = ["POST"])
def signup():
    try:
        new_record = User(
            username=request.json["username"],
            email=request.json["email"],
            password = request.json["password"]
             )
        new_record.set_password(request.json["password"])
        db.session.add(new_record)
        db.session.commit()
        response = new_record.to_dict()
        logging.info(f"Created new user: {new_record.username}")
        return make_response(jsonify(response), 201)
    except Exception as e:
        
        return make_response(jsonify({"errors": [str(e)]}), 400)

@app.route("/login",methods = ["POST"])
def login():
    username =request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token,user_id = user.id), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401
    

# Route to get the current user
@app.route("/current_user", methods=["GET"])
@jwt_required()
def get_current_user():
    token = request.headers.get("Authorization")
    app.logger.info(f"Received Token: {token}")

@app.route("/logout")
def logout():
    return "<h1> User log out</h1>"


#  User /patch and /put 
class UserById(Resource):
    @jwt_required()
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return make_response(jsonify(user.to_dict()),200)
    #@jwt_required()
    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        try:
            for key, value in request.json.items():
                if hasattr(user, key):
                    if key == 'password':
                        value = generate_password_hash(value) #.decode('utf-8')
                    setattr(user, key, value)
                    db.session.commit()
    
                    return make_response(jsonify(user.to_dict()), 200)
        
        except Exception as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)

    @jwt_required()
    def delete(self, id):
        pass

api.add_resource(UserById, '/user/<int:id>')

# Resources
class CustomercareListResource(Resource):
    
    @jwt_required()
    def get(self):
        try:
            customercares = Customercare.query.all()
            return [customercare.to_dict() for customercare in customercares], 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            message = data.get('message')
            time = data.get('time')

            customercare = Customercare(message=message, time=time)
            db.session.add(customercare)
            db.session.commit()

            return customercare.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

class CustomercareResource(Resource):
    @jwt_required()
    def get(self, customercare_id):
        try:
            customercare = Customercare.query.get_or_404(customercare_id)
            return customercare.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def put(self, customercare_id):
        try:
            customercare = Customercare.query.get_or_404(customercare_id)
            data = request.get_json()

            customercare.message = data.get('message', customercare.message)
            customercare.time = data.get('time', customercare.time)
            db.session.commit()

            return customercare.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def delete(self, customercare_id):
        try:
            customercare = Customercare.query.get_or_404(customercare_id)
            db.session.delete(customercare)
            db.session.commit()

            return {'message': 'Customercare deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# Add routes to the API
api.add_resource(CustomercareListResource, '/customercare')
api.add_resource(CustomercareResource, '/customercare/<int:customercare_id>')




@app.route("/delete/account")
def delete():
    return "<h1> delete your user account"

@app.route("/createToken", methods = ["POST"])
def new_token():
    try:
        new_record = Token(
            name=request.json["name"],
            description=request.json["description"],
            price = request.json["price"]
             )
        db.session.add(new_record)
        db.session.commit()
 
        return make_response(jsonify("success adding creating new token"), 201)

    except Exception as e:
        return make_response(jsonify({"errors": [str(e)]}))

@app.route("/tokens", methods = ["GET"])
def tokens():

    tokens = []
    for token in Token.query.all():
        token_dict = {
            "id": token.id,
            "name": token.name,
            "description": token.description,
            "price": token.price,
        }
        tokens.append(token_dict)

    response = make_response(
        tokens,
        200,
        {"Content-Type": "application/json"}
    )

    return response




# product API,S
@app.route("/product",methods=["POST"])
def create_product():
    try:
        new_record = Product(
        description = request.json["name"],
        price = request.json["price"],
        units = request.json["units"],
        category = request.json["category"]        
        )
        db.session.add(new_record)
        db.session.commit()
        return make_response(jsonify("success: Product added"),201)
    except Exception as e:
        return make_response(jsonify({'error': [str(e)]}))

#packages
class Packages(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Product.query.all()]
        return make_response(jsonify(response_dict_list), 200)
    def post(self):

        try:
            new_record =Package(
                        name = request.get_json["name"],
                        price = request.get_json["price"]

                    )
            db.session.add(new_record)
            db.session.commit()
            return make_response(jsonify("success: package added"),201)
        except Exception as e:
            return make_response(jsonify({'error': [str(e)]})
                    )
class PackageById(Resource):
    def get(self,id):
        package = Package.query.filter_by(id=id).first()
        if  Product:
            return make_response(jsonify(Product.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Package not found"}), 404)


api.add_resource(Packages,"/packages")
api.add_resource(PackageById,"/package/<int:id>")



class Products(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Product.query.all()]
        return make_response(jsonify(response_dict_list), 200)
class ProductById(Resource):
    def get(self,id):
        product = Product.query.filter_by(id=id).first()
        if product:
            return make_response(jsonify(product.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Product not found"}), 404)
        


api.add_resource(Products, "/products")
api.add_resource(ProductById, "/product/<int:id>")



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("mpesa_callbacks.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)




# Define the Transaction model

# MPesa Callback Processor
class MPesaCallback:
    @staticmethod
    def process_callback(callback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the callback data from M-Pesa and extract relevant transaction details.

        Args:
            callback_data (Dict[str, Any]): Raw callback data from M-Pesa

        Returns:
            Dict[str, Any]: Processed transaction details
        """
        try:
            body = callback_data.get("Body", {})
            stkCallback = body.get("stkCallback", {})

            # Extract basic transaction details
            checkout_request_id = stkCallback.get("CheckoutRequestID")
            result_code = stkCallback.get("ResultCode")
            result_desc = stkCallback.get("ResultDesc")

            # Initialize transaction details
            transaction_details = {
                "checkout_request_id": checkout_request_id,
                "result_code": result_code,
                "result_desc": result_desc,
                "amount": None,
                "mpesa_receipt_number": None,
                "transaction_date": None,
                "phone_number": None,
            }

            # If transaction was successful, extract additional details
            if result_code == 0:  # Successful transaction
                callback_metadata = stkCallback.get("CallbackMetadata", {}).get(
                    "Item", []
                )

                # Process callback metadata
                for item in callback_metadata:
                    name = item.get("Name")
                    value = item.get("Value")

                    if name == "Amount":
                        transaction_details["amount"] = value
                    elif name == "MpesaReceiptNumber":
                        transaction_details["mpesa_receipt_number"] = value
                    elif name == "TransactionDate":
                        transaction_details["transaction_date"] = value
                    elif name == "PhoneNumber":
                        transaction_details["phone_number"] = value

            logger.info(
                f"Processed callback for CheckoutRequestID: {checkout_request_id}"
            )
            return transaction_details

        except Exception as e:
            logger.error(f"Error processing callback data: {e}")
            raise ValueError(f"Invalid callback data structure: {e}")


# Flask Routes
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Hello, World!"})


@app.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    """
    Flask endpoint to handle M-Pesa callbacks.
    """
    try:
        callback_data = request.get_json()
        logger.info(f"Received callback: {json.dumps(callback_data, indent=2)}")

        # Process the callback
        transaction_details = MPesaCallback.process_callback(callback_data)

        # Store transaction details in the database
        store_transaction_details(transaction_details)

        return jsonify(
            {"ResultCode": 0, "ResultDesc": "Callback processed successfully"}
        ), 200

    except Exception as e:
        logger.error(f"Callback processing failed: {e}")
        return jsonify(
            {"ResultCode": 1, "ResultDesc": f"Callback processing failed: {str(e)}"}
        ), 500


# Helper Functions
def store_transaction_details(transaction_details: Dict[str, Any]) -> None:
    """
    Store transaction details in the database.

    Args:
        transaction_details (Dict[str, Any]): Processed transaction details
    """
    try:
        # Validate required fields
        if (
            not transaction_details.get("checkout_request_id")
            or not transaction_details.get("result_code")
            or not transaction_details.get("result_desc")
        ):
            raise ValueError("Missing required transaction details")

        # Create a new Transaction object
        transaction = Transaction(
            checkout_request_id=transaction_details["checkout_request_id"],
            result_code=transaction_details["result_code"],
            result_desc=transaction_details["result_desc"],
            amount=transaction_details.get("amount"),
            mpesa_receipt_number=transaction_details.get("mpesa_receipt_number"),
            transaction_date=transaction_details.get("transaction_date"),
            phone_number=transaction_details.get("phone_number"),
        )

        # Add and commit the transaction to the database
        db.session.add(transaction)
        db.session.commit()
        logger.info(
            f"Transaction {transaction_details['checkout_request_id']} stored successfully"
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to store transaction details: {e}")
        raise e
    



@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.json
    user_id = data.get('user_id')
    account_type = data.get('account_type')

    if not user_id or not account_type:
        return jsonify({"error": "user_id and account_type are required"}), 400

    account = Account(user_id=user_id, account_type=account_type)
    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "Account created successfully", "account_id": account.id}), 201

@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "account_id": account.id,
        "user_id": account.user_id,
        "balance": account.balance,
        "account_type": account.account_type
    })

@app.route('/transactionsUser', methods=['POST'])
def create_transactionUser():
    data = request.json
    account_id = data.get('account_id')
    description = data.get('description')
    amount = data.get('amount')
    price = data.get('price')

    if not account_id or not description or not amount or not price:
        return jsonify({"error": "account_id, description, amount, and price are required"}), 400

    # Check if account exists
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Create transaction
    transaction = TransactionUser(
        account_id=account_id,
        description=description,
        amount=amount,
        price=price
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction created successfully", "transaction_id": transaction.id}), 201

@app.route('/transactions/<int:account_id>', methods=['GET'])
def get_transactions(account_id):
    transactions = TransactionUser.query.filter_by(account_id=account_id).all()
    if not transactions:
        return jsonify({"error": "No transactions found for this account"}), 404

    return jsonify([{
        "id": t.id,
        "description": t.description,
        "amount": t.amount,
        "price": t.price,
        "timestamp": t.timestamp
    } for t in transactions])


# Run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)

