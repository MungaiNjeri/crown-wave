from flask import Flask, request, make_response, jsonify, send_from_directory
from models import db,User, Token, Product, Transaction, Account
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS 
from flask_jwt_extended import JWTManager,create_access_token, jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
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
    username = request.json.get("username", None)
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
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/logout")
def logout():
    return "<h1> User log out</h1>"

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




# token API


if __name__ == '__main__':
    app.run(port=5555, debug=True)
