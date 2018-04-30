from pymongo import MongoClient
from pymongo import ReadPreference
# Argument
from pymongo.errors import PyMongoError

# Connection to the ReplicaSet
client = MongoClient(host=['mongo1:27017', 'mongo2:27017'], replicaset='replicaTest')
coll = client.test.testCausal
secondary_coll = coll.with_options(read_preference=ReadPreference.SECONDARY)

# Connection to the secondary
clientAdmin = MongoClient(host=['mongo2:27017'])
admin = clientAdmin.admin

with client.start_session(causal_consistency=False) as session:
    print("Start session document")
    print(coll.find_one({'_id': 1}))

    print("\nStopping replication on the secondary node")
    print(admin.command({'configureFailPoint': 'rsSyncApplyStop', 'mode': 'alwaysOn'})['ok'])

    print("\n==> 'x' increment +10 with upsert")
    try:
        coll.update_one({'_id': 1}, {'$inc': {'x': 10}}, upsert=True, session=session)
    except PyMongoError as e:
        print(e)

    print("\nEnd session document")
    try:
        print(secondary_coll.find_one({'_id': 1}, session=session))
    except PyMongoError as e:
        print(e)

    print("\nRestarting replication on the secondary node")
    print(admin.command({'configureFailPoint': 'rsSyncApplyStop', 'mode': 'off'})['ok'])
