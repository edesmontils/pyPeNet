import discord
import os
import json
from pyDynaPeNet import *
from pyPeNet import *
import os
import logging

with open('token.json') as json_data:
    data = json.load(json_data,) 

client = discord.Client()
#affichage dans la console quand le bot est lancer
@client.event
async def on_ready():
    print('connecté en tant que {0.user}'.format(client))

#event quand un message est placer dans le channel
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Bonjour'):
        mess= message.content.split(',')
        await message.channel.send(mess[1])

#commande pour créer un réseau de petri avec pyPeNet
#le message doit avoir un forme précis : !petri:P;T;A;W;MO
#les éléménts des doivent être séparé par des virgules et pour A on place des | entre chaque arc
#exemple !petri :p1,p2;t1,t2,t3;p1,t1|t1,p2|p2,t2|t2,p1|p1,t2|t3,p2;1, 1, 1, 1, 0, 1;1,1
    if message.content.startswith('!petri'):
        await message.reply("analise de votre réseau de petri:")
        #découpage du message pour récupèrer les éléments
        mess= message.content.split(':')
        param =mess[1].split(';')
        for i in range(0,len(param)):
            await message.channel.send(param[i])
        reseau = PeNet()
        #mise en forme des éléments pour qu'ils puissent  être utilisés 
        # dans la fonctiond load pour créer le réseau de petri 
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

        await message.channel.send(P)
        await message.channel.send(T)
        await message.channel.send(A)
        await message.channel.send(W)
        await message.channel.send(MO)
        reseau.load(P,T,A,W,MO)
        #une fois le réseau de petri créé si on envoie un message avec la commande 
        #!ModeAl:i, avec i étant le nombre d'itérations que l'on souhait effectué.
        @client.event
        async def on_message(message):
            if message.content.startswith('!ModeAl'):
                mess= message.content.split(':')
                imax=int(mess[1])
                reseau.init(mode=PeNet.MODE_ALEATOIRE)
                for i in range(imax):
                    reseau.next()
                    await message.channel.send(f"{reseau.lastT}-> {reseau.Mi}")
                await message.channel.send(f"""Comptage: {reseau.v_count}""")

#récupération du token pour connection au bot
client.run(data['token'])