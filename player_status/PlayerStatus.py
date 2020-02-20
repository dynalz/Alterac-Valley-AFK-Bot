import logging
import pyautogui
from time import sleep
from utils.__utils__ import chance
from datetime import datetime, timedelta
from random import uniform, choice, randint
from .PlayerControls import PlayerControls
from spam_functions import can_queue_in_av

class PlayerStatus(PlayerControls):
  def __init__(self, *args, **kwargs):
    self.afk_till = None
    self.is_in_queue = False
    self.is_logged_out = False
    self.current_location = None
    super(PlayerStatus, self).__init__(*args, **kwargs)

  def log_out(self):
    self.remove_afk()
    self.is_in_queue = False
    self.is_logged_out = True
    self.current_location = None

  def log_in(self):
    self.is_logged_out = False

  def is_in_battleground(self):
    return can_queue_in_av() and self.current_location == 'AV'

  def is_running(self):
    return self.running

  def change_location(self, location):
    if location != self.current_location:
      self.current_location = location
      self.remove_afk()

  def died(self):
    self.running = False

  def set_afk(self, minutes=None):
    self.afk_till = datetime.now() + timedelta(minutes=minutes if minutes else uniform(10, 25))
    logging.info(f'Player is now AFK till {self.afk_till.hour}:{self.afk_till.minute}')

  def remove_afk(self):
    self.afk_till = None

  def is_afk(self):
    return self.afk_till and self.afk_till > datetime.now()

  def get_random_no_action_required_time(self):
    if self.is_in_battleground():
      return uniform(12, 90)
    return uniform(7, 30)

Player = PlayerStatus()