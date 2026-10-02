from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection


auth = Blueprint(
    "auth",
    __name__
)


# Register Page

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO users
            (
                fullname,
                username,
                email,
                password
            )
            VALUES
            (%s,%s,%s,%s)
            """

            cursor.execute(
                query,
                (
                    fullname,
                    username,
                    email,
                    hashed_password
                )
            )

            connection.commit()


            return redirect(
                url_for("auth.login")
            )


        except Exception as e:

            print("REGISTER ERROR:", e)

            return "Registration Failed"


        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    return render_template(
        "register.html"
    )

# Login Page

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                select *
                from users
                where email=%s
                """,
                (email,)
            )

            user = cursor.fetchone()


            if user and check_password_hash(
                user["password"],
                password
            ):

                session["user_id"] = user["id"]
                session["username"] = user["username"]


                return redirect(
                    url_for("dashboard.dashboard_home")
                )


            else:

                return "Invalid Email or Password"


        except Exception as e:

            print("LOGIN ERROR:", e)

            return "Login Failed"


        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    return render_template(
        "login.html"
    )



# Logout

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )