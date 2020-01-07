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

class Action(object):
    def __init__(self, *args):
        super(Action, self).__init__(*args)


class Detecteur(Action):
    def __init__(self, *args):
        super(Detecteur, self).__init__(*args)


class EV3PeNet(PeNet):

    def connect(self, fl):
        """
            fl : propose une liste d'actions associées aux transitions. Valeurs possibles :
            - None : pas d'actions
            -
        """
        assert len(fl) == len(self.T)
        self.fl = fl

# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':
    print('main de pyEV3PeNet.py')

    rdp2 = PeNet()
    rdp2.load(("p1", "p2"), ("t1", "t2"), (("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2"), ("t2", "p1")), (1, 1, 1, 1),  (1, 1))



    ev3 = EV3PeNet()
    print(ev3.P)