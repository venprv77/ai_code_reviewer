from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection


auth = Blueprint("auth", __name__)


# ================= REGISTER =================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not fullname or not username or not email or not password:

            flash("All fields are required.")

            return redirect(
                url_for("auth.register")
            )

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Check existing email
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                flash("Email already registered.")

                cursor.close()
                connection.close()

                return redirect(
                    url_for("auth.register")
                )

            # Hash password
            hashed_password = generate_password_hash(
                password
            )

            # Insert user
            cursor.execute(
                """
                INSERT INTO users
                (
                    fullname,
                    username,
                    email,
                    password
                )
                VALUES
                (%s, %s, %s, %s)
                """,
                (
                    fullname,
                    username,
                    email,
                    hashed_password
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            flash(
                "Registration successful. Please login."
            )

            return redirect(
                url_for("auth.login")
            )

        except Exception as e:

            print(
                "REGISTER ERROR:",
                e
            )

            flash(
                "Registration failed."
            )

    return render_template(
        "register.html"
    )


# ================= LOGIN =================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        print(
            "LOGIN EMAIL:",
            email
        )

        print(
            "PASSWORD RECEIVED:",
            bool(password)
        )

        try:

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            print(
                "USER FOUND:",
                user is not None
            )

            if user:

                password_correct = check_password_hash(
                    user["password"],
                    password
                )

                print(
                    "PASSWORD CHECK:",
                    password_correct
                )

                if password_correct:

                    session["user_id"] = user["id"]

                    session["email"] = user["email"]

                    return redirect(
                        url_for(
                            "dashboard.dashboard_home"
                        )
                    )

            flash(
                "Invalid email or password"
            )

        except Exception as e:

            print(
                "LOGIN ERROR:",
                e
            )

            flash(
                "Login failed."
            )

    return render_template(
        "login.html"
    )