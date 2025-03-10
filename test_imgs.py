import numpy as np
import requests
from admin_db import query_db

if __name__ == "__main__":
    count_w = 0
    count_n = 0
    for i in range(int(query_db(f"SELECT COUNT(*) FROM parts;")[0][0])):
        url = f"http://127.0.0.1:8000/image/{i}"
        r = requests.get(url)
        if r.status_code != 200:
            print("FAIL:", i)
            count_n += 1
        else:
            print(f"SUCCESS: {i}")
            count_w += 1
    print(f"Working: {count_w}, Not working: {count_n}")