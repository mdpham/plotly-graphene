from pymongo import MongoClient
from os import environ
from bson import ObjectId


mongo_client = MongoClient(host = '127.0.0.1', port = 27017)
db = mongo_client['crescent']
print (db)
run = db.runs.find_one({'runID': ObjectId('5eda76def93f82004f4114c6')})
print(run)


