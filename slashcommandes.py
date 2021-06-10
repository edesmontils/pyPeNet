import discord
from discord import Colour
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import json
from pyDynaPeNet import *
from pyPeNet import *
import logging
from elevedict import strtoreseau , reseautostr
import copy

with open('token.json') as json_data:
    data = json.load(json_data,)  

client = discord.Client()
slash = SlashCommand(client, sync_commands=True) # Déclaration des slash commande a travers le client
@client.event
async def on_ready():
    print("Ready!")
listelve= dict(dict())
guild_ids = [831424773023727617] #id du serveur ou les slash commandes vont être répertorier

reseauP = PeNet()

#################################### CREATION ##################################################################

@slash.slash(name="Petri_création",
             description="This is just a test command, nothing more.",
             options=[
               create_option(
                 name="nom",
                 description="nom du réseau",
                 option_type=3,
                 required=True
               ),
               create_option(
                 name="reseau",
                 description="This is the first option we have.",
                 option_type=3,
                 required=True
               )
             ],guild_ids=guild_ids)
async def creation(ctx,nom:str,reseau:str):
        """
        création du d'un réseau de petri avec en entré un nom et une chaine de caractère
        """
        reseauP = PeNet()
        auteur=ctx.author
        if not f'{auteur}' in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
        testreseu=reseau.split(';')
        if len(testreseu)<5 :
          embedR = discord.Embed(title=f"réseau de petri {nom} de {ctx.author} ", colour=listelve[f'{auteur}']['Couleur'])
          embedR.add_field(name="P", value=" il manque des champs à votre réseau", inline=False)
        else:
          strtoreseau(reseau,reseauP)
          listelve[f'{auteur}']['reseauelev'][nom]=reseauP
          listelve[f'{auteur}']['nombredereseau'] = listelve[f'{auteur}']['nombredereseau'] + 1 
          embedR = discord.Embed(title=f"réseau de petri {nom} de {ctx.author} ", colour=listelve[f'{auteur}']['Couleur'])
          embedR.add_field(name="P", value=listelve[f'{auteur}']['reseauelev'][nom].P , inline=False)
          embedR.add_field(name="T", value=listelve[f'{auteur}']['reseauelev'][nom].T, inline=False)
          embedR.add_field(name="A", value= listelve[f'{auteur}']['reseauelev'][nom].A, inline=False)
          embedR.add_field(name="W", value=listelve[f'{auteur}']['reseauelev'][nom].W, inline=False)
          embedR.add_field(name="MO", value=listelve[f'{auteur}']['reseauelev'][nom].M0, inline=False)
          embedR.add_field(name="Réseau en chaine de caractères:", value= reseau , inline=False)
        await ctx.send(embed=embedR)

#################################### EXECUTION ##################################################################

@slash.slash(name='Petri_execution',
             description="execute un réseau de Petri avec un nombre de pas et un mode choisi",
             options=[
               create_option(
                 name="ndt",
                 description="nombre de transitions à effectuer",
                 option_type=4,
                 required=True
               ),
               create_option(
                 name="nomreseau",
                 description="choix du reseau à executer",
                 option_type=3,
                 required=True
               ),
               create_option(
                 name="mode",
                 description="Choix du mode ",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="ALEATOIRE",
                    value="ALEATOIRE"
                  ),
                  create_choice(
                    name="PLUSFREQUENT",
                    value="PLUSFREQUENT"
                  ),
                  create_choice(
                    name="MOINSFREQUENT",
                    value="MOINSFREQUENT"
                  ),
                  create_choice(
                    name="PLUSRECENT",
                    value="PLUSRECENT"
                  ),
                  create_choice(
                    name="MOINSRECENT",
                    value="MOINSRECENT"
                  ),
                  create_choice(
                    name="PLUSPRIORITAIRE",
                    value="PLUSPRIORITAIRE"
                  ),
                  create_choice(
                    name="MOINSPRIORITAIRE",
                    value="MOINSPRIORITAIRE"
                  )
                ])
             ],guild_ids=guild_ids
             )
async def exécution(ctx,ndt:int,nomreseau:str,mode:str):
        """
        exécution d'un des réseau de l'utilisateur choisi par son nom avec un mode et un nombre de tour placer en entré
        """
        auteur=ctx.author
        imax=ndt
        if not f'{auteur}' in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
        if nomreseau not in listelve[f'{auteur}']['reseauelev'] :
          embedA = discord.Embed(title=f"le Réseau: {nomreseau} n'existe pas", colour=listelve[f'{auteur}']['Couleur'])
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
          
          embedA = discord.Embed(title=f"Mode: {mode} , Réseau: {nomreseau}", colour=listelve[f'{auteur}']['Couleur'])
          for i in range(imax):
            if (listelve[f'{auteur}']['reseauelev'][nomreseau].next()==None):
              embedA.add_field(name=f"{i+1} blocage", value="aucune transition n'est possible", inline=False)
            else:
              embedA.add_field(name=f"{i+1}", value=f"{listelve[f'{auteur}']['reseauelev'][nomreseau].lastT}-> {listelve[f'{auteur}']['reseauelev'][nomreseau].Mi}", inline=False)
              embedA.add_field(name="comptage", value=listelve[f'{auteur}']['reseauelev'][nomreseau].v_count , inline=False)
        await ctx.send(embed=embedA)

#################################### SUPPRESSION ##################################################################

@slash.slash(name='Petri_suppressiondereseau',
             description="suppression du réseau choisi",
             options=[
               create_option(
                 name="nom",
                 description="nom du réseau à supprimer",
                 option_type=3,
                 required=True
               )],guild_ids=guild_ids
             )
async def suppression(ctx,nom:str):
      """
    	suppression du réseau de l'utilisateur dont le nom est placé avec la commande slash

    	"""
      auteur=ctx.author
      if not f'{auteur}' in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
      if nom  in listelve[f'{auteur}']['reseauelev']:
          listelve[f'{auteur}']['reseauelev'].pop(nom)
          embedA = discord.Embed(title=f"Suppression du réseau : {1}", colour=listelve[f'{auteur}']['Couleur'])
          await ctx.send(embed=embedA)
      else :
        embedA = discord.Embed(title=f"Suppression du réseau :le réseau que vous voulez supprimer n'existe pas", colour=listelve[f'{auteur}']['Couleur'])
        await ctx.send(embed=embedA)


#################################### AFFICHAGE ##################################################################

@slash.slash(name='Petri_affichage_reseau',
             description="affichage des réseau de l'eleve",
             guild_ids=guild_ids
             )
async def affichage(ctx):
            auteur=ctx.author
            if not f'{auteur}' in listelve :
              listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
            for i in listelve[f'{auteur}']['reseauelev']:
              embedR = discord.Embed(title=f"réseau de petri de {ctx.author} ", colour=listelve[f'{auteur}']['Couleur'])
              embedR.add_field(name="P", value=listelve[f'{auteur}']['reseauelev'][i].P , inline=False)
              embedR.add_field(name="T", value=listelve[f'{auteur}']['reseauelev'][i].T, inline=False)
              embedR.add_field(name="A", value= listelve[f'{auteur}']['reseauelev'][i].A, inline=False)
              embedR.add_field(name="W", value=listelve[f'{auteur}']['reseauelev'][i].W, inline=False)
              embedR.add_field(name="M0", value=listelve[f'{auteur}']['reseauelev'][i].M0, inline=False)
              embedR.add_field(name="option", value=f'reseau numéro :{i}'  , inline=False)
              await ctx.send(embed=embedR)

#################################### SAUVEGARDE ##################################################################

@slash.slash(name='Petri_sauvegardedonné',
             description="sauvegarde des données des élèves",
             options=[create_option(
                 name="choix",
                 description="Choix du mode",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="Sauvegarde",
                    value="Save"
                  ),
                  create_choice(
                    name="Recuperation",
                    value="Recup"
                  )])],
             guild_ids=guild_ids
             )
async def sauvegardeelev(ctx,choix:str):
            auteur=ctx.author
            if not f'{auteur}' in listelve :
              listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
            if ('Programmation' != auteur.top_role.name):
              embedR = discord.Embed(title=f"Vous n'avez pas les droits", colour=listelve[f'{auteur}']['Couleur'])
            else:
              if choix == "Save":
                listelevereseau= copy.deepcopy(listelve)
                for x in listelevereseau:
                    listelevereseau[x].pop('Couleur')
                    listelevereseau[x].update({'reseaudecouper':dict()})
                    for y in listelevereseau[x]['reseauelev']:
                      listelevereseau[x]['reseaudecouper'][y]=reseautostr(listelevereseau[x]['reseauelev'][y])
                    listelevereseau[x].pop('reseauelev')
                with open('donneeseleve.json', 'w') as f:
                  json.dump(listelevereseau,f,indent=4, ensure_ascii=False, sort_keys=False )
                embedR = discord.Embed(title=f"réseau de petri sauvegardé", colour=listelve[f'{auteur}']['Couleur'])
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
                embedR = discord.Embed(title=f"réseau de petri Récupéré", colour=listelve[f'{auteur}']['Couleur'])
            await ctx.send(embed=embedR)

#################################### MODIFICATION ##################################################################

@slash.slash(name='Petri_modifierreseau',
             description="modification d'un de vos reseau de Petri",
             options=[create_option(
                 name="modification",
                 description="Choix de la modification a faire",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="P",
                    value="P"
                  ),
                  create_choice(
                    name="T",
                    value="T"
                  ),
                  create_choice(
                    name="A",
                    value="A"
                  ),
                  create_choice(
                    name="W",
                    value="W"
                  ),
                  create_choice(
                    name="M0",
                    value="M0"
                  )
                  ]
                  ),
                create_option(
                 name="nom",
                 description="nom du réseau à supprimer",
                 option_type=3,
                 required=True
               ),
                create_option(
                 name="modreseau",
                 description="modification du réseau",
                 option_type=3,
                 required=True
               )
                  ],
             guild_ids=guild_ids
             )
async def modification(ctx,modification:str,nom:str,modreseau:str):
        """
        modification d'un réseau appartenant à l'utilisateur de la commande 
        """
        auteur=ctx.author
        if not f'{auteur}' in listelve :
          listelve[f'{auteur}']={'Couleur':discord.Colour.random(),'reseauelev':dict(),'nombredereseau': 0 }
        if nom not in listelve[f'{auteur}']['reseauelev'] :
          embedR = discord.Embed(title=f"le Réseau: {nom} n'existe pas", colour=listelve[f'{auteur}']['Couleur'])
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
          embedR = discord.Embed(title=f"Modification du réseau {nom} effectué", colour=listelve[f'{auteur}']['Couleur'])
          embedR.add_field(name="modification:", value=f'{modification} par {modreseau}' , inline=False)
          embedR.add_field(name="P", value=listelve[f'{auteur}']['reseauelev'][nom].P , inline=False)
          embedR.add_field(name="T", value=listelve[f'{auteur}']['reseauelev'][nom].T, inline=False)
          embedR.add_field(name="A", value= listelve[f'{auteur}']['reseauelev'][nom].A, inline=False)
          embedR.add_field(name="W", value=listelve[f'{auteur}']['reseauelev'][nom].W, inline=False)
          embedR.add_field(name="MO", value=listelve[f'{auteur}']['reseauelev'][nom].M0, inline=False)
        await ctx.send(embed=embedR)



client.run(data['tokendiscord'])