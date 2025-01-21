from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS 
import os 
from dotenv import load_dotenv
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crown-wave.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(metadata=metadata)

db.init_app(app)
migrate = Migrate(app, db)
# Configure CORS
CORS(app) 

# Configure upload folder and allowed extensions

UPLOAD_FOLDER = 'images/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



