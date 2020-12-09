import pymongo
import pandas as pd
from pymongo import MongoClient

## Instantiate client
mongo_uri = 'mongodb://localhost:27017/capston_db'
client = MongoClient(mongo_uri)

## Select database and collection (table)
db = client['capstone_db']
tbl = db.capstone_tbl


## Convert to dataframe
df = pd.DataFrame(list(tbl.find()))

print(df)
