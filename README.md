# Prečítať hoppschotch/README.md DIKI

# Ako skompilovať do exe
pip install pyinstaller uvicorn fastapi 
pyinstaller -F init.py --clean
./dist/init


# LISTING

LIST ALL PARTS: "/parts/list"

USES GET

LIST PART BY ID: "/parts/list/{ID}"

USES GET

LIST MULTIPLE PARTS BY IDS: "/parts/list/{ID,ID,ID}"
pr. /parts/list/1,2,189

USES GET

# SEARCH:

SEARCH BY NAME: "/parts/search/{name}"
pr. "/parts/search/rezistor"

USES GET

SEARCH BY CATEGORY: "/parts/search/category/{category}"
pr. "/parts/search/pasívne"

USES GET

SEARCH BY SUBCATEGORY: "/parts/search/sub_category/{subcategory}"
pr. "/parts/search/bipolárny"

USES GET

# CREATE PART
"/parts/create"
SEND DICTIONARY,
USES POST

pr: 
{
  "category" : "Pasívna",
  "sub_category" : "test",
  "name" : "test",
  "value" : "10k",
  "count" : 109  
}

# DELETE PARTS
BY IDS,
USES DELETE

"/parts/delete/{ID,ID,ID}"
pr. "/parts/delete/1,2,128"

# UPDATE PARTS
BY ID, SEND DICTIONARY,
USES PUT

pr. "/parts/update/{ID}"
{
    "category": "Aktívna",
    "sub_category": "test",
    "name": "test",
    "value": "0",
    "count": 1,
    "min_count": 10
}

# !!!!TESTING NOT DONE YET!!!!

# BORROWING
BY ID, WITH COUNT,
USES POST

"/parts/borrow/{part_ids}/{counts}"
pr. /parts/borrow/1,2,128/10,1,21