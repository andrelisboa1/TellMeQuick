import sqlite3 as sql

db_filename = "database.db"

def db_init(_connection):
    """
    STRUCTURE:
    user:
        id integer
        username text
        password text
    message:
        id integer
        src_user_id integer
        dest_user_id integer
        text_content text
    """
    with _connection as conn:
        cursor = conn.cursor()
        # Create user table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        # Create message table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                src_user_id INTEGER NOT NULL,
                dest_user_id INTEGER NOT NULL,
                text_content TEXT NOT NULL,
                FOREIGN KEY (src_user_id) REFERENCES user (id),
                FOREIGN KEY (dest_user_id) REFERENCES user (id)
            )
        """)
        _connection.commit()