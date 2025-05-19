import sqlite3
import os
from types import NoneType

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)



#DB ACCESS
##QUERY DB
def query_db(query: str):
    db_con = sqlite3.connect('db/test.db')
    db_cursor = db_con.cursor()
    db_cursor.execute(query)
    rows = db_cursor.fetchall()
    db_con.commit()
    db_con.close()
    return rows



#PART DICTIONARIES
##PARTS
###Construct part dictionary
def construct_part(row):
    if not row:
        return None
    return {"part_id": row[0],
                 "category": row[1],
                 "sub_category": row[2],
                 "name": row[3],
                 "value": row[4],
                 "count": row[5],
                 "min_count": row[6],
                 "created": row[7],
                 "updated": row[8]
               }

###Construct list of part dictionaries
def construct_part_list(rows):
    if not rows:
        return []
    parts = []
    for row in rows:
        parts.append(construct_part(row))
    return parts


##BORROWED PARTS
###Construct borrowed part dictionary
def construct_borrowed_part(row):
    return {
        "borrowed_id": row[0],
        "part_id": row[1],
        "count": row[2],
        "user_id": row[3],
    }

###Construct list borrowed part dictionaries
def construct_borrowed_part_list(rows):
    parts = []
    for row in rows:
        parts.append(construct_borrowed_part(row))
    return parts



#DB TABLE HANDLING
##INICIALIZATION OF TALBLES
def init_db():
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
    default_password = os.getenv("DEFAULT_PASSWORD")

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

    holder = input("Do you want to input data? (Y/n)")
    if holder == "y" or holder == "Y" or holder == "":
        input_data_to_db()
        holder = input("Do you want to list data? (Y/n)")
        if holder == "y" or holder == "Y" or holder == "":
            rows = parts_list_all()
            for row in rows:
                print(row)

##Reinicialazion of tables
def reinit_db():
    os.remove("db/test.db")
    init_db()


##TABLE DELETION
###Drop parts table
def delete_parts():
    query_db(
        """DROP TABLE IF EXISTS parts"""
    )

###Truncate parts table
def truncate_parts():
    query_db(
        """DELETE FROM parts"""
    )


##INSERTING INTO TABLES
###Insert parts from csv into parts table
def input_data_to_db():
    from db import parser
    query_db(
        f"""INSERT INTO parts (part_id, category, sub_category, name, value, count, min_count, description) values {parser.parse()}"""
    )




#PARTS
##LIST PARTS
###List all parts
def parts_list_all():
    return query_db(
        f"""SELECT * FROM parts"""
    )

###List single part by id
def parts_list_by_id(id):
    return query_db(
        f"""SELECT * FROM parts WHERE part_id ={id}"""
    )[0]

###List multiple parts by id
def parts_list_by_ids(part_ids: str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    part_ids_str = ""
    for i in range(len(part_ids)):
        part_ids_str += f"{part_ids[i]},"
    part_ids_str = part_ids_str[:-1]

    return query_db(
        f"""SELECT * FROM parts WHERE part_id IN ({part_ids_str})"""
    )

##SEARCH PARTS
###Search parts by name
def parts_search_by_name(name):
    return query_db(f"""SELECT * FROM parts WHERE CONCAT(parts.name, ' ', parts.value) LIKE '%{name}%'""")

###Search parts by category
def parts_search_by_category(category):
    return query_db(f"""SELECT * FROM parts WHERE category LIKE '%{category}%'""")

###Search parts by subcategory
def parts_search_by_sub_category(sub_category):
    return query_db(f"""SELECT * FROM parts WHERE sub_category LIKE '%{sub_category}%'""")


##PART HANDLING
###Create part
def parts_create(part):
    part_parameters = ["name", "category", "sub_category", "value", "count", "min_count"]
    for parameter in part_parameters:
        if part.get(parameter) is None:
            part.update({parameter: "NULL"})

    db_con = sqlite3.connect('db/test.db')
    db_cursor = db_con.cursor()

    db_cursor.execute(
        f"""INSERT INTO parts (part_id, category, sub_category, name, value, count, min_count) values (NULL, ?, ?, ?, ?, ?, ?);""",
        (part["category"], part["sub_category"], part["name"], part["value"], part["count"], part["min_count"]))

    db_con.commit()
    db_con.close()

    return query_db(f"""SELECT * FROM parts ORDER BY part_id DESC LIMIT 1""")[0]

###Delete multiple parts by IDS
def parts_delete_by_ids(part_ids: str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    part_ids_str = ""
    for i in range(len(part_ids)):
        part_ids_str += f"{part_ids[i]},"
    part_ids_str = part_ids_str[:-1]

    query_db(f"""DELETE FROM parts WHERE part_id IN ({part_ids_str})""")
    query_db(f"""DELETE FROM borrowed WHERE part_id IN ({part_ids_str})""")

    return {"message": f"parts {part_ids} deleted"}


###Update part by ID
def parts_update_by_id(part_id:int, parameters: dict):
    update = ""
    for parameter in parameters.keys():
        update += f"{parameter} = \"{parameters[parameter]}\","
    update = update[:-1]
    query_db(f"""UPDATE parts SET {update} WHERE part_id = {part_id}""")

    return query_db(f"""SELECT * FROM parts WHERE part_id = {part_id}""")[0]



#BORROWED PARTS
##LIST BORROWED PARTS
###List all borrowed parts
def parts_borrowed_list():
    return query_db(
        """SELECT borrowed_id, part_id, count, user_id FROM borrowed"""
    )


###List multiple borrowed parts by IDS
def parts_borrowed_list_by_ids(part_ids: str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    part_ids_str = ""
    for i in range(len(part_ids)):
        part_ids_str += f"{part_ids[i]},"

    part_ids_str = part_ids_str[:-1]

    return query_db(
        f"""SELECT * FROM borrowed WHERE borrowed_id IN ({part_ids_str})"""
    )


##PART HANDLING
###Delete borrowed parts by IDS
def parts_borrowed_delete_by_ids(part_ids: str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    part_ids_str = ""
    for i in range(len(part_ids)):
        part_ids_str += f"{part_ids[i]},"
    part_ids_str = part_ids_str[:-1]

    query_db(f"""DELETE FROM borrowed WHERE borrowed_id IN ({part_ids_str})""")

    return {"message": f"Borrowed parts {part_ids} deleted."}

###Borrow parts by IDS and COUNTS
def parts_borrow(part_ids:str, counts:str, token:str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    counts = counts.split(',')
    counts = [int(id) for id in counts]

    current_part_is_okay = True
    messages = []

    #CHECK IF NUMBER OF PART IDS AND PART COUNTS MATCH
    if len(part_ids) != len(counts):
        messages += {
            "message": "Length of IDS and COUNTS do not match."
        }
        return messages

    for i in range(len(part_ids)):
        part = parts_list_by_id(part_ids[i])

        #CHECK IF PART IS FOUND
        if not part:
            messages += {
                "message": f"Part not found.",
                "part_id": part_ids[i],
            }
            current_part_is_okay = False

        part = construct_part(part)

        #CHECK IF THERE IS ENOUGH PARTS
        if part["count"] - counts[i] < 0:
            messages += {
                "message": f"There is not enough of part.",
                "part_id": part_ids[i],
            }
            current_part_is_okay = False

        #CHECK IF BORROWING WON'T LEAVE FEWER PARTS THAN MIN COUNT
        if type(part["min_count"]) is not NoneType:
            if (part["count"] - counts[i]) < part["min_count"]:
                messages += {
                    "message": f"Borrowing leaves less parts in storage than min val.",
                    "part_id": part_ids[i],
                }

        if current_part_is_okay:
            #SET PART COUNTS IN PARTS TABLE
            parts_update_by_id(part_ids[i], {"count": part["count"] - counts[i]})

            from auth import get_user_id_by_token
            #ADD BORROWED PARTS INTO BORROWED TABLE
            query_db(f"""INSERT INTO borrowed (borrowed_id, part_id, count, user_id) VALUES (NULL, {part_ids[i]}, {counts[i]}, {get_user_id_by_token(token)})""")

    return messages

    #RETURN BORROWED PARTS
    str = ""
    for part in part_ids:
        str += f"{part},"
    str = str[:-1]
    return query_db(f"""SELECT part_id, count FROM borrowed WHERE part_id IN ({str})""")

###Return borrowed parts by IDS of borrowed parts
def parts_return(borrowed_ids:str):
    borrowed_ids = borrowed_ids.split(',')
    borrowed_ids = [int(id) for id in borrowed_ids]

    for i in range(len(borrowed_ids)):
        try:
            borrowed_part = construct_borrowed_part(
                parts_borrowed_list_by_ids(
                    str(borrowed_ids[i]))[0])
        except IndexError:
            raise Exception(f"Part {borrowed_ids[i]} not found. Parts before this returned!")

        part = construct_part(
            parts_list_by_id(
                construct_borrowed_part(
                    parts_borrowed_list_by_ids(
                        str(borrowed_ids[i])
                    )[0]
                )["part_id"]
            )
        )

        if part == [] or borrowed_part == []:
            raise Exception({
                "message": "Part {borrowed_ids[i]} not found. Parts before this returned successfully.",
                "returned_parts": borrowed_ids[:i],
                "part_not_found": borrowed_ids[i],
                "parts_not_returned": borrowed_ids[i:],
            })

        parts_update_by_id(part["part_id"], {"count": part["count"] + borrowed_part["count"]})

        parts_borrowed_delete_by_ids(str(borrowed_ids[i]))















#INTERFACE TO INTERACT WITH DB
#TODO MAKE BETTER INTERFACE
if __name__ == "__main__":
    match input(
        "What category of action would you like to do?\n"
        "Handle database (DB)\n"
        "List parts (L)\n"
        "List borrowed parts (B)\n"
    ):

        case "DB":
            match input(
                "What type of action would you like to do?\n"
                "Query database by SQL (Q)\n"
                "Initialize tables (I)\n"
                "Reinitialize tables (R)\n"
                "Delete parts table (D)\n"
                "Truncate parts table (T)\n"
                "Insert data to table from CSV file (C)"
            ):
                case "Q":
                    try:
                        print(
                            query_db(
                                input("Insert sql query: ")))
                    except Exception as e:
                        print(e)

                case "I":
                    try:
                        init_db()
                    except Exception as e:
                        print(e)

                case "R":
                    try:
                        reinit_db()
                    except Exception as e:
                        print(e)

                case "D":
                        try:
                            delete_parts()
                        except Exception as e:
                            print(e)

                case "C":
                        try:
                            input_data_to_db()
                        except Exception as e:
                            print(e)

        case "L":
            print(parts_list_all())

        case "B":
            print(parts_borrowed_list())



