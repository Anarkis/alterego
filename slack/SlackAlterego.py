import os
import requests
from slackclient import SlackClient
from jq import jq


class SlackAlterego:

    def __init__(self):
        self.token = os.environ["SLACK_API_TOKEN"]
        self.sc = SlackClient(self.token)

    def get_userlist(self):
        """
        Get the id and the name of all the users
        :return: a list of dictionaries with id and name [{id: X, name: X}]
        """
        params = {"token": self.token, "pretty": 1}
        r = requests.get("https://slack.com/api/users.list", params=params)
        return jq('.members[] | select (.deleted==false) | {id: .id, name: .name}').transform(r.json(),
                                                                                              multiple_output=True)

    def get_userchannel(self, users):
        """
        Get the channel for all the users
        :param users: list of dictionaries {id: X, name: X}
        :return: a modified list of dictionaries with the channel {id: X, name: X, channel: X}
        """
        for user in users:
            user_id = jq(".id").transform(user)
            answer = self.sc.api_call("im.open", user=user_id)
            user['channel'] = jq('.channel.id').transform(answer)
        return users

    def send_message(self, channel, text):
        """
        Method to send a text into a channel
        :param channel: channel where is going to be send the message
        :param text: will be the content of the message
        :return: the answer from the api
        """
        self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            as_user="true",
            user="bot"
        )

    def get_last_message(self, channel):
        """
        Method to get the info from the last message
        :param channel: channel to look
        :return: the duple user,ts related to the last message
        """
        info = self.sc.api_call("conversations.info", channel=channel)
        return jq('.channel.latest| {user: .user, ts: .ts}').transform(info)

    def add_reaction(self, channel, reaction):
        """
        Add a reaction to the last message
        :param channel: channel where it will add the reaction
        :param reaction: kind of reaction
        :return: the answer from the api
        """
        last_message = self.get_last_message(channel)
        self.sc.api_call("reactions.add", channel=channel, name=reaction, ts=last_message['ts'])
