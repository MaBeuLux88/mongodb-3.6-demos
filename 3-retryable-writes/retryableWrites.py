import sys
import time

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Argument
print(sys.argv[1])
retryWrites = sys.argv[1].lower() == 'true'
print("Activated ? : " + str(retryWrites))

# Database connection
client = MongoClient(host=['mongo1:27017', 'mongo2:27018'], replicaset='replicaTest', retryWrites=retryWrites, w=2)
db = client.test
collection = db.coll

# Drop collection
collection.drop()

# Write
for i in range(10000):
    try:
        doc = {'a': i}
        print("Write : " + str(doc))
        collection.insert_one(doc)
        time.sleep(0.05)
    except PyMongoError as e:
        print(e)
