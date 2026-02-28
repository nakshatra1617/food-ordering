import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # your MySQL username
            password="DB_password",  # your MySQL password
            database="food_ordering"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
