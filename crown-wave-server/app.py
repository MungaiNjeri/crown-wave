from flask import Flask, request, make_response, jsonify, send_from_directory

from models import db,User, Token,  Transaction, Account, Customercare, Package,Product

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
        return make_response(jsonify({error: [str(e)]}))

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
            return make_response(jsonify({error: [str(e)]})
                    )
class PackageById(Resource):
    def get(self,id):
        package = Package.query.filter_by(id=id).first()
        if product:
            return make_response(jsonify(product.to_dict()), 200)
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



if __name__ == '__main__':
    app.run(port=5555, debug=True)
