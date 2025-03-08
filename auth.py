from admin_db import query_db
from uuid import uuid4
import hashlib

def construct_user(row):
    return {
        "user_id": row[0],
        "username": row[1],
        "hashed_pass": row[2],
        "rights": row[3],
    }

def construck_user_list(rows):
    users = []
    for row in rows:
        users.append(construct_user(row))
    return users







def hash_password(password: str) -> str:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def create_user(username: str, password: str, rights: str):
    query_db(
        f"""INSERT INTO users (user_id, username, hashed_pass, rights) VALUES(NULL, {username}, '{hash_password(password)}', '{rights}'));"""
    )

    return query_db(
        f"""SELECT user_id FROM users WHERE username = '{username}';"""
    )


def users_delete_by_ids(user_ids:str):
    user_ids = user_ids.split(",")
    user_ids = [int(user_id) for user_id in user_ids]

    user_ids_str = ""
    for i in range(len(user_ids)):
        user_ids_str += f"{user_ids[i]},"
    user_ids_str = user_ids_str[:-1]

    query_db(
        f"""DELETE FROM users WHERE user_id IN ({user_ids_str});"""
    )




def login_user(login:dict) -> dict:
    user = query_db(
        f"""SELECT * FROM users WHERE username='{login["username"]}';"""
    )[0]

    if user == []:
        raise Exception("User not found.")


    user = construct_user(user)

    print(hash_password(login["password"]) == user["hashed_pass"])

    if hash_password(login["password"]) == user["hashed_pass"]:
        token = uuid4().hex
    else:
        raise Exception("Wrong password.")

    query_db(
        f"""INSERT INTO logon_users (logon_id, user_id, token, generated_time) VALUES (NULL, {user["user_id"]}, {token}, NULL);"""
    )

    return {
                "token": token,
            }

def verify_logon_user(token: str) -> bool:
    logon_user = query_db(
        f"""SELECT * FROM logon_users WHERE token='{token}';"""
    )

    if logon_user != []:
        return True
    else:
        return False


def verify_user_rights(token:str, rights: str) -> bool:
    if not verify_logon_user(token):
        return False
    else:
        rights_from_db = query_db(
            f"""SELECT rights FROM logon_users WHERE token='{token}';"""
        )[0]
        if rights != rights:
            return False
        else: return True
















if __name__ == "__main__":
    print(hash_password("jožo"))
