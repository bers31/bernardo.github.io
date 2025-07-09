import sqlite3
import argparse
from werkzeug.security import generate_password_hash

def add_user(db_path, username, email, password, role='user'):
    # Hash password
    pw_hash = generate_password_hash(password)
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Ensure "users" table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            token TEXT,
            locked_until DATETIME DEFAULT NULL,
            failed_attempts INTEGER NOT NULL DEFAULT 0
        );
    ''')
    # Insert new user
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, pw_hash, role)
        )
        conn.commit()
        print(f"User '{username}' added successfully with role '{role}'.")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting user: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a new user to lapas_chatbot.db')
    parser.add_argument('--db', default='lapas_chatbot.db', help='Path to SQLite database file')
    parser.add_argument('--username', required=True, help='Username for the new user')
    parser.add_argument('--email', required=True, help='Email for the new user')
    parser.add_argument('--password', required=True, help='Password for the new user')
    parser.add_argument('--role', default='user', choices=['user', 'admin'], help='Role for the new user')
    args = parser.parse_args()
    add_user(args.db, args.username, args.email, args.password, args.role)

# python3 insert_user.py --db lapas_chatbot.db --username namauser --email namaemail --password tulispassword --role admin
