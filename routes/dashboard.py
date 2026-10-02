from flask import Blueprint, render_template, session, redirect, url_for
from database import get_connection

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def dashboard_home():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    username = session.get("username", "User")

    total_reviews = 0
    average_score = 0
    total_bugs = 0
    total_suggestions = 0

    try:

        connection = get_connection()

        if connection:

            cursor = connection.cursor()

            # Total Reviews
            cursor.execute(
                "select count(*) from review where user_id=%s",
                (session["user_id"],)
            )

            result = cursor.fetchone()

            if result:
                total_reviews = result[0]

            # Average Score
            cursor.execute(
                """
                select
                coalesce(avg(score),0)
                from review
                where user_id=%s
                """,
                (session["user_id"],)
            )

            average_score = round(cursor.fetchone()[0], 2)

            # Total Bugs
            cursor.execute(
                """
                select
                coalesce(sum(bugs_found),0)
                from review
                where user_id=%s
                """,
                (session["user_id"],)
            )

            total_bugs = cursor.fetchone()[0]

            # Total Suggestions
            cursor.execute(
                """
                select
                coalesce(sum(suggestions),0)
                from review
                where user_id=%s
                """,
                (session["user_id"],)
            )

            total_suggestions = cursor.fetchone()[0]

            cursor.close()
            connection.close()

    except Exception as e:

        print("Dashboard Error:", e)

    return render_template(
        "dashboard.html",
        username=username,
        total_reviews=total_reviews,
        average_score=average_score,
        total_bugs=total_bugs,
        total_suggestions=total_suggestions
    )


@dashboard.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    reviews = []

    try:

        connection = get_connection()

        if connection:

            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                select
                    id,
                    filename,
                    language,
                    score,
                    bugs_found,
                    suggestions,
                    created_at
                from review
                where user_id=%s
                order by created_at desc
                """,
                (session["user_id"],)
            )

            reviews = cursor.fetchall()

            cursor.close()
            connection.close()

    except Exception as e:

        print("History Error:", e)

    return render_template(
        "history.html",
        reviews=reviews
    )


@dashboard.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = {}

    try:

        connection = get_connection()

        if connection:

            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                select
                    id,
                    username,
                    email
                from users
                where id=%s
                """,
                (session["user_id"],)
            )

            user = cursor.fetchone()

            cursor.close()
            connection.close()

    except Exception as e:

        print("Profile Error:", e)

    return render_template(
        "profile.html",
        user=user
    )


@dashboard.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))