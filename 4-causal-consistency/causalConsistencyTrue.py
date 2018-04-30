from pymongo import MongoClient
from pymongo import ReadPreference
# Connection to the database
from pymongo.errors import PyMongoError

client = MongoClient(host=['mongo1:27017', 'mongo2:27017'], replicaset='replicaTest')
coll = client.test.testCausal
secondary_coll = coll.with_options(read_preference=ReadPreference.SECONDARY)

with client.start_session(causal_consistency=True) as session:
    print("Start session document")
    print(coll.find_one({'_id': 1}))

    print("\n==> 'x' increment +10 with upsert")
    try:
        coll.update_one({'_id': 1}, {'$inc': {'x': 10}}, upsert=True, session=session)
    except PyMongoError as e:
        print(e)

    # A secondary read waits for replication of the write.
    print("\nEnd session document")

    try:
        print(secondary_coll.find_one({'_id': 1}, session=session))
    except PyMongoError as e:
        print(e)
