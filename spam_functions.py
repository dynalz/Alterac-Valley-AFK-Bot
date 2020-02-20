import logging
import pyautogui
from time import sleep
from random import uniform
from constants import *
from utils.__utils__ import *

def in_queue_or_av():
  return bool(imagesearch(HORDE_QUEUE_SYMBOL))
  return bool(imagesearch(HORDE_QUEUE_SYMBOL)) or bool(imagesearch(HORDE_QUEUE_SYMBOL1))

def can_queue_in_av():
  return not bool(imagesearch(DESERTER_DEBUFF))

def av_queue_popped():
  return bool(imagesearch(QUEUE_POP))

def av_finished():
  return bool(imagesearch(LEAVE_BG))

def can_av_recall():
  return bool(imagesearch(AV_RECALL))

def av_recall():
  move_cursor_and_click(AV_RECALL)
  move_cursor(cords=(uniform(500, 1500), uniform(200, 800)))
  sleep(uniform(11,13))

def enter_av():
  move_cursor_and_click(QUEUE_POP)

def leave_av():
  move_cursor_and_click(LEAVE_BG)

def log_out():
  tries = 0
  while True:
    pyautogui.press('esc')
    sleep(uniform(0.1, 0.4))
    if bool(imagesearch(LOG_OUT)):
      break
    tries += 1
    if tries >= 5:
      logging.info("Failed logging OUT - Esc did not bring Logout button")
      save_screenshot(take_screenshot(), tag="LogOutFail")
      return False
  move_cursor_and_click(LOG_OUT)
  
def align_av_door():
  pyautogui.keyDown('a')
  pyautogui.keyDown('w')
  pyautogui.keyDown('left')
  sleep(uniform(0.06, 0.08))
  pyautogui.keyUp('left')
  sleep(uniform(1,1.5))
  pyautogui.keyUp('a')
  pyautogui.keyUp('w')

@timeout(10)
def queue_av():
  sleep(uniform(0,1.2))
  pyautogui.press('f1')
  sleep(uniform(0,1.2))
  pyautogui.press('i')
  sleep(uniform(0,1.2))
  assure_img_present(AV_QUEUE1)
  move_cursor_and_click(AV_QUEUE1)
  sleep(uniform(0,1.2))
  assure_img_present(AV_QUEUE2)
  return move_cursor_and_click(AV_QUEUE2)


def av_setup(Player):
  sleep(uniform(55, 65))
  align_av_door()
  Player.autorun()
  Player.stealth()
  Player.toggle_slow_walk()
  sleep(uniform(55, 65))
  Player.toggle_slow_walk()



"""
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

print(pytesseract.image_to_string(cv2.imread('gg.png')))


"""
