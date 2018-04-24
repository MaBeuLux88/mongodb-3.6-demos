import sys

from pymongo import MongoClient
from pymongo import ReadPreference

# Argument
if len(sys.argv) != 2:
    print("You forgot the argument!\nCausal Consistency : [true|false]")
    exit(1)

causalConsistency = sys.argv[1].lower() == 'true'
print("Causal Consistency activated: " + (u'\U0001f604' if causalConsistency else u'\U0001f622') + "\n")

# Connection to the database
client = MongoClient(host=['mongo1:27017', 'mongo2:27018'], replicaset='replicaTest')
coll = client.test.testCausal

with client.start_session(causal_consistency=causalConsistency) as session:
    # with client.start_session(causal_consistency=True) as session:
    print("Start session document")
    print(coll.find_one({'_id': 1}))

    print("\n==> 'x' increment +10 with upsert\n")
    coll.update_one({'_id': 1}, {'$inc': {'x': 10}}, upsert=True, session=session)

    # A secondary read waits for replication of the write.
    print("End session document")
    secondary_coll = coll.with_options(read_preference=ReadPreference.SECONDARY)
    print(secondary_coll.find_one({'_id': 1}, session=session))
