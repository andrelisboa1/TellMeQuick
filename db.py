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

def add_message(_connection: sql.Connection, src_user_id: int, dest_user_id: int, text_content: str):
    """
    Adds a message to the message table.
    :param _connection: SQLite connection object
    :param src_user_id: ID of the sender
    :param dest_user_id: ID of the recipient
    :param text_content: Content of the message
    """
    cursor = _connection.cursor()
    cursor.execute("""
        INSERT INTO message (src_user_id, dest_user_id, text_content)
        VALUES (?, ?, ?)
    """, (src_user_id, dest_user_id, text_content))
    _connection.commit()

def get_messages_between_users(_connection: sql.Connection, user1_id: int, user2_id: int):
    """
    Retrieves messages exchanged between two users.
    :param _connection: SQLite connection object
    :param user1_id: ID of the first user
    :param user2_id: ID of the second user
    :return: List of messages exchanged between the two users
    """
    cursor = _connection.cursor()
    cursor.execute("""
        SELECT src_user_id, dest_user_id, text_content
        FROM message
        WHERE (src_user_id = ? AND dest_user_id = ?)
           OR (src_user_id = ? AND dest_user_id = ?)
        ORDER BY id ASC
    """, (user1_id, user2_id, user2_id, user1_id))
    return cursor.fetchall()

