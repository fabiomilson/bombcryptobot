import config
import pyautogui
import bot_click
import treasure_hunt
from logger import logger

# alterar aqui
offset_x = 373
offset_y = 557

def isTelaComChest():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_CHEST, confidence=config.TAXA_IMG_CHEST)
        logger('Tela com chest localizada')
        return x, y
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Tela com chest nao localizada: ' + str(e))
        else:
            logger('Tela com chest nao localizada')
        return None, None

def posicaoWorkJob():
    x_treasure, y_treasure = treasure_hunt.isTelaTreasureHunt()
    x, y = isTelaComChest()
    if(x is not None and x_treasure is None):
        try:
            x = x - offset_x
            y = y + offset_y
            return x, y
        except Exception as e:
            if config.DEBUG_ERROR:
                logger('Tela com chest nao localizada: ' + str(e))
            else:
                logger('Tela com chest nao localizada')