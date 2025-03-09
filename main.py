from urllib import response
from typing import Annotated
from fastapi import FastAPI, Response, status, Header

from auth import authenticate_user
from admin_db import construct_part, construct_part_list, construct_borrowed_part, construct_borrowed_part_list



rights = ["all", "user", None]



app = FastAPI()



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
        return construct_part(parts_create(part))
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to create parts.",
        }

##Delete multiple parts by IDS
#TODO make sure parts are deleted properly, Error checking
#TODO delete parts from borrowed too
@app.delete("/parts/delete/{part_ids}")
async def parts_delete_by_ids(part_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_delete_by_ids
    rights = "all"
    if authenticate_user(token, rights):
        return parts_delete_by_ids(part_ids)
    else:
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
        return construct_part(parts_update_by_id(part_id, parameters))
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to update parts.",
        }



#BORROWED PARTS
##LISTING
###List all borrowed parts
@app.get("/parts/borrowed/list")
async def parts_borrowed_list():
    from admin_db import parts_borrowed_list
    return construct_borrowed_part_list(parts_borrowed_list())

###List borrowed parts by IDS
@app.get("/parts/borrowed/list/{part_ids}")
async def parts_borrowed_list_by_ids(part_ids: str):
    from admin_db import parts_borrowed_list_by_ids
    return construct_borrowed_part_list(parts_borrowed_list_by_ids(part_ids))


##BORROWED PART HANDLING
###Delete borrowed parts by IDS
#TODO make sure parts are deleted properly, Error checking
@app.delete("/parts/borrowed/delete/{part_ids}")
async def parts_borrowed_delete_by_ids(part_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_borrowed_delete_by_ids
    rights = "all"
    if authenticate_user(token, rights):
        return parts_borrowed_delete_by_ids(part_ids)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to delete borrowed parts.",
        }

###Borrow parts
#TODO in admin_db, works, but doesn't check min count
#TODO ERROR LIST OUT OF RANGE
@app.post("/parts/borrow/{part_ids}/{counts}")
async def parts_update(part_ids: str, counts: str, response: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_borrow
    rights = "user"
    if authenticate_user(token, rights):
        try:
            response.status_code = status.HTTP_200_OK
            return parts_borrow(part_ids, counts)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": str(e)}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to borrow parts.",
        }

###Return borrowed parts
@app.post("/parts/return/{borrowed_ids}")
async def parts_return_by_id(borrowed_ids: str, resonse: Response, token: Annotated[str | None, Header()] = None):
    from admin_db import parts_return
    rights = "user"
    if authenticate_user(token, rights):
        try:
            parts_return(borrowed_ids)
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": str(e)}
        else:
            return {
                "message": f"Successfuly returned parts {borrowed_ids}.",
            }
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to return parts.",
        }



#USER
##USER AUTHENTICATION
###Login user
@app.post("/login")
async def login_user(login: dict):
    from auth import login_user
    return login_user(login)

###Logout user
@app.post("/logout")
async def logout_user(token: Annotated[str | None, Header()] = None):
    from auth import logout_user
    return logout_user(token)


##USER HANDLING
###Create user
@app.post("/user/create")
async def user_create(user: dict, response: Response, token: Annotated[str | None, Header()] = None):
    from auth import create_user
    rights = "all"
    if authenticate_user(token, rights):
        return create_user(user["username"], user["password"], user["rights"])
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to create users.",
        }

###Delete multiple users by IDS
@app.post("/user/delete/{user_ids}")
async def user_create(user_ids: str, response: Response, token: Annotated[str | None, Header()] = None):
    from auth import users_delete_by_ids
    rights = "all"
    if authenticate_user(token, rights):
        return users_delete_by_ids(user_ids)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "message": f"Unauthorized to delete users.",
        }



#TODO History
#TODO Users
#TODO LIMITED COUNT/MIN COUNT
#TODO Delete tokens after expiration time
#TODO ERROR CHECKING