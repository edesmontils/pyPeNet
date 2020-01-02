#!/usr/bin/env python3.7
# coding: utf8


class Place(object):
    def __init__(self, name, jetons=0):
        self.name = name
        self.contains = jetons

    def __str__(self):
        return self.name


class Transition(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Arc(object):
    def __init__(self, poids=1):
        assert poids >= 0, "Erreur sur le poids"
        self.poids = poids
        self.source = None
        self.cible = None

    def __str__(self):
        return self.source+"-"+self.poids+"->"+self.cible


class ArcPT(Arc):
    def __init__(self, place, transition, poids=1):
        super().__init__(poids)
        assert isinstance(place, Place), "place n'est pas une Place"
        assert isinstance(
            transition, Transition), "transition n'est pas une Transition"
        self.source = place
        self.cible = transition


class ArcTP(Arc):
    def __init__(self, transition, place, poids=1):
        super().__init__(poids)
        assert isinstance(place, Place), "place n'est pas une Place"
        assert isinstance(
            transition, Transition), "transition n'est pas une Transition"
        self.cible = place
        self.source = transition


class PeNet(object):
    pass


# ==================================================
# ==================================================
# ==================================================


if __name__ == '__main__':
    print('main de pyPeNet.py')
    p1 = Place("p1")
    t1 = Transition("t1")
    a = ArcPT(p1, t1)
    print(a)
