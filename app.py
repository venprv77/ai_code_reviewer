from flask import Flask, send_from_directory, render_template
from dotenv import load_dotenv
import os

from config import Config

from routes.auth import auth
from routes.dashboard import dashboard
from routes.reviewer import reviewer


load_dotenv()


app = Flask(__name__)

app.template_folder = "templates"

app.config["SECRET_KEY"] = Config.SECRET_KEY


UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER



# Register Blueprints

app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(reviewer)



@app.route("/reports/<path:filename>")
def download_report(filename):

    return send_from_directory(
        app.config["REPORT_FOLDER"],
        filename,
        as_attachment=True
    )



@app.route("/")
def home():

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)