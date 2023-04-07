import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Get database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Execute a query and return the result
def execute_query(query, values=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, values)
    result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return result

# Get a connection to the database
def get_connection():
    try:
        conn = mysql.connector.connect(host=DB_HOST,
            port=DB_PORT, 
            user=DB_USER, 
            password=DB_PASSWORD,
            database="satisfactions")
        return conn

    except Exception as e:
        print(f"Error: {e}")

# Create the database and tables if they doesn't exist
def setup_database():
    try:
        conn = mysql.connector.connect(host=DB_HOST,
            port=DB_PORT, 
            user=DB_USER, 
            password=DB_PASSWORD)
        cursor = conn.cursor()
        sql_statements = [
            "CREATE DATABASE IF NOT EXISTS satisfactions",
            "USE satisfactions",
            "CREATE TABLE IF NOT EXISTS factions (faction_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE, points INT)",
            "CREATE TABLE IF NOT EXISTS faction_items (faction_id INT, channel_id BIGINT UNSIGNED, role_id BIGINT UNSIGNED, FOREIGN KEY (faction_id) REFERENCES factions(faction_id))",
            "CREATE TABLE IF NOT EXISTS users (user_id BIGINT UNSIGNED PRIMARY KEY, faction_id INT, faction_leader BOOLEAN, FOREIGN KEY (faction_id) REFERENCES factions(faction_id))",
            "CREATE TABLE IF NOT EXISTS user_invites (user_id BIGINT UNSIGNED, faction_id INT, FOREIGN KEY (faction_id) REFERENCES factions(faction_id))"
        ]
        
        for statement in sql_statements:
            cursor.execute(statement)

        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()