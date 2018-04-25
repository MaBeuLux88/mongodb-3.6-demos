import json
# with open("persons.json") as f:
#     content = f.readlines()
#
# # print(content[0])
# # obj = json.loads(content[0])
# # print(obj)
# # print(obj["_id"])
#
# i = 0
# arr = []
# for line in content:
#     l = json.loads(line)
#     i += 1
#     l["_id"] = i
#     arr.append(l)
#
# print(arr)
#
# file = open("users.json", "w")
# for item in arr:
#     file.write("%s\n" % item)
import sys

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class RandomActivity(object):

    def __init__(self):
        self.docs = self.get_documents_from_file("users.json")
        self.users = self.get_collection()

        self.ids = self.collect_all_ids()
        self.deleted = list(self.ids)
        self.inserted = []

    def determine_action(self):
        if len(self.deleted) != 0 and len(self.ids) != len(self.inserted):
            # print("ACTION INSERT : DELETE : " + str(self.deleted[0:5]))
            return {"action": "insert", "_id": (self.deleted[0])}
        print("should not be here...")
        return {}

    @staticmethod
    def get_collection():
        client = MongoClient(host=['mongo1:27017', 'mongo2:27018'], replicaset='replicaTest')
        users = client.test.users
        return users

    @staticmethod
    def get_documents_from_file(users_json):
        with open(users_json) as file:
            str_lines = file.readlines()
        docs = []
        for line in str_lines:
            docs.append(json.loads(line))
        return docs

    def main(self):
        self.users.drop()

        # print("Deleted before : " + str(deleted))

        for i in range(10):
            action = self.determine_action()
            # print("deleted : " + str(deleted))
            # print("inserted : " + str(inserted))
            # print(action)
            self.make_action(action)

        # print(self.inserted)
        # print(self.deleted)

    def make_action(self, action):
        if action["action"] == "insert":
            self.insert(action["_id"])

    def insert(self, _id):
        print("==> INSERTING ID : " + str(_id))
        self.deleted = self.deleted[1:]
        self.inserted.append(_id)
        try:
            self.users.insert(self.docs[_id])
        except PyMongoError as e:
            print(e)

    def collect_all_ids(self):
        ids = []
        for doc in self.docs:
            ids.append(doc["_id"])
        return ids


RandomActivity().main()
