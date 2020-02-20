from time import sleep
from random import uniform, choice, randint
from utils.__utils__ import chance, keyDown, keyUp, press, hotkey

AVOID_AFK_ACTIONS = \
  [['jump']]*5 +\
  [['forward', 'forward_release']]*3 +\
  [['backwards', 'backwards_release']]*3 +\
  [['right', 'right_release']]*3 +\
  [['left', 'left_release']]*3 +\
  [['forward', 'jump', 'forward_release']]*2 +\
  [['backwards', 'jump', 'backwards_release']]*2 +\
  [['right', 'jump', 'right_release']]*2 +\
  [['left', 'jump', 'left_release']]*2 +\
  [['forward', 'right', 'jump', 'right_release', 'forward_release']] +\
  [['forward', 'left', 'jump', 'left_release', 'forward_release']] +\
  [['backwards', 'right', 'jump', 'right_release', 'backwards_release']] +\
  [['backwards', 'left', 'jump', 'left_release', 'backwards_release']]

class PlayerControls():
  def __init__(self):
    self.running = False

  def forward(self):
    keyDown('w')

  def backwards(self):
    keyDown('s')

  def right(self):
    keyDown('d')

  def left(self):
    keyDown('a')

  def forward_release(self):
    keyUp('w')

  def backwards_release(self):
    keyUp('s')

  def right_release(self):
    keyUp('d')

  def left_release(self):
    keyUp('a')

  def jump(self, multiple=False):
    if multiple:
      for i in range(randint(1, 12)):
        self.jump()
        sleep(uniform(0.125, 0.25))
    else:
      press('space')

  def random_unstuck_movement(self):
    self.stop_autorun()
    self.backwards_unstuck()
    sleep(uniform(0.05, 0.2))
    self.autorun()
    sleep(uniform(0.05, 0.2))
    self.stealth()
    side = choice(['a', 'd'])
    keyDown(side)
    self.jump(multiple=True)
    sleep(uniform(0, 1))
    keyUp(side)

  def random_avoid_afk_action(self):
    last_action_was_jump = False
    actions = choice(AVOID_AFK_ACTIONS)
    for action in actions:
      if action != 'jump':
        last_action_was_jump = False
        sleep(uniform(0.03, 0.15))
      else:
        last_action_was_jump = True
      getattr(self, action)()
    
  def backwards_unstuck(self):
    if chance(50):
      return
    side = choice(['a', 'd'])
    keyDown('s')
    keyDown(side)
    for i in range(randint(5, 20)):
      self.jump()
      sleep(uniform(0.1, 0.2))
    sleep(uniform(0, 1))
    keyUp(side)
    keyUp('s')


  def autorun(self):
    press('numlock')
    self.running = True

  def stop_autorun(self):
    self.running = False
    keyDown('w')
    keyUp('w')
  
  def toggle_slow_walk(self):
    hotkey('shift', '/')

  def stealth(self):
    press('c')