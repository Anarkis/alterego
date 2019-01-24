# Alterego

##Motivation
Due I'm leaving my current company, and I really like some of my colleagues, I came up with the idea of setting a bot, which send them some of ours jokes and add some interactions in case they reply to the bot.

##Setting things up
You only need a file with all the sentences that you can to send to a list of users (check `/text/example.yaml` )
This is the format that you have to write your own .yaml to be able to run **Alterego**

##Running it
Execute ``python alterego.py`` and it will start

##Environment
This project has been developed to run in Kubernetes, together with helm.
As database we use a MongoDB to store the data.

##Flow
We can identify clearly two parts:
 
 ##### Getting the data
 1. Get all the data from slack
 2. Store the data in Mongodb
 3. Read the text that we want to send
 4. Store the data in Mongodb
 5. Combine the Slack data with our text
 6. Store the result in Mongodb
 
  ##### Sending messages
  1. Query Mongodb and get one sentence
  2. If the user already wrote to us, add an reaction
  3. Send the message
  
  **Important:** To avoid send all the messages in consecutives days, sending the messages is random.
