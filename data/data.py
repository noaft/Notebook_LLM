import sqlite3
import json

conn = sqlite3.connect("chat.db")
cursor = conn.cursor()

def init():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    """)

# Lưu tin nhắn (JSON)
def save_message( message, response):
    data = json.dumps({"message": message, "response": response})
    cursor.execute("INSERT INTO messages (user, data) VALUES ( ?)", ( data))
    conn.commit()

# Lấy tin nhắn
def get_messages():
    cursor.execute("SELECT data FROM messages")
    return [( json.loads(data)) for data in cursor.fetchall()]
