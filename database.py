import mysql.connector
from mysql.connector import Error

from config import Config


def get_connection():

    try:

        connection = mysql.connector.connect(

            host="127.0.0.1",
            port=3306,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            connection_timeout=5,
            use_pure=True

        )

        return connection


    except Error as e:

        print("Database Connection Error:", e)

        return None



def test_connection():

    print("Testing Database Connection...")

    connection = get_connection()


    if connection:

        print("Database Connection Successfully!")

        connection.close()

    else:

        print("Connection Failed!")



if __name__ == "__main__":

    test_connection()