from flask import Flask, request, make_response, jsonify, send_from_directory

from models import db,User, Token,  Transaction, Account, Customercare, Package

from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS 
from flask_jwt_extended import JWTManager,create_access_token, jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os 
import logging


app = Flask(__name__)

# Configure CORS
CORS(app) 

# Configure upload folder and allowed extensions

UPLOAD_FOLDER = 'images/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'crown-wave.db')}")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your_secret_key")  # Load from env

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)


@app.route('/')
def index():
    return '<h1>Welcome to crown-wave-server</h1>'


@app.route("/signup", methods = ["POST"])
def signup():
    try:
        new_record = User(
            fullname = request.json["fullname"],
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
    

@app.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    if user:
        current_user = user.to_dict()
        return make_response(jsonify(current_user["username"]), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 404)


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
        data = request.get_json()
        user = User.query.filter_by(id=id).first()
        try:
            for attr in data:
                if(attr == "password"):
                    data.set_password(request.json["password"])       
                    setattr(user,attr,data[attr])
                else:    
                    setattr(user, attr, data[attr])
        
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify(str(e)))
        return make_response(user.to_dict(), 202)
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



class Createaccount(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()  # Get user ID from JWT
        account = Account(user_id=user_id, account_type=data.get('account_type'))
        db.session.add(account)
        db.session.commit()
        return jsonify({'message': 'Account created successfully'}), 201


class Addaccount(Resource):
    @jwt_required()
    def post(self):
        current_user =get_jwt_identity()
        data = request.get_json()
        account = Account(
            user_id=current_user['id'],
           balance=data.get('balance', 0.0),
            account_type=data['account_type']
        )
        db.session.add(account)
        db.session.commit()
        return jsonify({"message": "Account created successfully", "account": {
            "id": account.id,
            "user_id": account.user_id,
            "balance": account.balance,
            "account_type": account.account_type
        }})

class UpdateAccountBalance(Resource):
    @jwt_required()
    def put(self, account_id):
        current_user = get_jwt_identity()
        data = request.get_json()
        account = Account.query.filter_by(id=account_id, user_id=current_user['id']).first()
        if not account:
            return jsonify({"error": "Account not found or unauthorized"}), 404

        new_balance = data.get('balance')
        if new_balance is None or new_balance < 0:
            return {"error": "Balance must be a positive number"}, 400

        account.balance = new_balance
        db.session.commit()
        return jsonify({"message": "Balance updated successfully", "account": {
            "id": account.id,
            "user_id": account.user_id,
            "balance": account.balance,
            "account_type": account.account_type
        }})
    
class CreateTransaction(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        account = Account.query.filter_by(user_id=user_id).first()
        if not account:
            return jsonify({'message': 'Account not found'}), 404
        # Validate and process transaction logic here
        # ...
        amount = data.get('amount')
        if amount is None:
            return jsonify({'message': 'Missing required field: amount'}), 400
        try:
            amount = float(amount)
        except ValueError:
            return jsonify({'message': 'Invalid amount format'}), 400

        if account.balance + amount < 0:
            return jsonify({'message': 'Insufficient funds for transaction'}), 400
        transaction = Transaction(account_id=account.id, description=data.get('description'), amount=data.get('amount'))
        db.session.add(transaction)
        db.session.commit()

        return jsonify({"message": "Transaction created successfully", "transaction": {
            "id": transaction.id,
            "account_id": transaction.account_id,
            "description": transaction.description,
            "amount": transaction.amount}})
api.add_resource(Createaccount, '/Createaccounts')
api.add_resource(Addaccount, '/addaccounts')
api.add_resource(UpdateAccountBalance, '/updateBalance/<int:account_id>')
api.add_resource(CreateTransaction, '/transactions')


class PackageListResource(Resource):
    @jwt_required()
    def get(self):
        packages = Package.query.all()
        return [package.to_dict() for package in packages]
    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')

        if not name or not description or not price:
            return {'error': 'Missing required fields: name, description, price'}, 400

        try:
            price = float(price)
        except ValueError:
            return {'error': 'Invalid price format'}, 400

        package = Package(name=name, description=description, price=price)
        db.session.add(package)
        db.session.commit()

        return package.to_dict(), 201
    

class PackageResource(Resource):
    @jwt_required()
    def get(self, package_id):
        package = Package.query.get_or_404(package_id)
        return package.to_dict()
    @jwt_required()
    def put(self, package_id):
        package = Package.query.get_or_404(package_id)
        data = request.get_json()
        package.name = data.get('name', package.name)
        package.price = data.get('price', package.price)

        db.session.commit()
        return package.to_dict()
    @jwt_required()
    def delete(self, package_id):
        package = Package.query.get_or_404(package_id)
        db.session.delete(package)
        db.session.commit()
        return {'message': 'Package deleted successfully'}, 200
api.add_resource(PackageListResource,'/packages')
api.add_resource(PackageResource, '/packages/<int:package_id>')    




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



# token API


if __name__ == '__main__':
    app.run(port=5555, debug=True)
