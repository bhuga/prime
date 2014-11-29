#!/usr/bin/python
import cwiid
import sys
import time
from os import system

class Wheel(object):

    def __init__(self, side, handicap):
        self.speed = 0
        self.start_speed = 50
        self.side = side
        self.handicap = handicap

    def run(self, command):
        res = system(command)
        if res != 0:
          raise NameError(command + " returned " + str(res))
        
    def accelerate(self):
        self.set_speed(100)

    def decelerate(self):
        if True:
          self.set_speed(0)

    def set_speed(self, new):
        fixed = max(-100, min(new, 100))
        if fixed < 0:
          self.run("./backwards-" + self.side)
        else:
          self.run("./forward-" + self.side)
        self.speed = fixed
        self.run("./pwm-" + self.side + " " + str(self.handicap * (abs(fixed) / 100.0)))

    def add_speed(self, amount):
        self.set_speed(amount + self.speed)

class Car(object):
    def __init__(self):
        self.left = Wheel("left", 0.80)
        self.right = Wheel("right", 1.0)
        self.turn_speed = 50

    def accelerate(self):
        self.left.accelerate()
        self.right.accelerate()

    def decelerate(self):
        self.left.decelerate()
        self.right.decelerate()

    def reverse(self):
        self.left.set_speed(-100)
        self.right.set_speed(-100)

    def turn_left(self):
        print "turning left"
        if self.left.speed > 0:
          self.left.set_speed(self.right.speed - self.turn_speed)
        else:
          self.left.set_speed(self.right.speed + self.turn_speed)

    def turn_right(self):
        print "turning right"
        if self.right.speed > 0:
          self.right.set_speed(self.left.speed - self.turn_speed)
        else:
          self.right.set_speed(self.left.speed + self.turn_speed)

    def spin_left(self):
        self.left.set_speed(-100)
        self.right.set_speed(100)

    def spin_right(self):
        self.right.set_speed(-100)
        self.left.set_speed(100)

    def print_state(self):
        print "car:" + str(self.left.speed) + "    " + str(self.right.speed)

class Controller(object):
    def __init__(self, wiimote):
        self.wiimote = wiimote

    def button_2_pressed(self):
        return self.wiimote.state['buttons'] & cwiid.BTN_2 == cwiid.BTN_2

    def left_pressed(self):
        # no idea why cwiid.BTN_LEFT is 256 and when we press it we get 2048
        return self.wiimote.state['buttons'] & 2048 == 2048

    def right_pressed(self):
        return self.wiimote.state['buttons'] & 1024 == 1024

    def b_pressed(self):
        return self.wiimote.state['buttons'] & cwiid.BTN_B == cwiid.BTN_B

    def back_pressed(self):
        # print "read:" + str(self.wiimote.state['buttons']) + " compared to " + str(cwiid.BTN_DOWN)
        return self.wiimote.state['buttons'] & 256 == 256

menu = '''1: toggle LED 1
2: toggle LED 2
3: toggle LED 3
4: toggle LED 4
5: toggle rumble
a: toggle accelerometer reporting
b: toggle button reporting
c: enable motionplus, if connected
e: toggle extension reporting
i: toggle ir reporting
m: toggle messages
p: print this menu
r: request status message ((t) enables callback output)
s: print current state
t: toggle status reporting
x: exit'''

car = Car()

def main():
  system("./setup_pin_modes.sh")
  led = 0
  rpt_mode = 0
  rumble = 0
  mesg = False
  #Connect to address given on command-line, if present
  print 'Put Wiimote in discoverable mode now (press 1+2)...'
  global wiimote
  if len(sys.argv) > 1:
    wiimote = cwiid.Wiimote(sys.argv[1])
  else:
    wiimote = cwiid.Wiimote()
  controller = Controller(wiimote)
  wiimote.mesg_callback = callback
  print "Wiimote connected!"
  led ^= cwiid.LED1_ON
  wiimote.led = led
  rpt_mode ^= cwiid.RPT_BTN
  wiimote.rpt_mode = rpt_mode

  exit = 0
  while True:
    #print_state(wiimote.state)
    if controller.button_2_pressed():
        car.accelerate()
        if controller.left_pressed():
            car.turn_left()
        elif controller.right_pressed():
            car.turn_right()
    elif controller.b_pressed():
        if controller.left_pressed():
            car.spin_left()
        elif controller.right_pressed():
            car.spin_right()
        else:
            car.decelerate()
    elif controller.back_pressed():
      car.reverse()
      if controller.left_pressed():
          car.turn_left()
      elif controller.right_pressed():
          car.turn_right()
    else:
        car.decelerate()
    car.print_state()
    time.sleep (0.1)

# nothing past this gets called, whatevs.

  while not exit:
    c = sys.stdin.read(1)
    if c == '1':
      led ^= cwiid.LED1_ON
      wiimote.led = led
    elif c == '2':
      led ^= cwiid.LED2_ON
      wiimote.led = led
    elif c == '3':
      led ^= cwiid.LED3_ON
      wiimote.led = led
    elif c == '4':
      led ^= cwiid.LED4_ON
      wiimote.led = led
    elif c == '5':
      rumble ^= 1
      wiimote.rumble = rumble
    elif c == 'a':
      rpt_mode ^= cwiid.RPT_ACC
      wiimote.rpt_mode = rpt_mode
    elif c == 'b':
      rpt_mode ^= cwiid.RPT_BTN
      wiimote.rpt_mode = rpt_mode
    elif c == 'c':
      wiimote.enable(cwiid.FLAG_MOTIONPLUS)
    elif c == 'e':
      rpt_mode ^= cwiid.RPT_EXT
      wiimote.rpt_mode = rpt_mode
    elif c == 'i':
      rpt_mode ^= cwiid.RPT_IR
      wiimote.rpt_mode = rpt_mode
    elif c == 'm':
      mesg = not mesg
      if mesg:
        wiimote.enable(cwiid.FLAG_MESG_IFC);
      else:
        wiimote.disable(cwiid.FLAG_MESG_IFC);
    elif c == 'p':
      print menu
    elif c == 'r':
      print "requesting status"
      wiimote.request_status()
    elif c == 's':
      print_state(wiimote.state)
    elif c == 't':
      rpt_mode ^= cwiid.RPT_STATUS
      wiimote.rpt_mode = rpt_mode
    elif c == 'x':
      exit = -1;
    elif c == '\n':
      pass
    else:
      print 'invalid option'

  wiimote.close()

def print_buttons(state):
  button1 = state['buttons'] & cwiid.BTN_1 == cwiid.BTN_1
  if button1:
    print "Button 1 pressed"
  else:
   print "Button 1 not pressed"

def print_state(state):
  #  print 'Report Mode:',
  #for r in ['STATUS', 'BTN', 'ACC', 'IR', 'NUNCHUK', 'CLASSIC', 'BALANCE', 'MOTIONPLUS']:
  #  if state['rpt_mode'] & eval('cwiid.RPT_' + r):
    #      print r,
  # print

  #print 'Active LEDs:',
 # for led in ['1','2','3','4']:
#    if state['led'] & eval('cwiid.LED' + led + '_ON'):
  #      print led,
  #  print

  #print 'Rumble:', state['rumble'] and 'On' or 'Off'

  #print 'Battery:', int(100.0 * state['battery'] / cwiid.BATTERY_MAX)

  if 'buttons' in state:
    print 'Buttons:', state['buttons']

  if 'acc' in state:
    print 'Acc: x=%d y=%d z=%d' % (state['acc'][cwiid.X],
                                   state['acc'][cwiid.Y],
                                   state['acc'][cwiid.Z])

  if 'ir_src' in state:
    valid_src = False
    print 'IR:',
    for src in state['ir_src']:
      if src:
        valid_src = True
        print src['pos'],

    if not valid_src:
      print 'no sources detected'
    else:
      print

  if state['ext_type'] == cwiid.EXT_NONE:
    pass #print 'No extension'
  elif state['ext_type'] == cwiid.EXT_UNKNOWN:
    print 'Unknown extension attached'
  elif state['ext_type'] == cwiid.EXT_NUNCHUK:
    if state.has_key('nunchuk'):
      print 'Nunchuk: btns=%.2X stick=%r acc.x=%d acc.y=%d acc.z=%d' % \
        (state['nunchuk']['buttons'], state['nunchuk']['stick'],
         state['nunchuk']['acc'][cwiid.X],
         state['nunchuk']['acc'][cwiid.Y],
         state['nunchuk']['acc'][cwiid.Z])
  elif state['ext_type'] == cwiid.EXT_CLASSIC:
    if state.has_key('classic'):
      print 'Classic: btns=%.4X l_stick=%r r_stick=%r l=%d r=%d' % \
        (state['classic']['buttons'],
         state['classic']['l_stick'], state['classic']['r_stick'],
         state['classic']['l'], state['classic']['r'])
  elif state['ext_type'] == cwiid.EXT_BALANCE:
    if state.has_key('balance'):
      print 'Balance: right_top=%d right_bottom=%d left_top=%d left_bottom=%d' % \
        (state['balance']['right_top'], state['balance']['right_bottom'],
         state['balance']['left_top'], state['balance']['left_bottom'])
  elif state['ext_type'] == cwiid.EXT_MOTIONPLUS:
    if state.has_key('motionplus'):
      print 'MotionPlus: angle_rate=(%d,%d,%d)' % state['motionplus']['angle_rate']

def callback(mesg_list, time):
  print 'time: %f' % time
  for mesg in mesg_list:
    if mesg[0] == cwiid.MESG_STATUS:
      print 'Status Report: battery=%d extension=' % \
             mesg[1]['battery'],
      if mesg[1]['ext_type'] == cwiid.EXT_NONE:
        print 'none'
      elif mesg[1]['ext_type'] == cwiid.EXT_NUNCHUK:
        print 'Nunchuk'
      elif mesg[1]['ext_type'] == cwiid.EXT_CLASSIC:
        print 'Classic Controller'
      elif mesg[1]['ext_type'] == cwiid.EXT_BALANCE:
        print 'Balance Board'
      elif mesg[1]['ext_type'] == cwiid.EXT_MOTIONPLUS:
        print 'MotionPlus'
      else:
        print 'Unknown Extension'

    elif mesg[0] == cwiid.MESG_BTN:
      print 'Button Report: %.4X' % mesg[1]

    elif mesg[0] == cwiid.MESG_ACC:
      print 'Acc Report: x=%d, y=%d, z=%d' % \
            (mesg[1][cwiid.X], mesg[1][cwiid.Y], mesg[1][cwiid.Z])

    elif mesg[0] == cwiid.MESG_IR:
      valid_src = False
      print 'IR Report: ',
      for src in mesg[1]:
        if src:
          valid_src = True
          print src['pos'],

      if not valid_src:
        print 'no sources detected'
      else:
        print

    elif mesg[0] == cwiid.MESG_NUNCHUK:
      print ('Nunchuk Report: btns=%.2X stick=%r ' + \
             'acc.x=%d acc.y=%d acc.z=%d') % \
            (mesg[1]['buttons'], mesg[1]['stick'],
             mesg[1]['acc'][cwiid.X], mesg[1]['acc'][cwiid.Y],
             mesg[1]['acc'][cwiid.Z])
    elif mesg[0] == cwiid.MESG_CLASSIC:
      print ('Classic Report: btns=%.4X l_stick=%r ' + \
             'r_stick=%r l=%d r=%d') % \
            (mesg[1]['buttons'], mesg[1]['l_stick'],
             mesg[1]['r_stick'], mesg[1]['l'], mesg[1]['r'])
    elif mesg[0] ==  cwiid.MESG_BALANCE:
      print ('Balance Report: right_top=%d right_bottom=%d ' + \
             'left_top=%d left_bottom=%d') % \
            (mesg[1]['right_top'], mesg[1]['right_bottom'],
             mesg[1]['left_top'], mesg[1]['left_bottom'])
    elif mesg[0] == cwiid.MESG_MOTIONPLUS:
      print 'MotionPlus Report: angle_rate=(%d,%d,%d)' % \
            mesg[1]['angle_rate']
    elif mesg[0] ==  cwiid.MESG_ERROR:
      print "Error message received"
      global wiimote
      wiimote.close()
      exit(-1)
    else:
      print 'Unknown Report'

main()
