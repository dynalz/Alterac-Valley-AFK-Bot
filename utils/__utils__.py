import psutil
import logging
import win32gui
import win32con
import pyautogui
from math import sqrt
from constants import *
from datetime import datetime
from utils.imagesearch import *
from pyclick import HumanClicker
from random import uniform, choice
from user_input.UserInput import UserInput
from func_timeout import func_timeout, FunctionTimedOut
pyautogui.FAILSAFE = False
from time import sleep, time

human_clicker = HumanClicker()

def is_time_to_logout():
  timezone_hour = datetime.now().hour
  return timezone_hour >= LOGOUT_BETWEEN_HOURS[0] and timezone_hour < LOGOUT_BETWEEN_HOURS[1]

def timeout(time=10):
  def _wrapper(fn):
    def wrapper(*args, **kwargs):
      try:
        return func_timeout(time, fn, args=args, kwargs=kwargs)
      except KeyboardInterrupt:
        raise
      except FunctionTimedOut:
        logging.info(f'Timeout on function: {fn.__name__}, args: {args}, kwargs: {kwargs}')
        save_screenshot(take_screenshot())
        return False
    return wrapper
  return _wrapper

def stop_if_user_input(fn):
  def wrapper(*args, **kwargs):
    if UserInput.has_received_user_input_in_last_minute():
      return
    return fn(*args, **kwargs)
  return wrapper

@timeout(20)
def assure_img_present(img):
  while not imagesearch(img):
    sleep(0.1)
  return True

def get_distance(p1,p2):
  return abs((p1) - (p2))

def get_speed_from_pos_to_pos(current_position, final_position):
  dx = get_distance(current_position[0], final_position[0])
  dy = get_distance(current_position[1], final_position[1])
  distance = sqrt(dx**2 + dy**2)
  return distance/uniform(1200, 2000)

def move_cursor(image=None, cords=None):
  current_position = pyautogui.position()
  if image:
    cords = imagesearch(image)
    move_to_position = get_random_position_in_img(image, cords)
    move_to_position = (int(move_to_position[0]), int(move_to_position[1]))
  elif cords:
    move_to_position = (int(cords[0]), int(cords[1]))
  UserInput.disable_record_mouse_movements()
  human_clicker.move(move_to_position, get_speed_from_pos_to_pos(current_position, move_to_position))
  UserInput.set_mouse_current_position()
  UserInput.enable_record_mouse_movements()


def move_cursor_and_click(image=None, cords=None):
  move_cursor(image, cords)
  sleep(uniform(0.1,0.25))
  pyautogui.click()
  return True

def chance(percent):
  return uniform(0, 100) < percent

def guarantee_wow_focus():
  if not imagesearch(WOW_SYMBOL):
      raise Exception("Wow Application not running")
  if not imagesearch(WOW_FOCUSED, precision=0.93):
    move_cursor_and_click(WOW_SYMBOL)
    move_cursor(cords=(uniform(500, 1500), uniform(200, 800)))

def game_has_dced():
  return bool(imagesearch(DISCONNECTED))

def kill_game_window():
  PROCNAME = "wowclassic"
  for proc in psutil.process_iter():
    if PROCNAME in proc.name().lower():
      logging.info('Killed Wow Application')
      return proc.kill()

def open_wow_launcher():
  move_cursor_and_click(cords=(1920, 1080))
  assure_img_present(WOW_APP)
  move_cursor(WOW_APP)
  doubleClick()

def maximize_window():
  win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MAXIMIZE)
  sleep(1)
  win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MAXIMIZE)

def init_game_window():
  open_wow_launcher()
  assure_img_present(PLAY_BUTTON)
  move_cursor_and_click(PLAY_BUTTON)
  assure_img_present(WOW_SYMBOL)
  sleep(5)
  maximize_window()
  assure_img_present(LOG_CHARACTER)
  sleep(uniform(0.3, 3))
  press('enter')
  sleep(uniform(10, 22))
  logging.info('Inited Wow Application')


def guarantee_game_ready_for_action():
  if not bool(imagesearch(WOW_SYMBOL)):
    kill_game_window()
    init_game_window()
  else:
    guarantee_wow_focus()
    if game_has_dced():
      logging.info('Wow App got disconnected')
      kill_game_window()
      init_game_window()

def take_screenshot():
  return pyautogui.screenshot()

def save_screenshot(screenshot, tag="Exception"):
  screenshot.save(f'exceptions/[{tag}]{datetime.now().replace(microsecond=0)}.png'.replace(':', ';'))

def move_cursor_randomly_during(seconds):
  start_time = time()
  MAX_IDLE_TIMES = [x for x in range(2, 15)]
  while time() - start_time < seconds:
    move_cursor(cords=(uniform(100, 1900), uniform(50, 1000)))
    time_left = seconds - (time() - start_time)
    max_idle_times_available = [max_idle for max_idle in MAX_IDLE_TIMES if max_idle < time_left]
    if not max_idle_times_available:
      break
    sleep(uniform(0.05, choice(max_idle_times_available)))
    if UserInput.has_received_user_input_in_last_minute():
      return
  move_cursor(cords=(uniform(500, 1500), uniform(200, 800)))

def tab_out_and_random_activity(Player):
  alt_tab()
  move_cursor_randomly_during(seconds=Player.get_random_no_action_required_time())
  alt_tab()

@stop_if_user_input
def alt_tab():
  pyautogui.hotkey('alt', 'tab')

def keyDown(key):
  pyautogui.keyDown(key)

def keyUp(key):
  pyautogui.keyUp(key)

def press(key):
  pyautogui.press(key)

def hotkey(*args, **kwargs):
  pyautogui.hotkey(*args, **kwargs)

def doubleClick():
  pyautogui.doubleClick()