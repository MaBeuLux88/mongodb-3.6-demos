from pymongo import MongoClient
from pymongo.errors import WriteConcernError
import time

# Connection to the database
client = MongoClient(host=['mongo1:27017','mongo2:27018'],replicaset='myReplica',retryWrites=True,w=2)
#client = MongoClient(host=['mongo1:27017','mongo2:27018'],replicaset='myReplica',retryWrites=False,w=2)
db = client.test

for i in range(1500):
	try: 
                print("Write : " + str(i))
		db.test.insert_one({'a':i})
                time.sleep(0.1)
	except WriteConcernError, err:
		print WriteConcernError, err

