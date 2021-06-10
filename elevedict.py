import discord
from discord import Colour
import json
from pyDynaPeNet import *
from pyPeNet import *
import logging


#Passage d'une chaine de caractère à un réseau 
def strtoreseau(mes:str,reseauP : PeNet()):
    """
    passage d'une chaine de caractère a un réseau de petri 
    """
    param =mes.split(';')
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
    while len(W)!=len(A):
        W.append(1)
    M0= param[4].split(',')
    for i in range(0,len(M0)):
        M0[i]=int(M0[i])
    while len(M0)!=len(P):
        M0.append(0)

    reseauP.load(P,T,A,W,M0)

#Passage d'un réseau à une chaine de caractère
def reseautostr(reseauP : PeNet()):
    """
    passage d'un réseau de petri a une chaine de caractère
    """
    reseaustr=""
    for i in range (0,len(reseauP.P)) :
        if i != len(reseauP.P)-1 :
            reseaustr+=str(reseauP.P[i])+","
        elif i==len(reseauP.P)-1 :
            reseaustr+=reseauP.P[i]+";"
    for i in range (0,len(reseauP.T)) :
        if i != len(reseauP.T)-1 :
            reseaustr+=str(reseauP.T[i])+","
        elif i==len(reseauP.T)-1 :
            reseaustr+=reseauP.T[i]+";"
    for i in range (0,len(reseauP.A)) :
        if i != len(reseauP.A)-1 :
            for j in range(0,len(reseauP.A[i])):
                if j != len(reseauP.A[i])-1:
                    reseaustr+=str(reseauP.A[i][j])+","
                elif j==len(reseauP.A[i])-1 :
                    reseaustr+=str(reseauP.A[i][j])+"|"
        elif i==len(reseauP.A)-1 :
            for j in range(0,len(reseauP.A[i])):
                if j != len(reseauP.A[i])-1:
                    reseaustr+=str(reseauP.A[i][j])+","
                elif j == len(reseauP.A[i])-1: 
                    reseaustr+=str(reseauP.A[i][j])+";"
    for i in range (0,len(reseauP.W)) :
        if i != len(reseauP.W)-1 :
            reseaustr+=str(reseauP.W[i])+","
        elif i==len(reseauP.W)-1 :
            reseaustr+=str(reseauP.W[i])+";"

    for i in range (0,len(reseauP.M0)) :
        if i != len(reseauP.M0)-1 :
            reseaustr+=str(reseauP.M0[i])+","
        elif i==len(reseauP.M0)-1 :
            reseaustr+=str(reseauP.M0[i])
    return reseaustr
    
