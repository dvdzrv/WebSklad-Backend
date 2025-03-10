from admin_db import query_db, construct_part
from pathlib import Path

def get_img_by_id(part_id:int):
    try:
        row = query_db(
            f"""SELECT * FROM parts WHERE part_id = {part_id};"""
        )[0]
    except IndexError:
        return None

    if row == []:
        return None

    part = construct_part(row)

    try:
        img_path = Path(
            f"db/imgs/{str(part["name"]).lower() + " " + str(part["value"]).replace(",", ".")}.jpg"
        )
        if not img_path.is_file():
            return None
        else:
            return img_path
    except Exception as e:
        print(e)