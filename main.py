#from urllib import response
from typing import Annotated
from fastapi import FastAPI, Response, status, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Strict

from auth import authenticate_user, construct_user_list, construct_public_user_list
from admin_db import construct_part, construct_part_list, construct_borrowed_part, construct_borrowed_part_list
from history import history_add_operation
from imgs import *


#rights = ["all", "user", None]


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:*",
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#PARTS
##LISTING
###List all parts
@app.get("/parts/list")
async def parts_list_all():
    from admin_db import parts_list_all
    return construct_part_list(parts_list_all())

###List single part by ID
@app.get("/parts/list/{part_id}")
async def parts_list_by_id(part_id: int):
    from admin_db import parts_list_by_id
    return  construct_part(parts_list_by_id(part_id))

###List multiple parts by IDS
#TODO Error checking, if part is not found
@app.get("/parts/list/multiple/{part_ids}")
async def parts_list_by_ids(part_ids: str):
    from admin_db import parts_list_by_ids
    return construct_part_list(parts_list_by_ids(part_ids))


##SEARCHING
###Search in parts by name
@app.get("/parts/search/{name}")
async def parts_search_by_name(name: str):
    from admin_db import parts_search_by_name
    return construct_part_list(parts_search_by_name(name))

###Search in parts by category
@app.get("/parts/search/category/{category}")
async def parts_search_by_category(category: str):
    from admin_db import parts_search_by_category
    return construct_part_list(parts_search_by_category(category))

###Search in parts by subcategory
@app.get("/parts/search/sub_category/{sub_category}")
async def parts_search_by_category(sub_category: str):
    from admin_db import parts_search_by_sub_category
    return construct_part_list(parts_search_by_sub_category(sub_category))


##PART HANDLING
###Create part
#TODO Create multiple parts, Error checking
@app.post("/parts/create")
async def parts_create(part: dict, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_create
    rights = "all"
    if authenticate_user(token, rights):
        history_add_operation(token, f"User created part {part["name"] + " " + part["value"]}.")
        return construct_part(parts_create(part))
    else:
        history_add_operation(token, f"User failed to create part {part["name"] + part["value"]}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to create parts.",
        }

##Delete multiple parts by IDS
#TODO make sure parts are deleted properly, Error checking
@app.delete("/parts/delete/{part_ids}")
async def parts_delete_by_ids(part_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_delete_by_ids
    rights = "all"
    if authenticate_user(token, rights):
        history_add_operation(token, f"User deleted parts {part_ids}.")
        return parts_delete_by_ids(part_ids)
    else:
        history_add_operation(token, f"User failed to delete parts {part_ids}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to delete parts.",
        }

##Update single part
#TODO Update multiple parts, Error checking
@app.put("/parts/update/{part_id}")
async def parts_update_by_id(part_id:int, parameters: dict, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_update_by_id
    rights = "all"
    if authenticate_user(token, rights):
        history_add_operation(token, f"User updated part {part_id}.")
        return construct_part(parts_update_by_id(part_id, parameters))
    else:
        history_add_operation(token, f"User failed to update part {part_id}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to update parts.",
        }



#BORROWED PARTS
##LISTING
###List all borrowed parts
@app.get("/parts/borrowed/list")
async def parts_borrowed_list(response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_borrowed_list
    rights = "user"
    if authenticate_user(token, rights):
        return construct_borrowed_part_list(parts_borrowed_list())
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to list borrowed parts.",
        }

###List borrowed parts by IDS
@app.get("/parts/borrowed/list/{part_ids}")
async def parts_borrowed_list_by_ids(part_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_borrowed_list_by_ids
    rights = "user"
    if authenticate_user(token, rights):
        return construct_borrowed_part_list(parts_borrowed_list_by_ids(part_ids))
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to list borrowed parts.",
        }



##BORROWED PART HANDLING
###Delete borrowed parts by IDS
#TODO make sure parts are deleted properly, Error checking
@app.delete("/parts/borrowed/delete/{borrowed_ids}")
async def parts_borrowed_delete_by_ids(borrowed_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_borrowed_delete_by_ids
    rights = "all"
    if authenticate_user(token, rights):
        history_add_operation(token, f"User deleted borrowed parts {borrowed_ids}.")
        return parts_borrowed_delete_by_ids(borrowed_ids)
    else:
        history_add_operation(token, f"User failed to delete borrowed parts {borrowed_ids}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to delete borrowed parts.",
        }

###Borrow parts
#TODO in admin_db, works, but doesn't check min count
@app.post("/parts/borrow/{part_ids}/{counts}")
async def parts_update(part_ids: str, counts: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_borrow
    rights = "user"

    if authenticate_user(token, rights):
        messages = parts_borrow(part_ids, counts, token)

        if messages:
            response.status_code = status.HTTP_207_MULTI_STATUS
            history_add_operation(token, f"User tried borrowing parts {part_ids}, {messages}.")
            return messages
        else:
            return {
                "message": "Borrowed parts."
            }
    else:
        history_add_operation(token, f"User failed borrowing parts {part_ids}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to borrow parts.",
        }

###Return borrowed parts
@app.post("/parts/return/{borrowed_ids}")
async def parts_return_by_id(borrowed_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_return
    rights = "user"
    if authenticate_user(token, rights):
        try:
            parts_return(borrowed_ids)
        except Exception as e:
            history_add_operation(token, f"User failed returning parts {borrowed_ids}.")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": str(e)}
        else:
            history_add_operation(token, f"User borrowed parts {borrowed_ids}.")
            return {
                "message": f"Successfully returned parts {borrowed_ids}.",
            }
    else:
        history_add_operation(token, f"User failed returning parts {borrowed_ids}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to return parts.",
        }



#USER
##USER AUTHENTICATION
###Login user
#TODO Poslať aj práva
@app.post("/login")
async def login_user(login: dict, response: Response):
    from auth import login_user
    try:
        return login_user(login)
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": str(e),
        }


###Logout user
@app.post("/logout")
async def logout_user(token: Annotated[str | None, Header()] = None):
    from auth import logout_user
    history_add_operation(token, "User logged out.")
    return logout_user(token)


##USER HANDLING
###Create user
@app.post("/user/create")
async def user_create(user: dict, response: Response, token: Annotated[str | None, Header()] = None):
    from auth import create_user
    rights = "all"
    if authenticate_user(token, rights):
        history_add_operation(token, f"User created user {user["username"]}.")
        return create_user(user["username"], user["password"], user["rights"])
    else:
        history_add_operation(token, f"User failed to created user {user["username"]}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to create users.",
        }

###Delete multiple users by IDS
@app.delete("/user/delete/{user_ids}")
async def user_create(user_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from auth import users_delete_by_ids
    rights = "all"
    if authenticate_user(token, rights):
        history_add_operation(token, f"User deleted users {user_ids}.")
        users_delete_by_ids(user_ids)
        return {
            "message": f"Successfully deleted users.",
        }
    else:
        history_add_operation(token, f"User failed to delete users {user_ids}.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to delete users.",
        }

###List users by IDS
@app.get("/user/list/{user_ids}")
async def users_list_by_ids(user_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from auth import list_users_by_ids
    rights = "all"
    if authenticate_user(token, rights):
        history_add_operation(token, f"Listed users.")
        return construct_public_user_list(list_users_by_ids(user_ids))
    else:
        history_add_operation(token, f"Failed to list users.")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to list users.",
        }



#List history
@app.get("/history")
async def history(response: Response, token: Annotated[str | None, Header()] = None):
    from history import list_history, construct_history_list
    rights = "user"
    if authenticate_user(token, rights):
        return construct_history_list(list_history())
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to list history.",
        }

#Return image by id
@app.get("/image/{part_id}")
async def images(part_id: int, response: Response):
    img_path = get_img_by_id(part_id)
    if not img_path is None:
        return FileResponse(img_path)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": f"Image for ID:{part_id} not found.",
        }

@app.get("/images")
async def images_all():
    pass


@app.get("/schemas")
async def list_schemas():
    from admin_db import construct_schema_list, query_db
    return construct_schema_list(query_db("""SELECT * FROM schemas"""))

@app.get("/schema/image/{schema_id}")
async def get_image_of_schema(schema_id: int, response: Response):
    from admin_db import query_db
    try:
        schema_name = query_db(f"SELECT schema_name FROM schemas WHERE schema_id = '{schema_id}'")
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": str(e),
        }

    print(schema_name[0][0])
    return FileResponse("./db/schemas/" + str(schema_name[0][0]) + ".png")


#TODO LIMITED COUNT/MIN COUNT - vyberie ale upozorní


#TODO ERROR CHECKING
#TODO LIST ALL IMGS



#TODO Košík v db na BackEnde alebo zväčiť token expiring - zväčšili sme token čas
