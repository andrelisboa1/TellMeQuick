import sqlite3 as sql

db_filename = "database.db"

def db_init(_connection: sql.Connection):
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
    cursor = _connection.cursor()
    # Check if the database is already initialized
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='user'
    """)
    if cursor.fetchone():
        print("Database is already initialized.")
        return
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

def create_user(_connection: sql.Connection, username: str, password: str):
    """
    Inserts a new user into the user table.
    :param _connection: SQLite connection object
    :param username: Username of the new user
    :param password: Password of the new user
    """
    cursor = _connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO user (username, password)
            VALUES (?, ?)
        """, (username, password))
        _connection.commit()
        print(f"User '{username}' created successfully.")
    except sql.IntegrityError as e:
        print(f"Error: {e}")

def reset_database(_connection: sql.Connection):
    """
    Clears and rebuilds the database.
    :param _connection: SQLite connection object
    """
    cursor = _connection.cursor()
    # Clear the database
    cursor.execute("DROP TABLE IF EXISTS message")
    cursor.execute("DROP TABLE IF EXISTS user")
    _connection.commit()
    # Rebuild the database
    db_init(_connection)

