# Backend API for project WebSklad

## How to deploy
1. You either download latest released package from https://github.com/dvdzrv/FastAPIProject/releases or compile from source.
2. Create .env file
3. Copy everything from .env_example into .env
4. Replace fields in .env as needed
5. Place table (in .csv format) with parts into db/csvs/
6. Run init executable file

## How to compile from source into working executable:
1. Download source code zip from github
2. Download latest python
3. Install requirements
```
pip install requirements.txt
```
4. Compile
```
pyinstaller -F init.py --clean
```
Executable will be placed into dist/ directory.



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