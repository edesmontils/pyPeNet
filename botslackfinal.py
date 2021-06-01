from slashcommandes import modification
import discord
from discord import Colour
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
from elevedict import strtoreseau , reseautostr
import copy

env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SigningSecret'], '/slack/events', app)
listelve= dict(dict())
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID=client.api_call('auth.test')['user_id']

            
@app.route('/Petri_creation', methods=['POST'])
def reseauPetri():
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	text=data.get('text')
	reseau= PeNet()
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
	param =text.split(':')
	strtoreseau(param[1], reseau)
	listelve[f'{auteur}']['reseauelev'][param[0]]=reseau
	listelve[f'{auteur}']['nombredereseau'] = listelve[f'{auteur}']['nombredereseau'] + 1 

	client.chat_postMessage(attachments=[
		{
			"color": f"{listelve[f'{auteur}']['Couleur']}",
			"blocks": [
				{"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f":mag: réseau de Petri {param[0]} de {auteurnom}"
					}
				},
				{
					"type": "divider"
				},
				{
				"type": "section",
				"fields": [
					{
					"type": "mrkdwn",
					"text": f"*P:* {listelve[f'{auteur}']['reseauelev'][param[0]].P }"
					},
					{
					"type": "mrkdwn",
					"text": f"*T:* {listelve[f'{auteur}']['reseauelev'][param[0]].T}"
					},
					{
					"type": "mrkdwn",
					"text": f"*A:* {listelve[f'{auteur}']['reseauelev'][param[0]].A}"
					},
					{
					"type": "mrkdwn",
					"text": f"*W:* {listelve[f'{auteur}']['reseauelev'][param[0]].W}"
					},
					{
					"type": "mrkdwn",
					"text": f"*M0:* {listelve[f'{auteur}']['reseauelev'][param[0]].M0}"
					}
					]
				},
				{
					"type": "divider"
				},
				{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"réseau en str: {text}"
				}
			}
			]
		}],channel=channel_id)
	return Response(), 200


@app.route('/Petri_suppression', methods=['POST'])
def Petri_suppression():
	data = request.form
	auteur = data.get('user_id')
	channel_id = data.get('channel_id')
	nom=data.get('text')
	if nom in listelve[f'{auteur}']['reseauelev']:
			listelve[f'{auteur}']['reseauelev'].pop(nom)
			client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "réseau supprimé"
						}
					}
				]
			}
			],channel=channel_id)
	else:
		client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": ":mag: réseau non trouver"
						}
					}
				]
			}],channel=channel_id)
	return Response(), 200

@app.route('/Petri_modification', methods=['POST'])
def Petri_modification():
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	text=data.get('text')
	textsplit=text.split(':')
	nom = textsplit[0]
	modification=textsplit[1]
	modreseau=textsplit[2]
	if nom not in listelve[f'{auteur}']['reseauelev'] :
          client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"réseau non trouvé"
						}
					}
				]
			}],channel=channel_id)
	else: 
		if modification=='P':
			newP= modreseau.split(',')
			listelve[f'{auteur}']['reseauelev'][nom].P = newP
			while len(listelve[f'{auteur}']['reseauelev'][nom].P) != len(listelve[f'{auteur}']['reseauelev'][nom].M0):
				listelve[f'{auteur}']['reseauelev'][nom].M0.append(0)
			listelve[f'{auteur}']['reseauelev'][nom].load(listelve[f'{auteur}']['reseauelev'][nom].P,listelve[f'{auteur}']['reseauelev'][nom].T,listelve[f'{auteur}']['reseauelev'][nom].A,listelve[f'{auteur}']['reseauelev'][nom].W,listelve[f'{auteur}']['reseauelev'][nom].M0)
		elif modification=='T':
			newT=modreseau.split(',')
			listelve[f'{auteur}']['reseauelev'][nom].T = newT
			listelve[f'{auteur}']['reseauelev'][nom].load(listelve[f'{auteur}']['reseauelev'][nom].P,listelve[f'{auteur}']['reseauelev'][nom].T,listelve[f'{auteur}']['reseauelev'][nom].A,listelve[f'{auteur}']['reseauelev'][nom].W,listelve[f'{auteur}']['reseauelev'][nom].M0)
		elif modification=='A':
			newA= modreseau.split('|')
			for i in range(0,len(newA)):
				newA[i]=newA[i].split(',')
			listelve[f'{auteur}']['reseauelev'][nom].A = newA
			listelve[f'{auteur}']['reseauelev'][nom].load(listelve[f'{auteur}']['reseauelev'][nom].P,listelve[f'{auteur}']['reseauelev'][nom].T,listelve[f'{auteur}']['reseauelev'][nom].A,listelve[f'{auteur}']['reseauelev'][nom].W,listelve[f'{auteur}']['reseauelev'][nom].M0)
		elif modification=='W':
			newW= modreseau.split(',')
			for i in range(0,len(newW)):
				newW[i]=int(newW[i])
			listelve[f'{auteur}']['reseauelev'][nom].W = newW
			listelve[f'{auteur}']['reseauelev'][nom].load(listelve[f'{auteur}']['reseauelev'][nom].P,listelve[f'{auteur}']['reseauelev'][nom].T,listelve[f'{auteur}']['reseauelev'][nom].A,listelve[f'{auteur}']['reseauelev'][nom].W,listelve[f'{auteur}']['reseauelev'][nom].M0)
		elif modification=='M0':
			newMO= modreseau.split(',')
			for i in range(0,len(newMO)):
				newMO[i]=int(newMO[i])  
			listelve[f'{auteur}']['reseauelev'][nom].M0 = newMO
			listelve[f'{auteur}']['reseauelev'][nom].load(listelve[f'{auteur}']['reseauelev'][nom].P,listelve[f'{auteur}']['reseauelev'][nom].T,listelve[f'{auteur}']['reseauelev'][nom].A,listelve[f'{auteur}']['reseauelev'][nom].W,listelve[f'{auteur}']['reseauelev'][nom].M0)
		client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"modification effectuée: réseau {nom} de {auteurnom} élément {modification} modifié par {modreseau} "
						}
					},
					{
						"type": "divider"
					},
					{
					"type": "section",
					"fields": [
						{
						"type": "mrkdwn",
						"text": f"*P:* {listelve[f'{auteur}']['reseauelev'][nom].P }"
						},
						{
						"type": "mrkdwn",
						"text": f"*T:* {listelve[f'{auteur}']['reseauelev'][nom].T}"
						},
						{
						"type": "mrkdwn",
						"text": f"*A:* {listelve[f'{auteur}']['reseauelev'][nom].A}"
						},
						{
						"type": "mrkdwn",
						"text": f"*W:* {listelve[f'{auteur}']['reseauelev'][nom].W}"
						},
						{
						"type": "mrkdwn",
						"text": f"*M0:* {listelve[f'{auteur}']['reseauelev'][nom].M0}"
						}
						]
					},
					{
						"type": "divider"
					},
					{
					"type": "section",
					"text": {
						"type": "plain_text",
						"text": f"réseau en str: {reseautostr(listelve[f'{auteur}']['reseauelev'][nom])}"
					}
				}
				]
			}],channel=channel_id)
	return Response(), 200

@app.route('/Petri_affichage', methods=['POST'])
def Petri_affichage():
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	for i in listelve[f'{auteur}']['reseauelev']:
		client.chat_postMessage(attachments=[
		{
			"color": f"{listelve[f'{auteur}']['Couleur']}",
			"blocks": [
				{"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f":mag: réseau de Petri {i}  de {auteurnom}",
					}
				},
				{
					"type": "divider"
				},
				{
				"type": "section",
				"fields": [
					{
					"type": "mrkdwn",
					"text": f"*P:* {listelve[f'{auteur}']['reseauelev'][i].P }"
					},
					{
					"type": "mrkdwn",
					"text": f"*T:* {listelve[f'{auteur}']['reseauelev'][i].T}"
					},
					{
					"type": "mrkdwn",
					"text": f"*A:* {listelve[f'{auteur}']['reseauelev'][i].A}"
					},
					{
					"type": "mrkdwn",
					"text": f"*W:* {listelve[f'{auteur}']['reseauelev'][i].W}"
					},
					{
					"type": "mrkdwn",
					"text": f"*M0:* {listelve[f'{auteur}']['reseauelev'][i].M0}"
					}
					]
				},
				{
					"type": "divider"
				},
				{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"réseau en str: {reseautostr(listelve[f'{auteur}']['reseauelev'][i])}"
				}
			}
			]
		}],channel=channel_id)
	return Response(), 200

@app.route('/Petri_sauvegarde', methods=['POST'])
def Petri_sauvegarde():
	data = request.form
	auteur = data.get('user_id')
	channel_id = data.get('channel_id')
	choix=data.get('text')
	if choix == "Save":
              listelevereseau= copy.deepcopy(listelve)
              for x in listelevereseau:
                  listelevereseau[x].pop('Couleur')
                  listelevereseau[x].update({'reseaudecouper':dict()})
                  for y in listelevereseau[x]['reseauelev']:
                    listelevereseau[x]['reseaudecouper'][y]=reseautostr(listelevereseau[x]['reseauelev'][y])
                  listelevereseau[x].pop('reseauelev')
              with open('donneeselevesSlack.json', 'w') as f:
                json.dump(listelevereseau,f,indent=4, ensure_ascii=False, sort_keys=False )
              client.chat_postMessage(attachments=[
				{
					"color": f"{listelve[f'{auteur}']['Couleur']}",
					"blocks":[
						{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"sauvegarde effectué"
							}
						}
					]
				}],channel=channel_id)
	elif choix == "Recup":
              with open('donneeseleve.json') as f:
                dataelev = json.load(f)
              dicttampon= copy.deepcopy(dataelev)
              for x in dicttampon :
                dicttampon[x]={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau':dataelev[x]['nombredereseau']}
                print(dicttampon)
                for i in dataelev[x]['reseaudecouper']:
                  reseauP = PeNet()
                  strtoreseau(dataelev[x]['reseaudecouper'][i],reseauP)
                  dicttampon[x]['reseauelev'][i]=reseauP
              print(dicttampon)
              listelve.clear()
              listelve.update(dicttampon)
              client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"récupération effectué "
						}
					}
				]
			}],channel=channel_id)
	return Response(), 200

@app.route('/Petri_execution', methods=['POST'])
def Petri_execution():
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	text=data.get('text')
	textsplit=text.split(':')
	nomreseau = textsplit[0]
	imax=int(textsplit[1])
	mode=textsplit[2]
	if nomreseau not in listelve[f'{auteur}']['reseauelev']:
		client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"réseau non trouvé"
						}
					}
				]
			}],channel=channel_id)
	else:
		if mode == "ALEATOIRE":
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_ALEATOIRE)
		elif mode == "PLUSFREQUENT":
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_PLUSFREQUENT)
		elif  mode == "MOINSFREQUENT":
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_MOINSFREQUENT)
		elif  mode == "PLUSRECENT":
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_PLUSRECENT)
		elif  mode == "MOINSRECENT":
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_MOINSRECENT)
		elif  mode == "PLUSPRIORITAIRE":
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_PLUSPRIORITAIRE)
		else :
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_MOINSPRIORITAIRE)
	for i in range(imax):
			listelve[f'{auteur}']['reseauelev'][nomreseau].next()
			client.chat_postMessage(attachments=[
				{
					"color": f"{listelve[f'{auteur}']['Couleur']}",
					"blocks":[
						{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"{listelve[f'{auteur}']['reseauelev'][nomreseau].lastT}-> {listelve[f'{auteur}']['reseauelev'][nomreseau].Mi}"
							}
						},
						{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"comptage: {listelve[f'{auteur}']['reseauelev'][nomreseau].v_count}"
							}
						}

					]
				}],channel=channel_id)
	return Response(), 200

@app.route('/Petri_help', methods=['POST'])
def Petri_help():
	data = request.form
	auteur = data.get('user_id')
	channel_id = data.get('channel_id')
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
	client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"ceci est le message d'aide pour la compréhension du bot"
						}
					}
				]
			}],channel=auteur)
	return Response(), 200



if __name__ == "__main__":
    app.run(debug=True,port=80)