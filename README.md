# LISTING

LIST ALL PARTS: "/parts/list"

LIST PART BY ID: "/parts/list/{ID}"

LIST MULTIPLE PARTS BY IDS: "/parts/list/{ID,ID,ID}"
pr. /parts/list/1,2,189

# SEARCH:

SEARCH BY NAME: "/parts/search/{name}"
pr. "/parts/search/rezistor"

SEARCH BY CATEGORY: "/parts/search/category/{category}"
pr. "/parts/search/pasívne"

SEARCH BY SUBCATEGORY: "/parts/search/sub_category/{subcategory}"
pr. "/parts/search/bipolárny"

# CREATE PART
"/parts/create"
SEND DICTIONARY
pr: 
{
  "category" : "Pasívna",
  "sub_category" : "test",
  "name" : "test",
  "value" : "10k",
  "count" : 109  
}

# DELETE PARTS
BY IDS
"/parts/delete/{ID,ID,ID}"
pr. "/parts/delete/1,2,128"

# UPDATE PARTS
BY ID, SEND DICTIONARY
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
BY ID, WITH COUNT
"/parts/borrow/{part_ids}/{counts}"
pr. /parts/borrow/1,2,128/10,1,21