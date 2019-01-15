from pymongo import MongoClient
import os


class MongoDb:

    def __init__(self):
        self.host = os.environ['MONGODB_SERVICE_HOST']
        self.port = int(os.environ['MONGODB_SERVICE_PORT_MONGODB'])
        self.client = MongoClient(self.host, self.port)
        self.db = self.client.db

    def insert(self, collection, data):
        """
        Insert method in Mongodb
        :param collection: collection where will be inserted
        :param data: data to be inserted
        :return:
        """
        self.db[collection].insert_many(data)

    def is_collection(self, collection):
        """
        check if the slack collection is present in
        mongodb
        :param collection: collection to check
        :return: true if is stored, otherwise false
        """
        if collection in self.db.collection_names():
            return True
        else:
            return False

    def get_channel(self, username):
        """
        Get the channel for messaging directly to a user
        :param username: username to get the info
        :return: the first hit in the db
        """
        return list(self.db.slack.find({"name": username}, {"channel": 1}).limit(1))[0]

    def get_texts_user(self, username):
        """
        get all the texts related to one user
        :param username: user to get the texts
        :return: the texts
        """
        return list(self.db.text.find({"name": username, "kind": "user"}, {"text": 1, "_id": 0}))

    def get_texts_group(self, group_id):
        """
        get all the texts related to one group
        :param group_id: group which we will query
        :return: all the text relates to the group
        """
        return list(self.db.text.find({"kind": "group", "id": group_id}, {"text": 1, "_id": 0}))
