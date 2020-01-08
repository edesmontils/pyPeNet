#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) pour exécuter sous EV3.
    TODO :
    - EV3PeNet
"""
from pyPeNet import *

#from pybricks import ev3brick as brick
#from pybricks.ev3devices import Motor, UltrasonicSensor, TouchSensor, ColorSensor
#from pybricks.parameters import Port
#from pybricks.tools import wait
#from pybricks.robotics import DriveBase
class ES(object) :
    def __init__(self, *args):
        super(ES, self).__init__(*args)

    def do(self):
        print("Action done!")


class Action(ES):
    def __init__(self, *args):
        super(Action, self).__init__(*args)


class Detecteur(ES):
    def __init__(self, *args):
        super(Detecteur, self).__init__(*args)
        self.change = False

    def raised(self):
        self.change = True

    def do(self):
        self.change = False


class DynaPeNet(PeNet_I):
    def __init__(self, ):
        super(DynaPeNet, self).__init__()

    def connect(self, fl):
        """
            fl : propose une liste d'actions associées aux transitions. Valeurs possibles :
            - None : pas d'actions
            -
        """
        assert len(fl) == len(self.T)
        self.fl = fl

    def load(self, P, T, A, W, M0, F):
        super().load(P, T, A, W, M0)
        self.F = F

    def next(self):
        t = super().next()
        a = self.F[t]
        if (a != None) and (isinstance(a,Action)): a.do()
        return t


# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':
    print('main de pyEV3PeNet.py')

    rdp2 = DynaPeNet()
    rdp2.load(("p1", "p2"), ("t1", "t2"), (("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2"), ("t2", "p1")), 
                                           (1, 1, 1, 1),  (1, 1), (None, Action()))



    for i in range(15):
        rdp2.next()
        print(rdp2.Mi)