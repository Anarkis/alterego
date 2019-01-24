from pymongo import MongoClient
import os


class MongoDb:

    def __init__(self):
        self.host = os.environ['MONGODB_SERVICE_HOST']
        self.port = int(os.environ['MONGODB_SERVICE_PORT_MONGODB'])
        self.client = MongoClient(self.host, self.port)
        self.db = self.client.db

    def insert_one(self, collection, data):
        """
        Insert method in Mongodb
        :param collection: collection where will be inserted
        :param data: data to be inserted
        :return:
        """
        self.db[collection].insert_one(data)

    def insert_many(self, collection, data):
        """
        Insert method in Mongodb
        :param collection: collection where will be inserted
        :param data: data to be inserted
        :return:
        """
        self.db[collection].insert_many(data)

    def is_empty(self, collection):
        if self.db[collection].count() > 0:
            return False
        return True

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
        return self.db.slack.find_one({"name": username}, {"channel": 1})

    def get_users(self):
        """
        get all the duple name, group from all the users
        :return: a list
        """
        return list(self.db.text.find({"type": "user"}, {"name": 1, "groups": 1, "_id": 0}))

    def get_texts_user(self, username):
        """
        get all the texts related to one user
        :param username: user to get the texts
        :return: the texts
        """
        return list(self.db.text.find({"name": username, "type": "user"}, {"text": 1, "_id": 0}))

    def get_texts_group(self, group_id):
        """
        get all the texts related to one group
        :param group_id: group which we will query
        :return: all the text relates to the group
        """
        text = []
        for group in group_id:
            text.extend(self.db.text.find({"type": "group", "id": group}, {"text": 1, "sentence": 1, "_id": 0}))
        return list(text)

    def find_one_and_delete(self, username):
        """
        find one text related to a given user, and delete from the db
        :param username: to pick up the text
        :return: the text from the user
        """
        return self.db.final_text.find_one_and_delete({"user": username}, {"text":1, "_id":0})

    def find_one(self, username):
        """
        find one text related to a given user
        :param username: to pick up the text
        :return: the text from the user
        """
        return self.db.final_text.find_one({"user": username}, {"text":1, "_id":0})
