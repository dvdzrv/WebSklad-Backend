import sqlite3
import os

if __name__ == "__main__":
    db_con = sqlite3.connect('db/test.db')
    db_cursor = db_con.cursor()

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS parts
           (
               part_id      INTEGER PRIMARY KEY,
               category     TEXT NULL,
               sub_category TEXT NULL,
               name         TEXT NULL,
               value        TEXT NULL,
               count        INT  NOT NULL,
               min_count    INT       DEFAULT NULL,
               description  TEXT      DEFAULT NULL,
               create_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           );"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS borrowed
           (
               borrowed_id INTEGER PRIMARY KEY,
               part_id     INTEGER NOT NULL,
               user_id     INTEGER NOT NULL,
               count       INTEGER NOT NULL,
               FOREIGN KEY (part_id) REFERENCES parts (part_id),
               FOREIGN KEY (user_id) REFERENCES users (user_id)
           );"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS users
           (
               user_id     INTEGER PRIMARY KEY,
               username    TEXT NOT NULL,
               hashed_pass TEXT NOT NULL,
               rights      TEXT NOT NULL
           );"""
    )

    from auth import hash_password

    default_password = os.getenv("DEFAULT_PASSWORD")

    db_cursor.execute(
        f"""INSERT INTO users (user_id, username, hashed_pass, rights) VALUES (NULL, "admin", '{hash_password(default_password)}', "all");"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS history
           (
               history_id INTEGER PRIMARY KEY,
               user_id    INTEGER NOT NULL,
               operation  TEXT    NOT NULL,
               time       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (user_id) REFERENCES users (user_id)
           );"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS logon_users
           (
               logon_id       INTEGER PRIMARY KEY,
               user_id        INTEGER NOT NULL,
               token          TEXT    NOT NULL,
               generated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (user_id) REFERENCES users (user_id)
           );"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS schemas
           (
               schema_id          INTEGER PRIMARY KEY,
               schema_name        TEXT NOT NULL,
               part_ids           TEXT NOT NULL,
               part_counts        TEXT NOT NULL,
               schema_description TEXT DEFAULT NULL
           );"""
    )

    db_con.commit()
    db_con.close()

    from admin_db import input_data_to_db

    input_data_to_db()

    import uvicorn
    from main import app
    from uvicorn import run
    import multiprocessing

    multiprocessing.freeze_support()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)