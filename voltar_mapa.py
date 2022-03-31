import pyautogui
import config
import bot_click
from logger import logger

def go():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_BOTAO_VOLTAR, confidence=config.TAXA_IMG_BOTAO_VOLTAR)
        logger('Resetando mapa....')
        bot_click.click(x, y)
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Nao conseguiu resetar mapa: ' + str(e))
        else:
            logger('Nao conseguiu resetar mapa')