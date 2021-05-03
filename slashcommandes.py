import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import json
from pyDynaPeNet import *
from pyPeNet import *
import logging

with open('token.json') as json_data:
    data = json.load(json_data,)  

client = discord.Client()
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

@client.event
async def on_ready():
    print("Ready!")

guild_ids = [831424773023727617] # Put your server ID in this array.
reseau = PeNet()
@slash.slash(name="création",
             description="This is just a test command, nothing more.",
             options=[
               create_option(
                 name="petri",
                 description="This is the first option we have.",
                 option_type=3,
                 required=True
               )
             ],guild_ids=guild_ids)
async def on_message(ctx,petri:str):
        param =petri.split(';')
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
        embedR = discord.Embed(title=f"réseau de petri de ", color=0x00ff00)
        embedR.add_field(name="P", value= P, inline=False)
        embedR.add_field(name="T", value=T, inline=False)
        embedR.add_field(name="A", value= A, inline=False)
        embedR.add_field(name="W", value=W, inline=False)
        embedR.add_field(name="MO", value=MO, inline=False)
        embedR.add_field(name="option", value= petri , inline=False)
        await ctx.send(embed=embedR)

@slash.slash(name="aléatoire",
             description="lance le réseau en aléatoire.",
             options=[
               create_option(
                 name="ndp",
                 description="donne le nombre de pas réalisé par le réseau.",
                 option_type=4,
                 required=True
               )
             ],guild_ids=guild_ids)
async def testmessale(ctx, ndp:int):
                imax=ndp
                reseau.init(mode=PeNet.MODE_ALEATOIRE)
                embedA = discord.Embed(title=f"Mode aléatoire ", color=0x00ff00)
                for i in range(imax):
                    reseau.next()
                    embedA.add_field(name=f"{i}", value=f"{reseau.lastT}-> {reseau.Mi}", inline=False)
                    #await ctx.send(f"{reseau.lastT}-> {reseau.Mi}")
                embedA.add_field(name="comptage", value=reseau.v_count , inline=False)
                #await ctx.send(f"""Comptage: {reseau.v_count}""")
                await ctx.send(embed=embedA)

client.run(data['tokendiscord'])
