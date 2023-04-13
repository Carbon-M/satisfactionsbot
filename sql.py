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
def execute_query(query, values=None) -> list | None:
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
            "CREATE TABLE IF NOT EXISTS faction_items (faction_id INT, channel_id BIGINT UNSIGNED, role_id BIGINT UNSIGNED, FOREIGN KEY (faction_id) REFERENCES factions(faction_id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS users (user_id BIGINT UNSIGNED PRIMARY KEY, faction_id INT, faction_leader BOOLEAN, FOREIGN KEY (faction_id) REFERENCES factions(faction_id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS user_invites (user_id BIGINT UNSIGNED, faction_id INT, FOREIGN KEY (faction_id) REFERENCES factions(faction_id) ON DELETE CASCADE)"
        ]
        
        for statement in sql_statements:
            cursor.execute(statement)

        conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()

# User related functions

# Add an invite to a user from a faction to the database
def add_user_invite(user_id, faction_id):
    execute_query("INSERT INTO user_invites (user_id, faction_id) VALUES (%s, %s)", (user_id, faction_id))

# Remove an invite to a user from a faction from the database
def remove_user_invite(user_id, faction_id):
    execute_query("DELETE FROM user_invites WHERE user_id = %s AND faction_id = %s", (user_id, faction_id))

# Get whether or not a user has an invite from a faction
def is_user_invited(user_id, faction_id) -> bool:
    result = execute_query("SELECT * FROM user_invites WHERE user_id = %s AND faction_id = %s", (user_id, faction_id))
    return len(result) > 0

# Get a user's faction ID, returns none if they're not in a faction
def get_user_faction(user_id) -> int | None:
    result = execute_query("SELECT faction_id FROM users WHERE user_id = %s", (user_id,))
    if len(result) == 0:
        return None
    
    else:
        return result[0][0]

# Get whether or not a user is the leader of the faction they're in, defaults to false
def is_user_leader(user_id) -> bool:
    result = execute_query("SELECT faction_leader FROM users WHERE user_id = %s", (user_id,))
    if len(result) == 0:
        return False
    
    else:
        return result[0][0]

# Set a user's faction ID, if they're already in a faction, update it
def set_user_faction(user_id, faction_id, faction_leader):
    execute_query("INSERT INTO users (user_id, faction_id, faction_leader) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE faction_id = %s", (user_id, faction_id, faction_leader, faction_id))

# Faction related functions

# Add a faction to the database
def create_faction(name) -> int:
    execute_query("INSERT INTO factions (name, points) VALUES (%s, %s)", (name, 0))
    return get_faction_id(name)

# Get a faction's ID from the database
def get_faction_id(name) -> int | None:
    result = execute_query("SELECT faction_id FROM factions WHERE name = %s", (name,))

    if len(result) == 0:
        return None

    return result[0][0]

# Get a faction's name from the database
def get_faction_name(faction_id) -> str:
    result = execute_query("SELECT name FROM factions WHERE faction_id = %s", (faction_id,))
    return result[0][0]

# Rename a faction in the database
def rename_faction(faction_id, new_name):
    execute_query("UPDATE factions SET name = %s WHERE faction_id = %s", (new_name, faction_id))

# Delete a faction from the database
def delete_faction(faction_id):
    execute_query("DELETE FROM factions WHERE faction_id = %s", (faction_id,))

# Check if a faction name is unique
def is_faction_unique(name) -> bool:
    result = execute_query("SELECT * FROM factions WHERE name = %s", (name,))
    return len(result) == 0

# Faction Items related functions

# Get a faction's channel ID from the database
def get_channel_id(faction_id) -> int | None:
    result = execute_query("SELECT channel_id FROM faction_items WHERE faction_id = %s", (faction_id,))

    if len(result) == 0:
        return None

    return result[0][0]

# Get a faction's role ID from the database
def get_role_id(faction_id) -> int | None:
    result = execute_query("SELECT role_id FROM faction_items WHERE faction_id = %s", (faction_id,))

    if len(result) == 0:
        return None

    return result[0][0]