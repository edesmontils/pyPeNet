#!/usr/bin/env python3.7
# coding: utf8

""" Exécution d'un RdP "piloté" par le clavier """

# https://pythonhosted.org/pynput/keyboard.html & https://pythonhosted.org/pynput/mouse.html
from pynput.keyboard import Key, Listener
from pyDynaPeNet import *

keysDict = dict()
""" Tableau de caractères jouant le rôle de mémoire des touches utilisées : dict(str:int)"""


# def _runListener():
#     print('Start KeyboardListener')
#     try:
#         with Listener(on_press=_on_press, on_release=_on_release) as listener:
#             listener.join()
#     except KeyboardInterrupt:
#         print('End KeyboardListener')

def _on_press(key):
    pass  # print('{0} pressed'.format(key))

def _on_release(key):
    k = str(key)
    keysDict[k] = keysDict.get(k, 0) + 1
    #print(k,type(k))
    if key == Key.esc:
        # Stop listener
        return False


class KeyboardEvent(InEvent):
    """
        Classe permettant de gérer un événement clavier. Toutes les actions sont mémorisées.

        Parameters
        ----------
        c : str
            Touche associée à cet événement (espace par défaut)
    """
    def __init__(self, c = ' '):
        InEvent.__init__(self)
        self.c = "'"+str(c)+"'"
        """ La touche gérée par cet événement : str """

    def estDeclenchable(self) :
        return keysDict.get(self.c, 0) > 0

    def declencher(self) :
        keysDict[self.c] = keysDict[self.c] - 1


class KeyboardEventOnlyOne(KeyboardEvent):
    """
        Classe permettant de gérer un événement clavier. Toutes les actions d'un caractère sont vidées lors d'une exécution.
    """
    def __init__(self, c = ' '):
        KeyboardEvent.__init__(self,c)

    def declencher(self) :
        keysDict[self.c] = 0


# ==================================================
# ==================================================
# ==================================================


if __name__ == '__main__':
    rdp2 = DynaPeNet()
    rdp2.load(("p0","p1", "p2"), ("t0","t1", "t2"), 
              (("t0","p0"),("p0","t1"), ("p1", "t1"), ("t1", "p2"), ("p2", "t2")),
              (1, 1, 1, 1, 1),  (0, 2, 0))
    rdp2.setInEvent("t0", KeyboardEvent('c'))
    rdp2.setOutEvent("t0", StdoutDisplayEvent("====> new c !"))
    rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 go !"))
    rdp2.setOutEvent("t2", StdoutDisplayEvent("T2 go !"))
    l = Listener(on_press=_on_press, on_release=_on_release)
    l.start()
    rdp2.run()
    l.stop()
    