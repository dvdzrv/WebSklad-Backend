import sqlite3
from types import NoneType


def query_db(query: str):
    db_con = sqlite3.connect('db/test.db')
    db_cursor = db_con.cursor()
    db_cursor.execute(query)
    rows = db_cursor.fetchall()
    db_con.commit()
    db_con.close()
    return rows


def construct_part(row):
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

def construct_part_list(rows):
    parts = []
    for row in rows:
        parts.append(construct_part(row))
    return parts









#DB STUFF
#INICIALIZACIA DB
def init_db():
    db_con = sqlite3.connect('db/test.db')

    db_cursor = db_con.cursor()

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS parts (part_id integer PRIMARY KEY, category text, sub_category text null, name text, value text null, count int not null, min_count int null, create_time timestamp DEFAULT CURRENT_TIMESTAMP, updated_time timestamp DEFAULT CURRENT_TIMESTAMP);"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS borrowed (borrowed_id integer PRIMARY KEY, part_id integer NOT NULL, count integer NOT NULL, FOREIGN KEY(part_id) REFERENCES parts(part_id));"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY, username text NOT NULL, rights text NOT NULL);"""
    )

    db_cursor.execute(
        """INSERT INTO users (user_id, username, rights) VALUES (NULL, "admin", "all");"""
    )

    db_cursor.execute(
        """CREATE TABLE IF NOT EXISTS history (history_id integer PRIMARY KEY, user_id integer NOT NULL, operation text NOT NULL, time timestamp DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(user_id));"""
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

def reinit_db():
    query_db("""DROP TABLE history;""")
    query_db("""DROP TABLE borrowed;""")
    query_db("""DROP TABLE users;""")
    query_db("""DROP TABLE parts;""")
    init_db()

#ZMAZANIE TABULKY PARTS
def delete_parts():
    db_con = sqlite3.connect('db/test.db')

    db_cursor = db_con.cursor()

    db_cursor.execute(
        """DROP TABLE IF EXISTS parts"""
    )

    db_con.commit()

    db_con.close()


#ZMAZANIE OBSAHU PARTS
def truncate_parts():
    db_con = sqlite3.connect('db/test.db')

    db_cursor = db_con.cursor()

    db_cursor.execute(
        """DELETE FROM parts"""
    )

    db_con.commit()

    db_con.close()


#VKLADANIE DO DB
#VLOŽENIE Z CSV
def input_data_to_db():
    from db import parser
    db_con = sqlite3.connect('db/test.db')

    db_cursor = db_con.cursor()

    db_cursor.execute(
        f"""INSERT INTO parts (part_id, category, sub_category, name, value, count, min_count) values {parser.parse()}"""
    )

    db_con.commit()

    db_con.close()












#LIST PARTS FROM DB
#LIST ALL PARTS
def parts_list_all():
    return query_db(
        f"""SELECT * FROM parts"""
    )


#LIST PART BY ID
def parts_list_by_id(id):
    return query_db(
        f"""SELECT * FROM parts WHERE part_id ={id}"""
    )[0]


#LIST MULTIPLE PARTS BY IDS
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

#SEARCH IN PARTS
#BY NAME
def parts_search_by_name(name):
    return query_db(f"""SELECT * FROM parts WHERE name LIKE '%{name}%'""")

#BY CATEGORY
def parts_search_by_category(category):
    return query_db(f"""SELECT * FROM parts WHERE category LIKE '%{category}%'""")

#BY SUBCATEGORY
def parts_search_by_sub_category(sub_category):
    return query_db(f"""SELECT * FROM parts WHERE sub_category LIKE '%{sub_category}%'""")


#CREATE PART
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


#DELETE PARTS
def parts_delete_by_ids(part_ids: str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    part_ids_str = ""
    for i in range(len(part_ids)):
        part_ids_str += f"{part_ids[i]},"
    part_ids_str = part_ids_str[:-1]

    query_db(f"""DELETE FROM parts WHERE part_id IN ({part_ids_str})""")

    return {"message": f"parts {part_ids} deleted"}


#UPDATE PART
def parts_update_by_id(part_id:int, parameters: dict):
    update = ""
    for parameter in parameters.keys():
        update += f"{parameter} = \"{parameters[parameter]}\","
    update = update[:-1]
    query_db(f"""UPDATE parts SET {update} WHERE part_id = {part_id}""")

    return query_db(f"""SELECT * FROM parts WHERE part_id = {part_id}""")[0]


#LIST BORROWED PARTS
def parts_borrowed_list():
    return query_db(
        """SELECT * FROM borrowed"""
    )


#LIST BORROWED PARTS BY IDS
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

#DELETE BORROWED PARTS BY IDS
def parts_borrowed_delete_by_ids(part_ids: str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    part_ids_str = ""
    for i in range(len(part_ids)):
        part_ids_str += f"{part_ids[i]},"
    part_ids_str = part_ids_str[:-1]

    query_db(f"""DELETE FROM borrowed WHERE borrowed_id IN ({part_ids_str})""")

    return {"message": f"Borrowed parts {part_ids} deleted."}










#BORROW PARTS
def parts_borrow(part_ids:str, counts:str):
    part_ids = part_ids.split(',')
    part_ids = [int(id) for id in part_ids]

    counts = counts.split(',')
    counts = [int(id) for id in counts]

    #CHECK IF NUMBER OF PART IDS AND PART COUNTS MATCH
    if len(part_ids) != len(counts):
        raise Exception("Length of IDS and COUNTS do not match.")


    for i in range(len(part_ids)):
        part = parts_list_by_id(part_ids[i])

        #CHECK IF PART IS FOUND
        if part == []:
            raise Exception(f"Part {part_ids[i]} not found.")

        part = construct_part(part)

        #CHECK IF THERE IS ENOUGH PARTS
        if part["count"] - counts[i] < 0:
            raise Exception(f"There is not enough of part: {part_ids[i]}. You requested {counts[i] - part["count"]} more parts.")

        #CHECK IF BORROWING WON'T LEAVE FEWER PARTS THAN MIN COUNT
        #TODO FINISH
        #if type(part["min_count"]) != NoneType:
        #    if part["count"] - counts[i] < part["min_count"]:
        #        return {
        #            "message:" f"Part {part_ids[i]} you requested will be borrowed, but it leaves less parts in storage, than minimal count.",
        #        }

        #SET PART COUNTS IN PARTS TABLE
        parts_update_by_id(part_ids[i], {"count": part["count"] - counts[i]})



        #ADD BORROWED PARTS INTO BORROWED TABLE
        query_db(f"""INSERT INTO borrowed (borrowed_id, part_id, count) VALUES (NULL, {part_ids[i]}, {counts[i]})""")



    #RETURN BORROWED PARTS
    str = ""
    for part in part_ids:
        str += f"{part},"
    str = str[:-1]
    return query_db(f"""SELECT part_id, count FROM borrowed WHERE part_id IN ({str})""")









#TODO MAKE BETTER INTERFACE
if __name__ == "__main__":
    match input(
        "What action would you like to do? (REINIT[R]/Delete parts table[D]/Truncate parts table[T]/Initialize DB[I]/Add parts to DB[A]/List all parts in DB[L])"):
        case "R":
            reinit_db()

        case "D":
            delete_parts()

        case "T":
            truncate_parts()

        case "I":
            init_db()

        case "L":
            rows = parts_list_all()
            for row in rows:
                print(row)

        case "A":
            input_data_to_db()
            holder = input("Do you want to list data? (Y/n)")
            if holder == "y" or holder == "Y" or holder == "":
                rows = parts_list_all()
                for row in rows:
                    print(row)
