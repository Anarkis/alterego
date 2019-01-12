import os
import requests
from slackclient import SlackClient
from jq import jq


class SlackAlterego:

    def __init__(self):
        self.token = os.environ["SLACK_API_TOKEN"]
        self.sc = SlackClient(self.token)


    def get_userlist(self):
        params = {"token": self.token, "pretty": 1}
        r = requests.get("https://slack.com/api/users.list", params=params)
        return jq('.members[] | {id: .id, name: .real_name}').transform(r.json(), multiple_output=True)

    def get_userchannel(self, users):
        for user in users:
            id = jq(".id").transform(user)
            answer = self.sc.api_call("im.open", user=id)
            jq(".channel.id").transform(answer, multiple_output=True)

    def send_message(self, channel, text):
        self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            as_user="true",
            user="bot"
        )
