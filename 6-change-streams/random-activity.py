import json
import random
import sys
import time

from pymongo import MongoClient
from pymongo.errors import PyMongoError


# This class generate some random activities on a MongoDB node for test and demo purposes.
# In this example, I am inserting, reading, updating and deleting "user" documents randomly.
# I
class RandomActivity:

    def __init__(self):
        self.docs = self.get_documents_from_file("users.json")
        self.users = self.get_collection()

        self.ids = self.collect_all_ids()
        self.deleted = list(self.ids)
        self.inserted = []

    def collect_all_ids(self):
        ids = []
        for doc in self.docs:
            ids.append(doc["_id"])
        return ids

    @staticmethod
    def get_argument():
        if len(sys.argv) != 2:
            print("You forgot the argument!\nSleep time between 2 operations: <float>")
            exit(1)

        sleep = float(sys.argv[1])
        print("Sleep time : " + str(sleep))
        return sleep

    @staticmethod
    def get_collection():
        client = MongoClient(host=['mongo1:27017', 'mongo2:27018'], replicaset='replicaTest')
        # client = MongoClient(host=['localhost:27017', 'localhost:27018'], replicaset='replicaTest')
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
        sleep = self.get_argument()
        self.remove_all_documents()
        for i in range(100000):
            action = self.determine_random_action()
            self.make_action(action)
            time.sleep(sleep)

    def determine_random_action(self):
        if len(self.inserted) == 0:
            return "insert"
        if len(self.deleted) == 0:
            return "delete"

        nb_docs = len(self.inserted)

        random1 = random.randint(1, 10)
        if random1 == 1:
            return "read"
        elif random1 < 6:
            return "update"

        if nb_docs < random.randint(0, len(self.ids) - 1):
            return "insert"
        else:
            return "delete"

    def remove_all_documents(self):
        self.users.remove({})

    def make_action(self, action):
        if action == "insert":
            self.insert()
        elif action == "update":
            self.update()
        elif action == "delete":
            self.delete()
        elif action == "read":
            self.read()
        else:
            print("ERROR : unknown action")
            exit(1)

    def insert(self):
        _id = self.deleted.pop(0)
        self.inserted.append(_id)
        print("==> INSERTING ID : " + str(_id))
        try:
            self.users.insert_one(self.docs[_id])
        except PyMongoError as e:
            print(e)

    def update(self):
        _id = random.choice(self.inserted)
        print("==> UPDATING  ID : " + str(_id))
        rand = random.randint(1, 3)
        try:
            if rand == 1:
                self.users.update_one({"_id": _id}, {"$inc": {"count": 1}})
            elif rand == 2:
                self.users.update_one({"_id": _id}, {"$set": {"gender": random.choice(["Female", "Male", "Robot"])}})
            else:
                ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
                self.users.update_one({"_id": _id}, {"$set": {"ip_address": ip}})
        except PyMongoError as e:
            print(e)

    def delete(self):
        _id = self.inserted.pop()
        self.deleted = [_id] + self.deleted
        print("==> DELETING  ID : " + str(_id))
        try:
            self.users.remove({"_id": _id})
        except PyMongoError as e:
            print(e)

    def read(self):
        try:
            _id = random.choice(self.inserted)
            doc = self.users.find_one({"_id": _id})
            print("==> READING  DOC : " + str(doc))
        except PyMongoError as e:
            print(e)


RandomActivity().main()
