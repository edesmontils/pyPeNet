#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

from pyDynaPeNet import *

# Create your objects here






# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize a motor at port B.
test_motor = Motor(Port.B)
print('test')
# Write your program here

# Play a sound.
ev3.speaker.beep()

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(500, 90)

# Play another beep sound.
ev3.speaker.beep(frequency=1000, duration=500)


rdp2 = DynaPeNet()
rdp2.load(("p0","p1", "p2"), 
          ("t0","t1", "t2"), 
          (("t0","p0"),("p0","t1"), ("p1", "t1"), ("t1", "p2"),("p2", "t2")),
          (1, 1, 1, 1, 1),
          (0, 2, 0) )#, (KeyboardEvent('c'), None, None),  (None, StdoutDisplayEvent("T1 go !"), StdoutDisplayEvent("T2 go !") ) )
rdp2.setOutEvent("t0", StdoutDisplayEvent("====> new c !"))
rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 go !"))
rdp2.setOutEvent("t2", StdoutDisplayEvent("T2 go !"))
rdp2.run()
