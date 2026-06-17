import re

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.database import create_user
from models.database import get_user_by_email

auth_bp = Blueprint(
    "auth",
    __name__
)

# REGISTER
@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        # remove spaces
        username = request.form["username"].strip()

        email = request.form["email"].strip()

        password = request.form["password"].strip()

        # USERNAME VALIDATION
        if len(username) < 3:

            return render_template(
                "register.html",
                error="Username must be at least 3 characters"
            )

        if not re.match(
            r"^[A-Za-z0-9_]+$",
            username
        ):
            return render_template(
                "register.html",
                error="Username can contain only letters, numbers and underscore"
            )

        # EMAIL VALIDATION
        if not re.match(
            r"^[^@]+@[^@]+\.[^@]+$",
            email
        ):

            return render_template(
                "register.html",
                error="Please enter a valid email address"
            )

        # PASSWORD VALIDATION
        if len(password) < 8:

            return render_template(
                "register.html",
                error="Password must be at least 8 characters"
            )

        if not re.search(
            r"[A-Z]",password
        ):

            return render_template(
                "register.html",
                error="Password must contain one uppercase letter"
            )

        if not re.search(
            r"[a-z]",password
        ):

            return render_template(
                "register.html",
                error="Password must contain one lowercase letter"
            )

        if not re.search(
            r"[0-9]",password
        ):

            return render_template(
                "register.html",
                error="Password must contain one number"
            )

        # CHECK EXISTING EMAIL
        user = get_user_by_email(email)

        if user:

            return render_template(
                "register.html",
                error="Account already exists with this email"
            )

        # HASH PASSWORD
        hashed_password = generate_password_hash(password)

        # save user
        create_user(
            username,email,hashed_password
        )

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)

def login():

    if request.method == "POST":

        email = request.form["email"].strip()

        password = request.form["password"].strip()

        # EMAIL FORMAT VALIDATION
        if not re.match(
            r"^[^@]+@[^@]+\.[^@]+$",
            email
        ):
            return render_template(
                "login.html",
                error="Please enter a valid email"
            )

        user = get_user_by_email(email)

        # user not found
        if not user:
            return render_template(
                "login.html",
                error="Invalid email or password"
            )

        # password check
        if check_password_hash(user[3],password):

            # create session
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/")

        else:
            return render_template(
                "login.html",
                error="Invalid email or password"
            )

    return render_template("login.html")

# LOGOUT
@auth_bp.route("/logout")

def logout():
    session.clear()

    return redirect("/login")

# TEST ROUTE
@auth_bp.route("/test")

def test():
    
    return "AUTH ROUTE WORKING"