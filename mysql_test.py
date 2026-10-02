import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="moksha",
    database="ai_code_reviewer",
    connection_timeout=5
)

print("Connected Successfully")

conn.close()