import sqlite3
import json

DB_PATH = "chat.db"

# init database
def init():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT
            )
        """)
        conn.commit()

# save  message and respone (JSON)
def save_message(message, response):
    data = json.dumps({"message": message, "response": response})
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (data) VALUES (?)", (data,))
        conn.commit()

# get all message
def get_messages():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM messages")
        return [json.loads(data[0]) for data in cursor.fetchall()]