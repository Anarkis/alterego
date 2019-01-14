from slack.SlackAlterego import SlackAlterego
from mongodb.MongoDb import MongoDb

if __name__ == '__main__':
    slack = SlackAlterego()
    mongo = MongoDb()

    # list = slack.get_userlist()
    # data = slack.get_userchannel(list)
    # mongo.insert(data)
    # print("data stored in mongodb")

    channel = mongo.get_channel("userxxx")
    print(channel['channel'])
    slack.send_message(channel['channel'], "Hello World")
    print("Fly Butterfly")
