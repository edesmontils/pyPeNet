#!/usr/bin/env pybricks-micropython
# coding: utf8

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) pour exécuter sous EV3.
    TODO :
    - EV3PeNet
"""
from pyDynaPeNet import *

class EV3Motor(OutEvent):
    def __init__(self, port):
        OutEvent.__init__(self)
        assert (port != None) and (port in [Port.A, Port.B, Port.C, Port.D]), "[EV3Motor init] bad port value"
        self.port = port
        self.motor = Motor(self.port)

    def declencher(self) :
        self.motor.run_time(500, 200)
        print('>')


# ==================================================

class EV3Sensor(InEvent):
    def __init__(self, port):
        InEvent.__init__(self)
        assert port in [Port.S1, Port.S2, Port.S3, Port.S4], "[EV3Sensor init] bad port value"
        self.port = port
        self.change = False
        self.sensor = TouchSensor(self.port)

    def setDeclenchable(self):
        self.change = True

    def estDeclenchable(self):
        return self.sensor.pressed() #self.change

    def declencher(self):
        pass #self.change = False


# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':


    # Initialize the EV3 Brick.
    ev3 = EV3Brick()

    # # Initialize a motor at port B.
    # test_motor = Motor(Port.B)
    # print('test')
    # # Write your program here

    # # Play a sound.
    # ev3.speaker.beep()

    # # Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
    # test_motor.run_target(500, 90)

    # # Play another beep sound.
    # ev3.speaker.beep(frequency=1000, duration=500)

    rdp2 = DynaPeNet()
    rdp2.load(("p1", "p2"), 
              ("t0","t1", "t2"), 
              (("p1", "t1"), ("t1", "p2"),("p2", "t2"),("t0","p1") ),
              (1, 1, 1, 1),  
              (0, 1) )
    rdp2.setInEvent("t0",EV3Sensor(Port.S1))
    rdp2.setOutEvent("t1", StdoutDisplayEvent("====> t1 !"))
    rdp2.setOutEvent("t2", EV3Motor(Port.B))
    rdp2.run(delay=0)