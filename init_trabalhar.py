import chest
import bot_click
import config
from logger import logger
import keyboard
import time
import pyautogui
from datetime import datetime
import random
import globals

global primeiro_work
primeiro_work = True

global data_ultimo_work
data_ultimo_work = datetime.now()

global etapas
etapas = {}

global etapa_atual
etapa_atual = 'clicar_setinha_pra_cima'

def getEtapaAtual():
    global etapa_atual
    return etapa_atual

def setEtapaAtual(value):
    global etapa_atual
    etapa_atual = value

def getEtapas():
    global etapas
    return etapas

def getDataUltimoWork():
    global data_ultimo_work
    return data_ultimo_work

def setDataUltimoWork():
    global data_ultimo_work
    data_ultimo_work = datetime.now()

def jaPassouEntre5e10Minutos():
    if config.DEBUG == True:
        return True
    
    minutagem_selecionada = 1 # default
    if config.MINUTO_ESPERA_MINIMO_INICIAR_TRABALHO == config.MAXIMO_ESPERA_MINIMO_INICIAR_TRABALHO:
        minutagem_selecionada = config.MINUTO_ESPERA_MINIMO_INICIAR_TRABALHO
    else:
        minutagem_selecionada = random.randrange(config.MINUTO_ESPERA_MINIMO_INICIAR_TRABALHO, config.MAXIMO_ESPERA_MINIMO_INICIAR_TRABALHO) * 60
    
    data_atual = datetime.now()
    data_ultimo_trabalhar = getDataUltimoWork()
    resultado_diff = data_atual - data_ultimo_trabalhar
    if resultado_diff.seconds > minutagem_selecionada:
        logger('[Work] Ja passou entre ' + str(config.MINUTO_ESPERA_MINIMO_INICIAR_TRABALHO) + ' e ' + str(config.MAXIMO_ESPERA_MINIMO_INICIAR_TRABALHO) + ' minutos.... minuto selecionado' + str(minutagem_selecionada) + ' diff: ' + str(resultado_diff.seconds / 60))
        return True
    else:
        logger('[Work] Ainda nao passou minutagem para TRABALHAR... ultimo trabalhar em: ' + str(data_ultimo_trabalhar) + ' minutagem selecionada: ' + str(minutagem_selecionada / 60))
        return False

def isHeroiWorkApareceu():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_BOTAO_HEROES, confidence=config.TAXA_IMG_BOTAO_HEROES)
        logger('Botao heroes apareceu')
        return True
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Botao heroes nao apareceu: ' + str(e))
        else: 
            logger('Botao heroes nao apareceu')
        return False

def clicarSetinhaPraCima():
    try:
        x, y = chest.posicaoWorkJob()
        logger('Clicando na setinha pra cima....')
        bot_click.click(x, y)
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Não conseguiu clicar na setinha pra cima: ' + str(e))
        else:
            logger('Não conseguiu clicar na setinha pra cima')

def clicarHeroes():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_BOTAO_HEROES, confidence=config.TAXA_IMG_BOTAO_HEROES)
        logger('Clicando no heroes para trabalhar....')
        bot_click.click(x, y)
        global primeiro_work
        primeiro_work = False
        setDataUltimoWork()
        setEtapas()
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Não conseguiu clicar no heroes para trabalhar: ' + str(e))
        else:
            logger('Não conseguiu clicar no heroes para trabalhar')

def setEtapas():
    setEtapaAtual('clicar_setinha_pra_cima')
    etapas['clicar_setinha_pra_cima'] = {"timeout": 0, "acao": clicarSetinhaPraCima}
    etapas['click_heroes'] = {"timeout": 0, "acao": clicarHeroes}

setEtapas() # inicializa etapas

def go():
    try: 
        global primeiro_work
        if primeiro_work == False:
            if(jaPassouEntre5e10Minutos() == False):
                return

        x, y = chest.posicaoWorkJob()
        logger("Colocando para trabalhar....")
        etapas = getEtapas()
        etapa_atual = getEtapaAtual()
        etapa = etapas[etapa_atual]
        if(etapa['timeout'] >= config.MAXIMO_TENTATIVAS_COMECAR_TRABALHAR):
            logger('Fudeu.... nao esta sendo possivel colocar para trabalhar')    
            #keyboard.press_and_release('ctrl + shift + r, \n')
            etapa['timeout'] = 0
            setEtapas()
        logger("Executando a etapa (trabalho): " + str(etapa))
        etapa['timeout'] = etapa['timeout'] + 1
        etapa['acao']()
        time.sleep(1)
        if(isHeroiWorkApareceu()):
            globals.setPrimeiroLogin(False)
            etapa['timeout'] = 0
            setEtapaAtual('click_heroes')            
        
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Não conseguiu por para trabalhar: ' + str(e))
        else:
            logger('Não conseguiu por para trabalhar')