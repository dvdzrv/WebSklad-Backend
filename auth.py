from admin_db import query_db
from uuid import uuid4
import hashlib
import datetime



token_valid_time = datetime.timedelta(minutes=2)



#USER DICTIONARIES
#PRIVATE USER DICTIONARIES, UNSAFE!!!!!
##Construct user dictionary
def construct_user(row):
    return {
        "user_id": row[0],
        "username": row[1],
        "hashed_pass": row[2],
        "rights": row[3],
    }


##Construct list of user dictionaries
def construct_user_list(rows):
    users = []
    for row in rows:
        users.append(construct_user(row))
    return users


#PUBLIC USER DICTIONARIES, SAFE!!!!!
##Construct public user dictionary
def construct_public_user(row):
    return {
        "user_id": row[0],
        "username": row[1],
        "rights": row[2],
    }


##Construct list of public user dictionaries
def construct_public_user_list(rows):
    users = []
    for row in rows:
        users.append(construct_public_user(row))
    return users



#PASSWORD HANDLING
##Hash password
def hash_password(password: str) -> str:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password



#USERS
##USER HANDLING
###List all users
def list_users():
    return query_db(
        f"""SELECT user_id, username, rights FROM users"""
    )

###List users by IDS
def list_users_by_ids(user_ids:str):
    print(user_ids)
    user_ids = user_ids.split(",")
    user_ids = [int(user_id) for user_id in user_ids]

    user_ids_str = ""
    for user_id in user_ids:
        user_ids_str += f"'{user_id}',"
    user_ids_str = user_ids_str[:-1]

    return query_db(
        f"""SELECT user_id, username, rights FROM users WHERE user_id IN ({user_ids_str})"""
    )

###Create user
def create_user(username: str, password: str, rights: str):
    query_db(
        f"""INSERT INTO users (user_id, username, hashed_pass, rights) VALUES(NULL, {username}, '{hash_password(password)}', '{rights}'));"""
    )

    return construct_user(
        query_db(
            f"""SELECT user_id, username, rights FROM users WHERE username = '{username}'"""
        )[0]
    )

###Delete user
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



#USER AUTHENTICATION AND AUTHORIZATION

#GET USER ID FROM TOKEN
def get_user_id_by_token(token:str):
    user_id = query_db(
        f"""SELECT user_id FROM logon_users WHERE token='{token}';"""
    )[0][0]

    user_id = str(user_id)

    return user_id

#USER AUTHENTICATION
##VERIFY IF USER IS LOGGED IN
def verify_logon_user(token: str) -> bool:
    logon_user = query_db(
        f"""SELECT * FROM logon_users WHERE token='{token}';"""
    )

    if logon_user != []:
        return True
    else:
        return False


##CHECK IF USER'S TOKEN IS VALID AND UNEXPIRED
def check_token_validation(token: str):
    now = datetime.datetime.now()
    token_init_time = query_db(
        f"""SELECT generated_time FROM logon_users WHERE token='{token}';"""
    )[0][0]

    token_init_time = datetime.datetime.strptime(token_init_time, "%Y-%m-%d %H:%M:%S")
    if now - token_init_time - datetime.timedelta(hours=1) < token_valid_time:
        return True
    else:
        query_db(
            f"""DELETE FROM logon_users WHERE token='{token}';"""
        )
        return False



#USER AUTHORIZATION
##GET USER RIGHTS BY TOKEN
def get_user_rights(token:str):
    user_id = query_db(
        f"""SELECT user_id FROM logon_users WHERE token='{token}';"""
    )[0][0]

    user_rights = query_db(
        f"""SELECT rights FROM users WHERE user_id='{user_id}';"""
    )[0][0]

    return user_rights


##VERIFY USER RIGHTS
def verify_user_rights(token:str, rights: str) -> bool:
    if not verify_logon_user(token) or not check_token_validation(token):
        return False
    else:
        user_id = query_db(
            f"""SELECT user_id FROM logon_users WHERE token='{token}';"""
        )[0][0]
        rights_from_db = query_db(
            f"""SELECT rights FROM users WHERE user_id='{user_id}';"""
        )[0][0]
        if rights != rights_from_db and rights_from_db != "all":
            return False
        else: return True

##AUTHENTICATE AND AUTHORIZE USER
def authenticate_user(token:str, rights:str):
    if token == None or rights == "":
        return False
    elif verify_user_rights(token, rights):
        return True

##DELETE EXPIRED TOKENS
def delete_expired_tokens():
    now = datetime.datetime.now()
    tokens = query_db(
        f"""SELECT logon_id, generated_time FROM logon_users;"""
    )

    from history import history_add_operation

    for token in tokens:
        token_init_time = datetime.datetime.strptime(token[1], "%Y-%m-%d %H:%M:%S")
        if now - token_init_time - datetime.timedelta(hours=1) < token_valid_time:
            history_add_operation(token, f"Deleted expired token.")
            query_db(
                f"""DELETE FROM logon_users WHERE logon_id='{token[0]}';"""
            )



##USER HANDLING
###Login user
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
        f"""INSERT INTO logon_users (logon_id, user_id, token) VALUES (NULL, {user["user_id"]}, '{token}');"""
    )

    from history import history_add_operation
    history_add_operation(token, f"User logged in.")

    return {
                "token": token,
            }

###Logout user
def logout_user(token: str):
    if not verify_logon_user(token):
        return {
            "message": "User not even logged in.",
        }

    query_db(
        f"""DELETE FROM logon_users WHERE token='{token}';"""
    )

    return {
        "message": "Logged out.",
    }




if __name__ == "__main__":
    print(hash_password("jožo"))
