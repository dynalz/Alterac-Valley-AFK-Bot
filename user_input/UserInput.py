import logging
import keyboard
import pyautogui
from threading import Thread
from time import time, sleep

BOT_KEYS = ['a', 's', 'd', 'w', 'i', 'f1', 'esc', 'space', 'enter', 'up', 'left', 'right', 'down', 'num lock', 'c', 'shift', '/', '?', 'left shift']

class UserInput(Thread):
  def __init__(self, *args, **kwargs):
    self.last_key_pressed = None
    self.last_mouse_position = None
    self.record_mouse_movements = True
    self.last_action_time = time() - 1000
    super(UserInput, self).__init__(*args, **kwargs)
    self.setDaemon(True)

  def disable_record_mouse_movements(self):
    self.record_mouse_movements = False

  def enable_record_mouse_movements(self):
    self.record_mouse_movements = True

  def has_received_user_input_in_last_minute(self):
    return time() - self.last_action_time < 60

  def set_last_action_time(self, time):
    if not self.has_received_user_input_in_last_minute():
      logging.info("Found User Input, going to sleep for 60 secs")
    self.last_action_time = time

  def key_pressed_event(self, key):
    if key.name.lower() in BOT_KEYS:
      return
    self.last_key_pressed = key
    self.set_last_action_time(time())
    #print("Key Pressed: {}".format(key))

  def set_mouse_current_position(self):
    self.last_mouse_position = pyautogui.position()

  def run(self):
    keyboard.on_press(self.key_pressed_event)
    self.set_mouse_current_position()
    while(True):
      #print(f"UserInput: {self.has_received_user_input_in_last_minute()} => How Long Ago: {int(time() - self.last_action_time) if self.last_action_time else None}")
      sleep(0.1)
      if not self.record_mouse_movements:
        continue
      current_mouse_position = pyautogui.position()
      if self.last_mouse_position != current_mouse_position:
        self.last_mouse_position = current_mouse_position
        self.set_last_action_time(time())


UserInput = UserInput()
