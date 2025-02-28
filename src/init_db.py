import sqlite3

def init_db():
    DB_con = sqlite3.connect('test.db')

    DB_cursor = DB_con.cursor()

    DB_cursor.execute(
        """CREATE TABLE IF NOT EXISTS parts (ID int AUTO_INCREMENT PRIMARY KEY, category text, sub_category text null, name text, value text null, count int not null, min_count int null, create_time timestamp DEFAULT CURRENT_TIMESTAMP, updated_time timestamp DEFAULT CURRENT_TIMESTAMP)"""
    )

    DB_con.commit()

    DB_con.close()

def create_test_data():
    import parser
    DB_con = sqlite3.connect('test.db')
    DB_cursor = DB_con.cursor()
    DB_cursor.execute(
        f"""INSERT INTO parts (id, name, category, sub_category, value, count, min_count) values {parser.parse()}"""
    )

    DB_con.commit()

    DB_con.close()

def list_all():
    DB_con = sqlite3.connect('test.db')
    DB_cursor = DB_con.cursor()
    DB_cursor.execute(
        """SELECT * FROM parts"""
    )

    rows = DB_cursor.fetchall()

    DB_con.commit()

    DB_con.close()

    return rows

if __name__ == "__main__":
    init_db()
    holder = input("Do you want to input data? (Y/n)")
    if holder == "y" or holder == "Y" or holder == "":
        create_test_data()

    holder = input("Do you want to list data? (Y/n)")
    if holder == "y" or holder == "Y" or holder == "":
        rows = list_all()
        for row in rows:
            print(row)

