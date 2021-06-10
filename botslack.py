from werkzeug import useragents
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
listprof = list()
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SigningSecret'], '/slack/events', app)
listelve= dict(dict())
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID=client.api_call('auth.test')['user_id']

#################################### CREATION ##################################################################
            
@app.route('/Petri_creation', methods=['POST'])
def reseauPetri():
	"""
        création du d'un réseau de petri avec en entré un nom et une chaine de caractère
    """
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	text=data.get('text')
	reseau= PeNet()
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
	param =text.split(':')
	testreseu=param[1].split(';')
	if len(testreseu)<5 :
		client.chat_postMessage(attachments=[
			{
				"color": f"{listelve[f'{auteur}']['Couleur']}",
				"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"{auteurnom} il manque des champs à votre réseau"
						}
					}
				]
			}
			],channel=channel_id)
	else:
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

#################################### SUPPRESSION ##################################################################

@app.route('/Petri_suppression', methods=['POST'])
def Petri_suppression():
	"""
	suppression du réseau de l'utilisateur dont le nom est placé avec la commande slash

	"""
	data = request.form
	auteur = data.get('user_id')
	channel_id = data.get('channel_id')
	nom=data.get('text')
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
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

#################################### MODIFICATION ##################################################################

@app.route('/Petri_modification', methods=['POST'])
def Petri_modification():
	"""
        modification d'un réseau appartenant à l'utilisateur de la commande 
    """
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	text=data.get('text')
	textsplit=text.split(':')
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
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
			while len(listelve[f'{auteur}']['reseauelev'][nom].A) != len(listelve[f'{auteur}']['reseauelev'][nom].W):
				listelve[f'{auteur}']['reseauelev'][nom].W.append(1)
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

#################################### AFFICHAGE ##################################################################

@app.route('/Petri_affichage', methods=['POST'])
def Petri_affichage():
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
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

#################################### SAUVEGARDE ##################################################################

@app.route('/Petri_sauvegarde', methods=['POST'])
def Petri_sauvegarde():
	data = request.form
	auteur = data.get('user_id')
	auteurnom=data.get('user_name')
	channel_id = data.get('channel_id')
	choix=data.get('text')
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
	if  len(listprof) == 0:
		listprof.append(auteurnom)
	if auteurnom not in listprof :
		client.chat_postMessage(attachments=[
				{
					"color": f"{listelve[f'{auteur}']['Couleur']}",
					"blocks":[
						{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"vous n'avez pas les droits"
							}
						}
					]
				}],channel=channel_id)
	else:
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
		elif  "AJOUE_PROF" in choix:
			nvprof=choix.split(':')
			prof=nvprof[1].split('@')
			listprof.append(prof[1])
			client.chat_postMessage(attachments=[
				{
					"color": f"{listelve[f'{auteur}']['Couleur']}",
					"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "Professeur ajouté"
					}
					#,
					#"accessory": {
					#	"type": "users_select",
					#	"placeholder": {
					#		"type": "plain_text",
					#		"text": "Select a user",
					#		"emoji": True
					#	},
					#	"action_id": "users_select-action"
					#}
					}
			]}],channel=channel_id)
		else:
			client.chat_postMessage(attachments=[
				{
					"color": f"{listelve[f'{auteur}']['Couleur']}",
					"blocks":[
					{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"{auteurnom} l'option que vous entré n'est pas valide"
					}
					}
			]}],channel=channel_id)


	return Response(), 200

#@app.route('/SelectMenue', methods=['GET','POST'])
#def selectMenue():
#	test= request.
	#print(test)
	#data=dict()
	#data=copy.deepcopy(test['payload'])
	#data=test['actions']['selected_user']
#	print(test)
	#actions=data[len(data)-10]
	#print(actions)
	#newprof=actions["selected_user"]
#	return Response(), 200

#################################### EXECUTION ##################################################################

@app.route('/Petri_execution', methods=['POST'])
def Petri_execution():
	"""
    exécution d'un des réseau de l'utilisateur choisi par son nom avec un mode et un nombre de tour placer en entré
    """
	data = request.form
	auteur = data.get('user_id')
	auteurnom = data.get('user_name')
	channel_id = data.get('channel_id')
	text=data.get('text')
	textsplit=text.split(':')
	if not auteur in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
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
						"text": f"{auteurnom} votre réseau n'existe pas"
						}
					}
				]
			}],channel=channel_id)
	else:
		if mode == "MOINSPRIORITAIRE":
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_MOINSPRIORITAIRE)
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
			mode="ALEATOIRE"
			listelve[f'{auteur}']['reseauelev'][nomreseau].init(mode=PeNet.MODE_ALEATOIRE)
	for i in range(imax):
			if (listelve[f'{auteur}']['reseauelev'][nomreseau].next()==None):
				client.chat_postMessage(attachments=[
				{
					"color": f"{listelve[f'{auteur}']['Couleur']}",
					"blocks":[
						{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"il n'y a aucune transition possible"
							}
						}
						]
				}
				],channel=channel_id)

			else :
				client.chat_postMessage(attachments=[
					{
						"color": f"{listelve[f'{auteur}']['Couleur']}",
						"blocks":[
							{
							"type": "section",
							"text": {
								"type": "mrkdwn",
								"text": f"mode:{mode} tour {i} : {listelve[f'{auteur}']['reseauelev'][nomreseau].lastT}-> {listelve[f'{auteur}']['reseauelev'][nomreseau].Mi}"
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

#################################### HELP ##################################################################

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
						"text": "*le réseau*: séparation des éléments par des *;* "
					}
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*P*:séparation des éléments par des *,*"
					}
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*T*:séparation des éléments par des *,*"
					}
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*A*:séparation des éléments par des arcs par *|* dans les arcs séparation des élements par de *,*"
					}
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*W*:séparation des éléments par des *,*"
					}
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*M0*:séparation des éléments par des *,*"
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*commande création:* nom_du_réseau:le_réseau"
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*commande exécution:* nom_du_réseau:nombre_de_tours:mode_tout_en_majuscule"
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*commande Modification:* nom_du_réseau:élément_à_modifier:la_modification"
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*commande supression:* nom_du_réseau"
					}
				}
			]
		}
	],channel=auteur)
	return Response(), 200



if __name__ == "__main__":
    app.run(debug=True,port=80)
