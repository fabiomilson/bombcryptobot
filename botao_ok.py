import config
import pyautogui
from logger import logger
import bot_click

def isBotaOk():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_BOTAO_OK)
        logger('Tela de botao ok localizado')
        return True
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Tela de botao ok nao localizado: ' + str(e))
        else:
            logger('Tela de botao ok nao localizado')
        return False

def tentaClickar():
    if(isBotaOk()):
        try:
            x, y = pyautogui.locateCenterOnScreen(config.IMG_BOTAO_OK)
            logger('Tentando clickar em ok....')
            bot_click.click(x, y)
        except Exception as e:
            if config.DEBUG_ERROR:
                logger('Tela de botao ok nao localizado: ' + str(e))
            else:
                logger('Tela de botao ok nao localizado')
            return False