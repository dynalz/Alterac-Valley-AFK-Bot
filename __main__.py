import sys,os
sys.path.append(os.getcwd()+'\\utils')
import logging
from constants import *
from spam_functions import *
from utils.__utils__ import *
from random import randint, uniform
from user_input.UserInput import UserInput
from player_status.PlayerStatus import Player
from utils.WindowsController.Windows import Windows
logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO, datefmt='%H:%M:%S')


#Player.current_location = "AV"
def main():
  avs_count = 0
  logging.info('Init')
  just_entered_bg = False
  while True:
    try:
      guarantee_game_ready_for_action()
      if just_entered_bg:
        av_setup(Player)
        just_entered_bg = False
      elif Player.is_in_battleground() and not in_queue_or_av():
        Player.change_location("Orgrimmar")
      elif not Player.is_afk() and chance(10):
        Player.jump(multiple=True)
      elif Player.is_in_battleground() and chance(50):
        if can_av_recall() and chance(5):
          Player.stop_autorun()
          av_recall()
        elif chance(10):
          Player.stop_autorun()
          Player.jump()
          sleep(15)
        else:
          Player.random_unstuck_movement()

      if is_time_to_logout() and not in_queue_or_av():
        log_out()
        logging.info('Logged out')
        Player.log_out()
        return
      if not in_queue_or_av():
        if can_queue_in_av():
          if queue_av():
            logging.info('Queued to Alterac Valley')
            if chance(70):
              Player.set_afk()
        else:
          logging.info('Cannot queue into AV due to debuff')
          Player.change_location("Orgrimmar")
          if not Player.is_afk():
            Player.set_afk(15)
      if av_queue_popped():
        enter_av()
        just_entered_bg = True
        logging.info('Entered Alterac Valley.')
        Player.change_location("AV")
      if av_finished():
        leave_av()
        avs_count += 1
        logging.info(f'AV Finished, exiting. AVs done: {avs_count}')
        Player.change_location("Orgrimmar")
        if not is_time_to_logout() and chance(5):
          sleep(10)
          log_out()
          logging.info('Random logged out')
          sleep(randint(200, 1000))
          pyautogui.press('enter')
          logging.info('Logged back in')
          sleep(10)
    except:
      logging.exception("Exception in main execution")
      save_screenshot(take_screenshot())
      os._exit(1)
    finally:
      if not just_entered_bg and not Player.is_afk()\
      and not UserInput.has_received_user_input_in_last_minute()\
      and chance(80):
        tab_out_and_random_activity(Player)
        sleep(uniform(0.2, 1.5))
        if Player.is_in_battleground():
          Player.random_avoid_afk_action()
      else:
        sleep(uniform(3, 10))
      while UserInput.has_received_user_input_in_last_minute():
        sleep(1)

def log_in_when_ready():
  logging.info('APP is paused, logging back in when its time to log')
  while is_time_to_logout():
    sleep(randint(300, 1800))
  press('esc')
  kill_game_window()
  logging.info('Logging back in')
  init_game_window()
  Player.log_in()


if __name__ == "__main__":
  UserInput.start()
  Windows.deny_shutdown()
  while True:
    if not is_time_to_logout():
      main()
    log_in_when_ready()

