#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) à exécuter.
    TODO :
    - gestion des événements clavier comme transition source
    - gestion des événements souris (?) faisable par le même blibliothèque que pour le clavier.
    - proposer un timer pour provoquer une transition source au bout de x secondes
    - introduire un timer sur les transitions pour simuler le temps d'exécution
"""
from pyPeNet import *
# https://pythonhosted.org/pynput/keyboard.html & https://pythonhosted.org/pynput/mouse.html
from pynput.keyboard import Key, Listener

from multiprocessing import Manager

# ==================================================
# ==================================================
# ==================================================

# m = Manager()
keysDict = dict()


def runListener():
    print('Start KeyboardListener')
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print('End KeyboardListener')


def on_press(key):
    pass  # print('{0} pressed'.format(key))


def on_release(key):
    k = str(key)
    keysDict[k] = keysDict.get(k, 0) + 1
    print(type(k))
    if key == Key.esc:
        # Stop listener
        return False


# ==================================================
# ==================================================
# ==================================================


class Event(object):
    def __init__(self):
        super(Event, self).__init__()

    def do(self):
        pass

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


class StdoutDisplayEvent(DisplayEvent):
    def __init__(self, cdc=None):
        super(StdoutDisplayEvent, self).__init__()
        self.cdc = cdc

    def do(self):
        print(self.cdc)


# ==================================================
# IN
# ==================================================


class InEvent(Event):
    def __init__(self):
        super(InEvent, self).__init__()

    def done(self) :
        return False

# ==================================================


class Sensor(InEvent):
    def __init__(self, port=None):
        super(Sensor, self).__init__(port)
        assert port != None, "[Sensor init] bad port value"
        self.port = port
        self.change = False

    def raised(self):
        self.change = True

    def do(self):
        self.change = False

# ==================================================


class ButtonEvent(InEvent):
    def __init__(self):
        super(ButtonEvent, self).__init__()


class KeyboardEvent(InEvent):
    def __init__(self, c):
        super(KeyboardEvent, self).__init__()
        self.c = c


# ==================================================
# ==================================================
# ==================================================


class DynaPeNet(PeNet_I):
    def __init__(self):
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

    def estDeclanchable(self, t):
        return (self.UeT[t] <= self.Mi).all()

    def declancher(self, t):
        self.v_count[t] += 1
        self.Mi = self.Mi + self.UT[t]

    def next(self):
        t = super().next()
        a = self.F[t]
        if (a != None) and (isinstance(a, OutEvent)):
            a.do()
        return t

    def run(self):
        t = -1
        try:
            while(t != None):
                t = self.next()
            print("RdP bloqué !")
        except KeyboardInterrupt:
            print("Fin du RdP par interruption:")
        finally:
            print(self.Mi)
            print(self.v_count)


# ==================================================
# ==================================================
# ==================================================


if __name__ == '__main__':
    rdp2 = DynaPeNet()
    rdp2.load(("p1", "p2"), ("t1", "t2"), (("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2"), ("t2", "p1")),
              (1, 1, 1, 1),  (1, 1), (None, None))

    l = Listener(on_press=on_press, on_release=on_release)
    l.start()
    rdp2.run()
    l.stop()
    for (i, v) in keysDict.items():
        print(v)
