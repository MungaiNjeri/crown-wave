from flask import Flask, request, make_response, jsonify, send_from_directory
from models import db,User
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS 
from flask_jwt_extended import JWTManager,create_access_token, jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import Account, Transaction
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
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'artvista.db')}")

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


@app.route("/signup")
def signup():
    try:
        new_record = User(
            username=request.json["username"],
            email=request.json["email"],
            user_role = request.json["userrole"],
             )
        new_record.set_password(request.json["password"])
        db.session.add(new_record)
        db.session.commit()
        response = new_record.to_dict()
        logging.info(f"Created new user: {new_record.username}")
        return make_response(jsonify(response), 201)
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return make_response(jsonify({"errors": [str(e)]}), 400)

@app.route("/login")
def login():
    return "<h1> login to your account<h2>"



@app.route('/api/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    new_account = Account(user_id=data['user_id'], balance=data.get('balance', 0.0))
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Account created', 'account_id': new_account.account_id}), 201



@app.route('/api/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({
        'account_id': account.account_id,
        'user_id': account.user_id,
        'balance': account.balance
    })

@app.route('/api/accounts/<int:account_id>', methods=['PUT'])
def update_balance(account_id):
    data = request.get_json()
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    account.balance = data['balance']
    db.session.commit()
    return jsonify({'message': 'Account balance updated'})


@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted'})



@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    account = Account.query.get(data['account_id'])
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    new_transaction = Transaction(
        account_id=data['account_id'],
        description=data['description'],
        amount=data['amount']
    )
    account.balance += data['amount']  # Update account balance
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added', 'transaction_id': new_transaction.transaction_id}), 201



@app.route('/api/accounts/<int:account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    transactions = Transaction.query.filter_by(account_id=account_id).all()
    return jsonify([
        {
            'transaction_id': t.transaction_id,
            'description': t.description,
            'amount': t.amount
        } for t in transactions
    ])




@app.route("/delete/account")
def delete():
    return "<h1> delete your user account"




if __name__ == '__main__':
    app.run(port=5555, debug=True)
