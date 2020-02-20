IMG_SUBFOLDER = "./imgs/"
PNG = ".png"

def build_img_ext(file_name):
  return IMG_SUBFOLDER + file_name + PNG


WOW_APP = build_img_ext("wow_app")
LOG_OUT  = build_img_ext("log_out")
WOW_SYMBOL = build_img_ext("wow_symbol")
PLAY_BUTTON  = build_img_ext("play_button")
DISCONNECTED = build_img_ext("disconnected")
LOG_CHARACTER  = build_img_ext("log_character")
WOW_FOCUSED = build_img_ext("wow_symbol_focused")
WOW_NOT_FOCUSED = build_img_ext("wow_symbol_not_focused")

HORDE_QUEUE_SYMBOL = build_img_ext("horde_queue_symbol")
HORDE_QUEUE_SYMBOL1 = build_img_ext("horde_queue_symbol1")
QUEUE_POP = build_img_ext("queue_pop")
LEAVE_BG  = build_img_ext("leave_bg")
AV_QUEUE1 = build_img_ext("av_queue1")
AV_QUEUE2 = build_img_ext("av_queue2")
AV_RECALL  = build_img_ext("av_recall")
DESERTER_DEBUFF  = build_img_ext("deserter_debuff")




LOGOUT_BETWEEN_HOURS = (2, 9)
