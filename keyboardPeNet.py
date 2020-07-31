#!/usr/bin/env python3.7
# coding: utf8

# https://pythonhosted.org/pynput/keyboard.html & https://pythonhosted.org/pynput/mouse.html
from pynput.keyboard import Key, Listener
from pyDynaPeNet import *

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


if __name__ == '__main__':
    rdp2 = DynaPeNet()
    rdp2.load(("p0","p1", "p2"), ("t0","t1", "t2"), 
              (("t0","p0"),("p0","t1"), ("p1", "t1"), ("t1", "p2"), ("p2", "t2")),
              (1, 1, 1, 1, 1),  (0, 2, 0))
    rdp2.setInEvent("t0", KeyboardEvent('c'))
    rdp2.setOutEvent("t0", StdoutDisplayEvent("====> new c !"))
    rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 go !"))
    rdp2.setOutEvent("t2", StdoutDisplayEvent("T2 go !"))
    l = Listener(on_press=on_press, on_release=on_release)
    l.start()
    rdp2.run()
    l.stop()
    