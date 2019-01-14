from pymongo import MongoClient
import os


class MongoDb:

    def __init__(self):
        self.host = os.environ['MONGODB_SERVICE_HOST']
        self.port = int(os.environ['MONGODB_SERVICE_PORT_MONGODB'])
        self.client = MongoClient(self.host, self.port)
        self.db = self.client.db

    def insert(self, data):
        self.db.slack.insert_many(data)

    def get_channel(self, username):
        return list(self.db.slack.find({"name": username}, {"channel": 1}))[0]
