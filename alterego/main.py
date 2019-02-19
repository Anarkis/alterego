from slack.SlackAlterego import SlackAlterego
from mongodb.MongoDb import MongoDb
from logger.logger import logger
import yaml
import time
import random


def setup():
    collection = ["slack", "text", "final_text"]

    if not mongo.is_collection(collection[1]) or mongo.is_empty(collection[1]):
        with open('alterego/text/text.yaml', 'r') as file:
            text = yaml.safe_load(file)['text']
        mongo.insert_many(collection[1], text)
        logger.info('Text data stored in mongodb')
    else:
        logger.info('Text data already present in mongodb')

    if not mongo.is_collection(collection[0]) or mongo.is_empty(collection[0]):
        users_selected = []
        for user in mongo.get_users():
            users_selected.append(user['name'])

        user_list = slack.get_userlist()
        data = slack.get_userchannel(user_list, users_selected)
        mongo.insert_many(collection[0], data)
        logger.info("Slack data stored in mongodb")

    else:
        logger.info("Slack data already present in mongodb")

    if not mongo.is_collection(collection[2]):
        users = mongo.get_users()
        for user in users:
            user_texts = mongo.get_texts_user(user['name'])
            if bool(user.get('groups', {})):
                group_texts = mongo.get_texts_group(user['groups'])
                user_texts.extend(group_texts)

            for element in user_texts:
                for text in element['text']:
                    mongo.insert_one("final_text", {"user": user['name'], "text": text})

        logger.info("Data combined and inserted in mongodb")
    else:
        logger.info("Combined data already present in mongodb")


def play():
    users = mongo.get_users()

    for user in users:
        secs = random.randint(1, 60)
        logger.info("Waiting %s ", secs)
        time.sleep(secs)

        if secs < 50:
            sentence = mongo.find_one_and_delete(user['name'])
            if sentence is not None:
                logger.info("message %s", sentence)
                logger.info("sending to %s", user['name'])
                channel = mongo.get_channel(user['name'])['channel']
                slack.add_reaction(channel)
                slack.send_message(channel, sentence['text'])
                logger.info("sent")
            else:
                logger.info("No more messages for %s", user['name'])
        else:
            logger.info("Skipping to %s", user['name'])


slack = SlackAlterego()
mongo = MongoDb()

setup()
play()

logger.info("Fly Butterfly")
