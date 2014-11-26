Optimus prime
=============

you know, the robot.


#### Wiring diagram

vnh2sp30 pins are counted left-to-right with the pins at the bottom of your
viewport (vision)

| pi pin | bcm gpio # | wiringpi pin | vnh2sp30 pin |  description |
|--------|------------|--------------|--------------|--------------|
| 2 | | | | usb cable +5v |
| 4 | | | 8 | +5v vnh2sp30 controller power |
| 6 | | | | usb cable ground |
| 8 | | | usb cable terminal signal |
| 9 | | | 7 or 9 | ground for vnh |
| 10 | | | usb cable terminal signal |
| 11 | 17 | 0 | 4 | right wheel pwm |
| 12 | 18 | 1 | 12 | left wheel pwm |
| 16 | 23 | 4 | 13 | left wheel backward |
| 18 | 24 | 5 | 14 | left wheel forward |
| 21 | 9 | 13 | 3 | right wheel forward |
| 23 | 11 | 14 | 2 | right wheel backward |
 
