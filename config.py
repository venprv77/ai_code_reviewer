import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default_secret_key"
    )


    # Database

    DB_HOST = os.getenv(
        "DB_HOST"
    )

    DB_PORT = os.getenv(
        "DB_PORT"
    )

    DB_USER = os.getenv(
        "DB_USER"
    )

    DB_PASSWORD = os.getenv(
        "DB_PASSWORD"
    )

    DB_NAME = os.getenv(
        "DB_NAME"
    )


    # File Upload

    UPLOAD_FOLDER = "uploads"

    REPORT_FOLDER = "reports"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024