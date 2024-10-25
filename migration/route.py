from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, User, Transaction, Package
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from mpesa import lipa_na_mpesa_online  # Ensure this import is present

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'

db.init_app(app)
jwt = JWTManager(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form  # Use form data
        if User.query.filter_by(email=data['email']).first():
            return render_template("register.html", error="User already exists")

        new_user = User(username=data['username'], email=data['email'], phone=data['phone'], balance=0.0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user:
            token = create_access_token(identity=user.id)
            return redirect(url_for('get_balance', token=token))  # Pass token as query parameter
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route('/transactions', methods=['GET', 'POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if request.method == 'POST':
        data = request.form
        amount = float(data['amount'])
        if user.balance < amount:
            return render_template("transactions.html", error="Insufficient balance", balance=user.balance)

        new_transaction = Transaction(user_id=user.id, amount=amount, recipient=data['recipient'])
        user.balance -= amount
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for('get_balance'))
    
    return render_template("transactions.html", balance=user.balance)

@app.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return render_template("balance.html", balance=user.balance)

@app.route('/packages', methods=['GET'])
def get_packages():
    packages = Package.query.all()
    package_list = [{"name": p.name, "price": p.price, "reward": p.reward} for p in packages]
    return render_template("packages.html", packages=package_list)

@app.route('/mpesa_pay', methods=['GET', 'POST'])
def mpesa_payment():
    if request.method == 'POST':
        data = request.form
        phone_number = data.get("phone_number")
        amount = data.get("amount")
        
        if not phone_number or not amount:
            return render_template("mpesa_payment.html", error="Phone number and amount are required.")

        try:
            response = lipa_na_mpesa_online(phone_number, float(amount))
            return render_template("mpesa_payment.html", success="Payment successful", response=response)
        except Exception as e:
            return render_template("mpesa_payment.html", error=str(e))
    
    return render_template("mpesa_payment.html")

if __name__ == '__main__':
    app.run(debug=True)
