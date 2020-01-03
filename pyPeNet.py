#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) classiques
"""
import pprint

class Place(object):
    """
        Représente une place dans un RdP
    """

    def __init__(self, name, jetons=0):
        self.name = name
        self.contains = jetons

    def __str__(self):
        return self.name+"("+str(self.contains)+")"


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
        return str(self.source)+" -"+str(self.poids)+"-> "+str(self.cible)


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
    def __init__(self):
        pass

    def __str__(self):
        return [str(p) for p in self.P]

    def define(self, P, T, A, W, M0):
        assert len(A) == len(W), "incohérence entre A et W"
        assert len(P) == len(M0), "incohérence entre P et M0"
        self.P = list(P)
        self.T = list(T)
        self.A = list(A)
        self.W = list(W)
        self.M0 = list(M0)


    def load(self, P, T, A, W, M0):
        nbp = len(P)
        self.P = list()
        nbt = len(T)
        self.T = list()
        nba = len(A)
        self.A = list()

        assert nba == len(W), "incohérence entre A et W"
        assert nbp == len(M0), "incohérence entre P et M0"

        self.W = list(W)
        self.M0 = list(M0)

        for i in range(nbp):
            p = P[i]
            m = M0[i]
            self.P.append(Place(p, m))

        for i in range(nbt):
            t = T[i]
            self.T.append(Transition(t))

        for i in range(nba):
            (source, cible) = A[i]
            assert ((source in P) and (cible in T)) or ((source in T) and (cible in P) ), "Arc incohérent "+source+"/"+cible
            if source in P:
                for p in self.P:
                    if p.name == source :
                        break
                for t in self.T:
                    if t.name == cible :
                        break
                self.A.append(ArcPT(p,t,W[i]))
            else:
                for p in self.P:
                    if p.name == cible :
                        break
                for t in self.T:
                    if t.name == source :
                        break
                self.A.append(ArcTP(t,p,W[i]))  


    def init(self):
        for i in range(len(self.M0)):
            self.P[i].contains = self.M0[i]


# ==================================================
# ==================================================
# ==================================================


if __name__ == '__main__':
    print('main de pyPeNet.py')
    pp = pprint.PrettyPrinter(indent=4)

    p1 = Place("p1")
    t1 = Transition("t1")
    p2 = Place("p2")
    t2 = Transition("t2")
    p3 = Place("p3")
    t3 = Transition("t3")
    a1 = ArcPT(p1, t1)
    a2 = ArcTP(t1, p2)
    a3 = ArcPT(p2, t2)
    a4 = ArcTP(t2, p1)

    rdp1 = PeNet()
    rdp1.define((p1, p2, p3), (t1, t2, t3),
                (a1, a2, a3, a4), (1, 1, 1, 1), (1, 0, 0))

    rdp2 = PeNet()
    rdp2.load(("p1", "p2"), ("t1", "t2"), (("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2"), ("t2", "p1")), (1, 1, 1, 1),  (1, 0))
    for p in rdp2.P: print(str(p)+" ")
