#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) pour exécuter sous EV3.
    TODO :
    - EV3PeNet
"""
from pyDynaPeNet import *

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, UltrasonicSensor, TouchSensor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase



class EV3Motor(Action):
    def __init__(self, port):
        super(EV3Motor, self).__init__(port)
        assert (port != None) and (port in [Port.A, Port.B, Port.C, Port.D]), "[EV3Motor init] bad port value"




class EV3Sensor(Sensor):
    def __init__(self, port):
        super(EV3Sensor, self).__init__(port)
        assert port in [Port.S1, Port.S2, Port.S3, Port.S4], "[EV3Sensor init] bad port value"






# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':
    rdp2 = DynaPeNet()
    rdp2.load(("p1", "p2"), ("t1", "t2"), (("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2"), ("t2", "p1")), 
                                           (1, 1, 1, 1),  (1, 1), (None, Action('S1')))



    for i in range(15):
        rdp2.next()
        print(rdp2.Mi)