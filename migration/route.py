import uuid
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    Blueprint,
    flash,
)
from migration.models import Link, User, Transaction, Package
from flask_scrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from migration.mpesa import lipa_na_mpesa_online  # Ensure this import is present
from migration.config import app, db, login_manager, mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

jwt = JWTManager(app)
from flask_login import login_required, current_user, login_user, logout_user

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Blueprint
route_app = Blueprint("route_app", __name__)


# bcrypt = Bcrypt(app)
@app.route("/test", methods=["GET"])
def some_route():
    return "Hello, World!"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    referrer_id = None

    # Check if there's a referral parameter in the URL
    ref_code = request.args.get("ref")
    if ref_code:
        referrer = Link.query.filter_by(
            link_url=url_for("signup", ref=ref_code, _external=True)
        ).first()
        if referrer:
            referrer_id = referrer.user_id

    if request.method == "POST":
        data = request.form  # Use form data

        # Extract and validate data
        username = data.get("username")
        phone = data.get("phone")
        email = data.get("email")
        password = data.get("password")
        membership_level = data.get("membership_level").upper()

        if not all([username, phone, email, password]):
            return render_template("signup.html", error="All fields are required.")

        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="User already exists")

        # Hash password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            phone=phone,
            email=email,
            membership_level=membership_level,
            password=hashed_password,
            balance=0.0,
        )

        db.session.add(new_user)
        db.session.commit()

        # Increment referral count if the user signed up via a referral link
        if referrer_id:
            referrer = Link.query.get(referrer_id)
            referrer.referral_count += 1
            db.session.commit()

        # Create and send the welcome email
        msg = Message(
            subject="Welcome to Your App!",
            recipients=[email],
            body=f"Hello {username},\n\nThank you for signing up for our service! We’re excited to have you on board.",
        )

        try:
            mail.send(msg)
            flash("Signup successful! A welcome email has been sent.", "success")
        except Exception as e:
            flash(
                f"Signup successful, but an error occurred while sending the email: {e}",
                "warning",
            )

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        # Retrieve username and password from form data
        username = data.get("username")
        password = data.get("password")

        # Retrieve user by username
        user = User.query.filter_by(username=username).first()

        if user:
            # Check if the entered password matches the hashed password in the database
            if check_password_hash(user.password, password):
                # Log the user in and redirect to the dashboard
                login_user(user)
                return redirect(url_for("dashboard"))
            else:
                # Password is incorrect
                return render_template("login.html", error="Invalid credentials")
        else:
            # Username does not exist in the database
            return render_template("login.html", error="Invalid credentials")

    # Render the login page if the request method is GET
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate token
            token = serializer.dumps(email, salt="password-reset-salt")
            reset_url = url_for("reset_password", token=token, _external=True)

            # Send reset email
            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=f"Please click the link to reset your password: {reset_url}",
            )
            mail.send(msg)
            flash("Password reset email sent! Check your inbox.", "info")
        else:
            flash("No account found with that email address.", "warning")

        return redirect(url_for("login"))

    return render_template(
        "forgot_password.html"
    )  # Create a form template with an email input


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        # Verify token and extract email
        email = serializer.loads(
            token,
            salt="password-reset-salt",
            max_age=app.config["RESET_TOKEN_EXPIRATION"],
        )
    except Exception:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        password = request.form.get("password")

        # Update user's password
        user = User.query.filter_by(email=email).first()
        if user:
            hashed_password = generate_password_hash(password)
            user.password = hashed_password
            db.session.commit()
            flash("Your password has been updated!", "success")
            return redirect(url_for("login"))
        else:
            flash("User not found.", "warning")

    return render_template(
        "reset_password.html"
    )  # A form template for new password input


@app.route("/dashboard")
@app.route("/account")
@login_required
def dashboard():
    # Fetch user balance and other details
    balance = current_user.balance
    transactions = (
        Transaction.query.filter_by(user_id=current_user.id)
        .order_by(Transaction.timestamp.desc())
        .limit(5)
        .all()
    )
    user_details = {
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "profile_pic": current_user.profile_pic,
        "membership": current_user.membership_level,
    }
    whatsapp_balance = current_user.account_balance.whatsapp_balance if current_user.account_balance else 0
    cashback_balance = current_user.account_balance.cashback_balance if current_user.account_balance else 0
    totalwhatsapp_withdrawal = getattr(current_user, 'totalwhatsapp_withdrawal', 0) or 0

    # Generate or retrieve referral link
    referral_link = Link.query.filter_by(user_id=current_user.id).first()
    if not referral_link:
        # Create a unique referral link for the user if it doesn't exist
        unique_id = str(uuid.uuid4())
        link_url = url_for("signup", ref=unique_id, _external=True)
        referral_link = Link(user_id=current_user.id, link_url=link_url)
        db.session.add(referral_link)
        db.session.commit()

    # Fetch referral count
    referrals = referral_link.referral_count

    return render_template(
        "Dashboard.html",
        balance=balance,
        whatsapp_balance=whatsapp_balance,
        cashback_balance=cashback_balance,
        totalwhatsapp_withdrawal=totalwhatsapp_withdrawal,
        transactions=transactions,
        user_details=user_details,
        referral_link=referral_link.link_url,
        referrals=referrals,
    )
@app.route("/capital",methods=["POST"])
@login_required
def add_capital():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        user.balance += amount
        db.session.commit()
        return redirect(url_for("get_balance"))
    return render_template("capital.html", balance=user.balance)

@app.route("/withdraw",methods=["POST"])
@login_required
def withdraw_capital():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        if user.balance < amount:
            return render_template(
                "withdraw.html", error="Insufficient balance", balance=user.balance
            )
        user.balance -= amount
        db.session.commit()
        return redirect(url_for("get_balance"))
    return render_template("withdraw.html", balance=user.balance)
@login_required
@app.route("/transfer", methods=["GET", "POST"])
def transfer_capital():
    user = current_user
    if request.method == "POST":
        data = request.form
        recipient_phone = data["recipient_phone"]
        amount = float(data["amount"])
        
        if user.balance < amount:
            return render_template("transfer.html", error="Insufficient balance", balance=user.balance)
        
        recipient = User.query.filter_by(phone=recipient_phone).first()
        if recipient:
            new_transaction = Transaction(
                user_id=user.id, amount=amount, recipient=recipient_phone
            )
            user.balance -= amount
            recipient.balance += amount
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for("get_balance"))
        else:
            return render_template("transfer.html", error="User not found", balance=user.balance)
    
    return render_template("transfer.html", balance=user.balance)

@login_required
@app.route("/transactions", methods=["GET", "POST"])
def create_transaction():
    user = current_user

    if request.method == "POST":
        data = request.form
        amount = float(data["amount"])
        
        if user.balance < amount:
            return render_template("transactions.html", error="Insufficient balance", balance=user.balance)
        
        new_transaction = Transaction(
            user_id=user.id, amount=amount, recipient=data["recipient"]
        )
        user.balance -= amount
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for("get_balance"))

    return render_template("transactions.html", balance=user.balance)
@app.route("/capital")
@login_required
def capital():
    return render_template("capital.html")

@app.route("/records")
@login_required
def records():
    return render_template("records.html")

@app.route("/recharge")
@login_required
def recharge():
    return render_template("recharge.html")
@app.route("/whatsapp")
@login_required
def whatsapp():
    return render_template("whatsapp.html")

@app.route("/team")
@login_required
def team():
    return render_template("team.html")

@app.route("/token")
@login_required
def token():
    return render_template("token.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    if request.method == "POST":
        # Add your transfer logic here
        pass
    return render_template("transfer.html")

@app.route("/withdrawal")
@login_required
def withdrawal():
    return render_template("withdrawal.html")

@app.route("/package")
@login_required
def package():
    return render_template("package.html")

@app.route("/claim")
@login_required
def claim():
    return render_template("claim.html")
@login_required
@app.route("/balance", methods=["GET"])
def get_balance():
    user = current_user
    return render_template("balance.html", balance=user.balance)

@app.route("/packages", methods=["GET"])
def get_packages():
    packages = Package.query.all()
    package_list = [
        {"name": p.name, "price": p.price, "reward": p.reward} for p in packages
    ]
    return render_template("packages.html", packages=package_list)
@app.route("/mpesa_pay", methods=["GET", "POST"])
def mpesa_payment():
    if request.method == "POST":
        data = request.form
        phone_number = data.get("phone_number")
        amount = data.get("amount")

        if not phone_number or not amount:
            return render_template(
                "mpesa_payment.html", error="Phone number and amount are required."
            )

        try:
            response = lipa_na_mpesa_online(phone_number, float(amount))
            return render_template(
                "mpesa_payment.html", success="Payment successful", response=response
            )
        except Exception as e:
            return render_template("mpesa_payment.html", error=str(e))

    return render_template("mpesa_payment.html")


if __name__ == "__main__":
    app.run(debug=True)
