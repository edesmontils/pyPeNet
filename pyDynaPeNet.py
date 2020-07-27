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

#from multiprocessing import Manager
import time
# ==================================================
# ==================================================
# ==================================================


class Event(object):
    def __init__(self):
        super(Event, self).__init__()

    def declencher(self) :
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

    def declencher(self) :
        print(self.cdc)


# ==================================================
# IN
# ==================================================


class InEvent(Event):
    def __init__(self):
        super(InEvent, self).__init__()

    def estDeclenchable(self) :
        return False

    def declencher(self) :
        pass

# ==================================================


class Sensor(InEvent):
    def __init__(self, port=None):
        super(Sensor, self).__init__(port)
        assert port != None, "[Sensor init] bad port value"
        self.port = port
        self.change = False

    def raised(self):
        self.change = True

    def declencher(self):
        self.change = False

# ==================================================


class ButtonEvent(InEvent):
    def __init__(self):
        super(ButtonEvent, self).__init__()

# ==================================================

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
    #print(k,type(k))
    if key == Key.esc:
        # Stop listener
        return False


class KeyboardEvent(InEvent):
    def __init__(self, c = ' '):
        InEvent.__init__(self)
        self.c = "'"+str(c)+"'"

    def estDeclenchable(self) :
        return keysDict.get(self.c, 0) > 0

    def declencher(self) :
        keysDict[self.c] = keysDict[self.c] - 1


class KeyboardEventOnlyOne(KeyboardEvent):
    def __init__(self, c = ' '):
        KeyboardEvent.__init__(self,c)

    def declencher(self) :
        keysDict[self.c] = 0



# ==================================================
# ==================================================
# ==================================================


class DynaPeNet(PeNet_I):
    def __init__(self):
        PeNet_I.__init__(self)
        self.F_In = list()
        self.F_Out = list()

    def load(self, P, T, A, W, M0, FI = None, FO = None):
        super().load(P, T, A, W, M0)
        if FI == None :
            self.F_In = [None] * len(self.T)
        else:
            self.F_In = FI
        assert self.nbt == len(self.F_In), "[load] incohérence entre F_In et T"
        if FO == None :
            self.F_Out = [None] * len(self.T)
        else:
            self.F_Out = FO
        assert self.nbt == len(self.F_Out), "[load] incohérence entre F_Out et T"


    def setInEvent(self, t, inEvt) :
        assert isinstance(inEvt, InEvent), "[setInEvent] mauvais type d'event"
        if t in self.T:
            i = self.T.index(t)
            self.F_In[i] = inEvt
        else:
            pass

    def setOutEvent(self, t, outEvt):
        assert isinstance(outEvt, OutEvent), "[setOutEvent] mauvais type d'event"
        if t in self.T:
            i = self.T.index(t)
            self.F_Out[i] = outEvt
        else:
            pass

    def estDeclenchable(self, t):
        dec = super().estDeclenchable(t)
        a = self.F_In[t]
        if dec and (a != None) and (isinstance(a, InEvent)):
            return dec and a.estDeclenchable()
        else:
            return dec

    def declencher(self, t):
        super().declencher(t)
        a = self.F_In[t]
        if (a != None) and (isinstance(a, InEvent)):
            a.declencher()
        a = self.F_Out[t]
        if (a != None) and (isinstance(a, OutEvent)):
            a.declencher()

    def run(self):
        t = -1
        try:
            while(1):
                t = self.next()
                if t!=None : print(self.sequence)
                time.sleep(1)
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
    rdp2.load(("p0","p1", "p2"), ("t0","t1", "t2"), (("t0","p0"),("p0","t1"), ("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2")),
              (1, 1, 1, 1, 1),  (0, 2, 0))#, (KeyboardEvent('c'), None, None),  (None, StdoutDisplayEvent("T1 go !"), StdoutDisplayEvent("T2 go !") ) )
    rdp2.setInEvent("t0", KeyboardEvent('c'))
    rdp2.setOutEvent("t0", StdoutDisplayEvent("====> new c !"))
    rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 go !"))
    rdp2.setOutEvent("t2", StdoutDisplayEvent("T2 go !"))
    l = Listener(on_press=on_press, on_release=on_release)
    l.start()
    rdp2.run()
    l.stop()