from fastapi import FastAPI
import sqlite3
from typing import List
from pydantic import BaseModel

#BASE MODELS
class Part(BaseModel):
    category: str
    sub_category: str | None = None
    name: str
    value: str | None = None
    count: int
    min_count: int | None = None

app = FastAPI()

#LIST ALL PARTS
@app.get("/parts/list")
async def parts_list_all():
    from admin_db import parts_list_all
    rows = parts_list_all()
    parts = []
    for i in range(len(rows)):
        parts.append(
            {"part_id": rows[i][0],
             "category": rows[i][1],
             "sub_category": rows[i][2],
             "name": rows[i][3],
             "value": rows[i][4],
             "count": rows[i][5],
             "min_count": rows[i][6],
             "created": rows[i][7],
             "updated": rows[i][8], }
        )
    return parts

#LIST PART BY ID
@app.get("/parts/list/{part_id}")
async def parts_list_by_id(part_id: int):
    from admin_db import parts_list_by_id
    rows = parts_list_by_id(part_id)
    return{0:
               {"part_id": rows[0][0],
                 "category": rows[0][1],
                 "sub_category": rows[0][2],
                 "name": rows[0][3],
                 "value": rows[0][4],
                 "count": rows[0][5],
                 "min_count": rows[0][6],
                 "created": rows[0][7],
                 "updated": rows[0][8]
               }
            }

#LIST MULTIPLE PARTS BY IDS
@app.get("/parts/list/multiple/{part_ids}")
async def parts_list_by_ids(part_ids: str):
    from admin_db import parts_list_by_ids
    rows = parts_list_by_ids(part_ids)
    parts = []
    for i in range(len(rows)):
        parts.append(
                    {"part_id": rows[i][0],
                    "category": rows[i][1],
                    "sub_category": rows[i][2],
                    "name": rows[i][3],
                    "value": rows[i][4],
                    "count": rows[i][5],
                    "min_count": rows[i][6],
                    "created": rows[i][7],
                    "updated": rows[i][8],}
                  )
    return parts

#SEARCH IN PARTS
@app.get("/parts/search/{name}")
async def parts_search_by_name(name: str):
    from admin_db import parts_search_by_name
    rows = parts_search_by_name(name)
    parts = []
    for i in range(len(rows)):
        parts.append(
            {"part_id": rows[i][0],
             "category": rows[i][1],
             "sub_category": rows[i][2],
             "name": rows[i][3],
             "value": rows[i][4],
             "count": rows[i][5],
             "min_count": rows[i][6],
             "created": rows[i][7],
             "updated": rows[i][8], }
        )
    return parts

@app.get("/parts/search/category/{category}")
async def parts_search_by_category(category: str):
    from admin_db import parts_search_by_category
    rows = parts_search_by_category(category)
    parts = []
    for i in range(len(rows)):
        parts.append(
            {"part_id": rows[i][0],
             "category": rows[i][1],
             "sub_category": rows[i][2],
             "name": rows[i][3],
             "value": rows[i][4],
             "count": rows[i][5],
             "min_count": rows[i][6],
             "created": rows[i][7],
             "updated": rows[i][8], }
        )
    return parts

@app.get("/parts/search/sub_category/{sub_category}")
async def parts_search_by_category(sub_category: str):
    from admin_db import parts_search_by_sub_category
    rows = parts_search_by_sub_category(sub_category)
    parts = []
    for i in range(len(rows)):
        parts.append(
            {"part_id": rows[i][0],
             "category": rows[i][1],
             "sub_category": rows[i][2],
             "name": rows[i][3],
             "value": rows[i][4],
             "count": rows[i][5],
             "min_count": rows[i][6],
             "created": rows[i][7],
             "updated": rows[i][8], }
        )
    return parts

#CREATE PART
@app.post("/parts/create")
async def parts_create(part: dict):
    from admin_db import parts_create
    rows = parts_create(part)
    return {0:
               {"part_id": rows[0][0],
                 "category": rows[0][1],
                 "sub_category": rows[0][2],
                 "name": rows[0][3],
                 "value": rows[0][4],
                 "count": rows[0][5],
                 "min_count": rows[0][6],
                 "created": rows[0][7],
                 "updated": rows[0][8]
               }
            }

#DELETE PARTS
@app.delete("/parts/delete/{part_ids}")
async def parts_delete_by_ids(part_ids: str):
    from admin_db import parts_delete_by_ids
    rows = parts_delete_by_ids(part_ids)
    return rows

#UPDATE PART
@app.put("/parts/update/{part_id}")
async def parts_update_by_id(part_id:int, parameters: dict):
    from admin_db import parts_update_by_id
    rows = parts_update_by_id(part_id, parameters)
    return {"part_id": rows[0][0],
                 "category": rows[0][1],
                 "sub_category": rows[0][2],
                 "name": rows[0][3],
                 "value": rows[0][4],
                 "count": rows[0][5],
                 "min_count": rows[0][6],
                 "created": rows[0][7],
                 "updated": rows[0][8]
               }

@app.post("/parts/borrow/{part_ids}/{counts}")
async def parts_update(part_ids: str, counts: str):
    from admin_db import parts_borrow
    rows = parts_borrow(part_ids, counts)
    return rows