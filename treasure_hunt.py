import config
import pyautogui
from logger import logger
import bot_click

def isTelaTreasureHunt():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_TREASURE_HUNT, confidence=config.TAXA_IMG_TREASURE_HUNT)
        logger('Tela de com treasure hunt localizada')
        return x, y
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Tela de com treasure hunt nao localizada: ' + str(e))
        else:
            logger('Tela de com treasure hunt nao localizada')
        return None, None

def tentaClickar():
    x, y = isTelaTreasureHunt()
    if(x is not None):
        logger('Tentando clickar em treasure hunt....')
        bot_click.click(x, y)