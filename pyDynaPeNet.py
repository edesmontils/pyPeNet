#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) pour exécuter sous EV3.
    TODO :
    - EV3PeNet
"""
from pyPeNet import *

# ==================================================
# ==================================================


class Event(object):
    def __init__(self):
        super(Event, self).__init__()

    def do(self):
        pass # print("Action done!")

# ==================================================
# OUT
# ==================================================


class OutEvent(Event):
    def __init__(self):
        super(OutEvent, self).__init__()


# ==================================================

class DisplayEvent(OutEvent):
    def __init__(self):
        super(DisplayEvent, self).__init__()



# ==================================================
# IN
# ==================================================


class InEvent(Event):
    def __init__(self, port=None):
        super(InEvent, self).__init__()
        self.port = port

# ==================================================

class Sensor(InEvent):
    def __init__(self, port):
        super(Sensor, self).__init__(port)
        assert port != None, "[Sensor init] bad port value"
        self.change = False

    def raised(self):
        self.change = True

    def do(self):
        self.change = False

# ==================================================
# ==================================================
# ==================================================

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
        if (a != None) and (isinstance(a, OutEvent)):
            a.do()
        return t


# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':
    rdp2 = DynaPeNet()
    rdp2.load(("p1", "p2"), ("t1", "t2"), (("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2"), ("t2", "p1")),
              (1, 1, 1, 1),  (1, 1), (None, DisplayEvent()))

    for i in range(15):
        rdp2.next()
        print(rdp2.Mi)
