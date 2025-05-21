import sqlite3
from uuid import uuid4


def init_db():
    try:
        db_con = sqlite3.connect('db/test.db')
        db_cursor = db_con.cursor()

        db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS parts (part_id INTEGER PRIMARY KEY, category TEXT NULL, sub_category TEXT NULL, name TEXT NULL, value TEXT NULL, count INT NOT NULL, min_count INT DEFAULT NULL, description TEXT DEFAULT NULL, create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
        )

        db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS borrowed (borrowed_id INTEGER PRIMARY KEY, part_id INTEGER NOT NULL, user_id INTEGER NOT NULL, count INTEGER NOT NULL, FOREIGN KEY(part_id) REFERENCES parts(part_id), FOREIGN KEY(user_id) REFERENCES users(user_id));"""
        )

        db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL, hashed_pass TEXT NOT NULL, rights TEXT NOT NULL);"""
        )

        from auth import hash_password
        default_password = uuid4().hex

        db_cursor.execute(
            f"""INSERT INTO users (user_id, username, hashed_pass, rights) VALUES (NULL, "admin", '{hash_password(default_password)}', "all");"""
        )

        db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS history (history_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, operation TEXT NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(user_id));"""
        )

        db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS logon_users (logon_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, token TEXT NOT NULL, generated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users (user_id));"""
        )

        db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS schemas (schema_id INTEGER PRIMARY KEY, schema_name TEXT NOT NULL, part_ids TEXT NOT NULL, part_counts TEXT NOT NULL, schema_description TEXT DEFAULT NULL);"""
        )

        db_con.commit()
        db_con.close()

        for i in range(20):
            print("DEFAULT PASSWORD SET TO: ", default_password)

    except sqlite3.OperationalError:
        print("Database already exists.")