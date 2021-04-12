#!/usr/bin/env pybricks-micropython
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) pour exécuter sous EV3.

    .. warning:: documentation à faire
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port, Color, Button
from pyDynaPeNet import *




# ==================================================
# ================ Entrées =========================
# ==================================================

class EV3Sensor(InEvent):
    def __init__(self, port):
        InEvent.__init__(self)
        assert port in [Port.S1, Port.S2, Port.S3, Port.S4], "[EV3Sensor init] bad port value"
        self.port = port

    def estDeclenchable(self):
        return False

    def declencher(self):
        pass

# ==================================================

class EV3TouchSensor(EV3Sensor):
    def __init__(self, port):
        EV3Sensor.__init__(self,port)
        self.sensor = TouchSensor(self.port)

    def estDeclenchable(self):
        return self.sensor.pressed()

# ==================================================

class EV3ColorSensor(EV3Sensor):
    def __init__(self, port):
        EV3Sensor.__init__(self,port)
        self.sensor = ColorSensor(self.port)

class EV3ColorSensorColor(EV3ColorSensor):
    colorList = [Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN, Color.PURPLE, None]

    def __init__(self, port, color):
        assert color in self.colorList, "[EV3ColorSensor init] bad color value"
        EV3ColorSensor.__init__(self,port)
        self.color = color 

    def estDeclenchable(self):
        return self.sensor.color() == self.color

class EV3ColorSensorAmbient(EV3ColorSensor):
    def __init__(self, port, ambient):
        EV3ColorSensor.__init__(self,port)
        self.ambient = ambient 

    def estDeclenchable(self):
        return self.sensor.ambient() == self.ambient

class EV3ColorSensorReflection(EV3ColorSensor):
    def __init__(self, port, reflection):
        EV3ColorSensor.__init__(self,port)
        self.reflection = reflection 

    def estDeclenchable(self):
        return self.sensor.reflection() == self.reflection

class EV3ColorSensorRGB(EV3ColorSensor):
    def __init__(self, port, r,g,b):
        EV3ColorSensor.__init__(self,port)
        self.r = r 
        self.g = g
        self.b = b

    def estDeclenchable(self):
        (r,g,b) = self.sensor.rgb()
        return (r==self.r) and (g==self.g) and (b==self.b)

# ==================================================

class EV3UltrasonicSensor(EV3Sensor):
    def __init__(self, port, distance):
        EV3Sensor.__init__(self,port)
        self.sensor = UltrasonicSensor(self.port)
        self.distance = distance

    def estDeclenchable(self):
        return self.sensor.distance() == self.distance # en mm

# ==================================================

class EV3GyroscopicSensor(EV3Sensor):
    def __init__(self, port):
        EV3Sensor.__init__(self,port)
        self.sensor = GyroSensor(self.port)


class EV3GyroscopicSensorSpeed(EV3GyroscopicSensor):
    def __init__(self, port, speed):
        EV3GyroscopicSensor.__init__(self,port)
        self.speed = speed

    def estDeclenchable(self):
        return self.sensor.speed() == self.speed # en deg/s

class EV3GyroscopicSensor(EV3GyroscopicSensor):
    def __init__(self, port, angle, startAngle=None):
        EV3GyroscopicSensor.__init__(self,port)
        self.angle = angle
        if startAngle is not None : 
            self.sensor.reset_angle(startAngle)

    def estDeclenchable(self):
        return self.sensor.angle() == self.angle # en deg

# ==================================================

class EV3Button(InEvent):
    buttonList = [Button.LEFT_DOWN, Button.LEFT, Button.LEFT_UP, Button.UP, Button.RIGHT_UP, Button.RIGHT, Button.RIGHT_DOWN, Button.DOWN, Button.CENTER]

    def __init__(self, ev3, btn):
        InEvent.__init__(self)
        assert btn in self.buttonList, "[EV3Button init] bad button value"
        self.button = btn
        self.ev3 = ev3

    def estDeclenchable(self):
        return self.button in self.ev3.buttons.pressed()

# ==================================================
# =============== Sorties ==========================
# ==================================================

class EV3Motor(OutEvent):
    def __init__(self, port, speed):
        OutEvent.__init__(self)
        assert (port != None) and (port in [Port.A, Port.B, Port.C, Port.D]), "[EV3Motor init] bad port value"
        self.port = port
        self.speed = speed
        self.motor = Motor(self.port)

    def declencher(self) :
        self.motor.run(500)

class EV3MotorTime(EV3Motor):
    def __init__(self, port, speed, duration):
        EV3Motor.__init__(self, port, speed)
        self.duration = duration

    def declencher(self) :
        self.motor.run_time(self.speed, self.duration)

# ==================================================

class EV3LightOn(OutEvent):

    colorList = [Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN, Color.PURPLE, None]

    def __init__(self, ev3, color):
        OutEvent.__init__(self)
        assert color in self.colorList, "[EV3LightOn init] bad color value"
        self.ev3 = ev3
        self.color = color

    def declencher(self) :
        self.ev3.light.on(self.color)

class EV3LightOff(OutEvent):
    
    def __init__(self, ev3):
        OutEvent.__init__(self)
        self.ev3 = ev3

    def declencher(self) :
        self.ev3.light.off()


# ==================================================

class EV3Say(OutEvent):
    
    def __init__(self, ev3, text, langue = 'fr-fr'):
        OutEvent.__init__(self)
        self.ev3 = ev3
        self.text = text
        self.ev3.speaker.set_speech_options(language=langue)

    def declencher(self) :
        self.ev3.speaker.say(self.text)

# ==================================================

class EV3StdoutDisplay(DisplayEvent):
    def __init__(self, ev3, cdc=None):
        DisplayEvent.__init__(self)
        self.cdc = cdc
        self.ev3 = ev3

    def declencher(self) :
        self.ev3.screen.print(self.cdc)

class EV3StdoutClear(DisplayEvent):
    def __init__(self, ev3):
        DisplayEvent.__init__(self)
        self.ev3 = ev3

    def declencher(self) :
        self.ev3.screen.clear()


# ==================================================
# ==================================================
# ==================================================

class EV3PeNet(DynaPeNet):
    def __init__(self, ev3):
        DynaPeNet.__init__(self)
        self.ev3 = ev3
        ev3.speaker.say("Let's go!")

# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':

    rdp2 = EV3PeNet(EV3Brick())
    rdp2.load(("p1", "p2"), 
              ("t0","t1", "t2"), 
              (("p1", "t1"), ("t1", "p2"),("p2", "t2"),("t0","p1") ),
              (1, 1, 1, 1),  
              (0, 1) )
    rdp2.setOutEvent("t0",EV3LightOn(rdp2.ev3, Color.RED))
    rdp2.setInEvent("t0",EV3TouchSensor(Port.S1))
    rdp2.setInEvent("t1",EV3Button(rdp2.ev3, Button.CENTER))
    rdp2.setOutEvent("t1", EV3StdoutDisplay(rdp2.ev3,"====> t1 !"))
    rdp2.setOutEvent("t2", EV3Say(rdp2.ev3, "Moteur !"))
    rdp2.setOutEvent("t2", EV3MotorTime(Port.B,200,600))
    rdp2.setOutEvent("t2", EV3LightOff(rdp2.ev3))
    rdp2.run(delay=0)