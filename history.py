from admin_db import query_db
from auth import get_user_id_by_token

def construct_history(row):
    return {
        "history_id": row[0],
        "user_id": row[1],
        "operation": row[2],
        "time": row[3],
    }

def construct_history_list(rows):
    history_list = []
    for row in rows:
        history_list.append(construct_history(row))
    return history_list



def list_history():
        return query_db(
            f"""SELECT * FROM history;"""
        )


def history_add_operation(token: str, operation: str):
    try:
        user_id = get_user_id_by_token(token)

        query_db(
            f"""INSERT INTO history (history_id, user_id, operation) VALUES (NULL, '{user_id}', '{operation}');"""
        )

    except IndexError:
        query_db(
            f"""INSERT INTO history (history_id, user_id, operation) VALUES (NULL, '0', '{operation}');"""
        )
    