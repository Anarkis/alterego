from slack.SlackAlterego import SlackAlterego

if __name__ == '__main__':
    slack = SlackAlterego()

    result = slack.send_message("XXXXXX", "hello world")
    #list = slack.get_userlist()
    #print(slack.get_userchannel(list))


