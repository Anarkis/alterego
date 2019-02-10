from slack.SlackAlterego import SlackAlterego
from mongodb.MongoDb import MongoDb
import yaml
import time
import random


def setup():
    collection = ["slack", "text", "final_text"]

    if not mongo.is_collection(collection[1]) or mongo.is_empty(collection[1]):
        with open('text/example.yaml', 'r') as file:
            text = yaml.safe_load(file)['text']
        mongo.insert_many(collection[1], text)
        print("Text data stored in mongodb")
    else:
        print("Text data already present in mongodb")

    if not mongo.is_collection(collection[0]) or mongo.is_empty(collection[0]):
        users_selected = []
        for user in mongo.get_users():
            users_selected.append(user['name'])

        user_list = slack.get_userlist()
        data = slack.get_userchannel(user_list, users_selected)
        mongo.insert_many(collection[0], data)
        print("Slack data stored in mongodb")

    else:
        print("Slack data already present in mongodb")

    if not mongo.is_collection(collection[2]) or mongo.is_empty(collection[2]):
        users = mongo.get_users()
        for user in users:
            user_texts = mongo.get_texts_user(user['name'])
            group_texts = mongo.get_texts_group(user['groups'])
            user_texts.extend(group_texts)

            for element in user_texts:
                for text in element['text']:
                    mongo.insert_one("final_text", {"user": user['name'], "text": text})

        print("Data combined and inserted in mongodb")
    else:
        print("Combined data already present in mongodb")


def play():
    users = mongo.get_users()

    for user in users:
        secs = random.randint(1, 90)
        print("Will wait %s ", secs)
        time.sleep(secs)

        if secs % 2 == 0:
            sentence = mongo.find_one_and_delete(user['name'])
            if sentence != "null":
                print("sending")
                channel = mongo.get_channel(user['name'])['channel']
                slack.add_reaction(channel)
                slack.send_message(channel, sentence['text'])


if __name__ == '__main__':
    slack = SlackAlterego()
    mongo = MongoDb()

    setup()
    play()

    print("Fly Butterfly")
