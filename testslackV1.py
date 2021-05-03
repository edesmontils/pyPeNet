import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import string
import json
from pyDynaPeNet import *
from pyPeNet import *
import logging

env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SigningSecret'], '/slack/events', app)
reseau = PeNet()
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID=client.api_call('auth.test')['user_id']
@slack_event_adapter.on('message')
def message(payload): 
    event = payload.get('event',{})
    channel_id= event.get('channel')
    user_id= event.get('user')
    text=event.get('text')
    
    if ('!petri' in text):
        decoup=text.split(':')
        param =decoup[1].split(';')
        P= param[0]
        P= P.split(',')
        T= param[1]
        T=T.split(',')
        A= param[2].split('|')
        for i in range(0,len(A)):
            A[i]=A[i].split(',')
        W= param[3].split(',')
        for i in range(0,len(W)):
            W[i]=int(W[i])
        MO= param[4].split(',')
        for i in range(0,len(MO)):
                MO[i]=int(MO[i])
        reseau.load(P,T,A,W,MO)

        if BOT_ID != user_id:
            client.chat_postMessage(channel=channel_id , text=f"P:{P}")
            client.chat_postMessage(channel=channel_id , text=f"T:{T}")
            client.chat_postMessage(channel=channel_id , text=f"A:{A}")
            client.chat_postMessage(channel=channel_id , text=f"W:{W}")
            client.chat_postMessage(channel=channel_id , text=f"MO:{MO}")
            
@ app.route('/reseauPetri', methods=['POST'])
def reseauPetri():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text=data.get('text')
    param =text.split(';')
    P= param[0]
    P= P.split(',')
    T= param[1]
    T=T.split(',')
    A= param[2].split('|')
    for i in range(0,len(A)):
        A[i]=A[i].split(',')
    W= param[3].split(',')
    for i in range(0,len(W)):
        W[i]=int(W[i])
    MO= param[4].split(',')
    for i in range(0,len(MO)):
            MO[i]=int(MO[i])
    reseau.load(P,T,A,W,MO)
    client.chat_postMessage(channel=channel_id , text=f"P:{P}")
    client.chat_postMessage(channel=channel_id , text=f"T:{T}")
    client.chat_postMessage(channel=channel_id , text=f"A:{A}")
    client.chat_postMessage(channel=channel_id , text=f"W:{W}")
    client.chat_postMessage(channel=channel_id , text=f"MO:{MO}")
    return Response(), 200

    
if __name__ == "__main__":
    app.run(debug=True,port=3000)