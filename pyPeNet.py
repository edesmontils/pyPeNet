#!/usr/bin/env python3.7
# coding: utf8


class Place(object):
    def __init__(self, name, jetons=0):
        self.name = name
        self.contains = jetons


class Transition(object):
    def __init__(self, name):
        self.name = name


class Arc(object):
    def __init__(self, poids=1):
        assert poids >= 0, "Erreur sur le poids"
        self.poids = poids
        self.source = None
        self.cible = None


class ArcPT(Arc):
    def __init__(self, place, transition, poids=1):
        super(poids)
        self.source = place
        self.cible = transition


class ArcTP(Arc):
    def __init__(self, transition, place, poids=1):
        super(poids)
        self.cible = place
        self.source = transition



#==================================================
#==================================================
#==================================================

if __name__ == '__main__':
	print('main de pyPeNet.py')