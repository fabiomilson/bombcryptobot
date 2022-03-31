import pyautogui
import config
import bot_click
from logger import logger

def go():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_NEW_MAP, confidence=config.TAXA_IMG_NEW_MAP)
        logger('Clicando no new map....')
        bot_click.click(x, y)
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Nao conseguiu clicar no new map: ' + str(e))
        else:
            logger('Nao conseguiu clicar no new map')