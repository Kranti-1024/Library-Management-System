# This is 'database/db_connection.py'

import mysql.connector
from mysql.connector import Error
from utils.config import DB_CONFIG  # Import credentials

def create_connection():
    """ Create a database connection to the MySQL database """
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            print("Successfully connected to the database")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None  # Return None if connection fails
        
    return connection

def close_connection(connection):
    """ Close the database connection """
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")

# A simple test to run when this file is executed directly
if __name__ == '__main__':
    conn = create_connection()
    if conn:
        close_connection(conn)