import pyautogui
from logger import logger
import config
import bot_click
import random
from datetime import datetime
import keyboard
import time
import globals

global etapas
etapas = {}

global etapa_atual
etapa_atual = 'click_connect_wallet'

global data_ultimo_login
data_ultimo_login = datetime.now()

def getEtapaAtual():
    global etapa_atual
    return etapa_atual

def setEtapaAtual(value):
    global etapa_atual
    etapa_atual = value

def getEtapas():
    global etapas
    return etapas

def getDataUltimoLogin():
    global data_ultimo_login
    return data_ultimo_login

def setDataUltimoLogin():
    global data_ultimo_login
    data_ultimo_login = datetime.now()

def isTelaLogin():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_CONNECT_WALLET, confidence=config.TAXA_IMG_CONNECT_WALLET)
        logger('Tela de login localizada')
        return True
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Tela de login nao localizada: ' + str(e))
        else:
            logger('Tela de login nao localizada')
        return False

def isAssinaturaApareceu():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_BOTAO_ASSINAR, confidence=config.TAXA_IMG_BOTAO_ASSINAR) # localiza metamask
        logger('Tela de assinatura apareceu')
        return True
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Tela de nao assinatura apareceu: ' + str(e))
        else: 
            logger('Tela de nao assinatura apareceu')
        return False

def isTelaUsuarioSenhaApareceu():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_CONNECT_WALLET_USUARIO_SENHA, confidence=config.TAXA_IMG_BOTAO_ASSINAR) # localiza metamask
        logger('Tela de USUARIO E SENHA apareceu')
        return True
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Tela de USUARIO E SENHA nao apareceu: ' + str(e))
        else: 
            logger('Tela de USUARIO E SENHA nao apareceu')
        return False

def clicarBotaoConnectWallet():
    x, y = pyautogui.locateCenterOnScreen(config.IMG_CONNECT_WALLET, confidence=config.TAXA_IMG_CONNECT_WALLET) # para click no botao
    logger('Tentando logar....')
    bot_click.click(x, y)

def clicarBotaoConnectWalletUsuarioSenha():
    x, y = pyautogui.locateCenterOnScreen(config.IMG_CONNECT_WALLET_USUARIO_SENHA, confidence=config.TAXA_IMG_CONNECT_WALLET) # para click no botao
    logger('Tentando logar wallet usuario senha....')
    bot_click.click(x, y)

def clicarBotaoAssinar():
    x, y = pyautogui.locateCenterOnScreen(config.IMG_BOTAO_ASSINAR, confidence=config.TAXA_IMG_BOTAO_ASSINAR) # localiza metamask
    bot_click.click(x, y)
    globals.setPrimeiroLogin(False)
    setDataUltimoLogin()
    setEtapas()

def setEtapas():
    setEtapaAtual('click_connect_wallet')
    etapas['click_connect_wallet'] = {"timeout": 0, "acao": clicarBotaoConnectWallet}
    etapas['click_connect_wallet_usuario_senha'] = {"timeout": 0, "acao": clicarBotaoConnectWalletUsuarioSenha}
    etapas['click_botao_assinar'] = {"timeout": 0, "acao": clicarBotaoAssinar}

setEtapas() #inicializa etapas

def jaPassouMinutagem():
    if config.DEBUG == True:
        return True
    minutagem_selecionada = random.randrange(config.MINUTO_ESPERA_MINIMO_PARA_LOGIN, config.MINUTO_ESPERA_MAXIMO_PARA_LOGIN) * 60
    data_atual = datetime.now()
    data_ultimo_login = getDataUltimoLogin()
    resultado_diff = data_atual - data_ultimo_login
    if resultado_diff.seconds > minutagem_selecionada:
        logger('Ja passou entre ' + str(config.MINUTO_ESPERA_MINIMO_PARA_LOGIN) + ' e ' + str(config.MINUTO_ESPERA_MAXIMO_PARA_LOGIN) + ' minutos.... minuto selecionado' + str(minutagem_selecionada / 60) + ' diff: ' + str(resultado_diff.seconds / 60))
        return True
    else:
        logger('Ainda nao passou minutagem para LOGIN... ultimo login em: ' + str(data_ultimo_login) + ' minutagem selecionada: ' + str(minutagem_selecionada / 60))
        return False


def tentaLogar():
    try:
        etapa_atual = getEtapaAtual()
        isPrimeiroLogin = globals.getPrimeiroLogin()
        if((isTelaLogin() and jaPassouMinutagem()) or isPrimeiroLogin or (etapa_atual == 'click_botao_assinar')):
            logger("Obtendo etapa....")
            etapas = getEtapas()
            etapa = etapas[etapa_atual]
            if(etapa['timeout'] >= config.MAXIMO_TENTATIVAS_LOGIN):
                logger('Fudeu.... nao esta sendo possivel logar')    
                keyboard.press_and_release('ctrl + shift + r, \n')
                etapa['timeout'] = 0
                setEtapas()
            
            logger("Executando a etapa (login): " + str(etapa))
            etapa['timeout'] = etapa['timeout'] + 1
            etapa['acao']()
            time.sleep(3)
            if(isTelaUsuarioSenhaApareceu()):
                etapa['timeout'] = 0
                setEtapaAtual('click_connect_wallet_usuario_senha')
                tentaLogar()
            time.sleep(8)
            if(isAssinaturaApareceu()):
                etapa['timeout'] = 0
                setEtapaAtual('click_botao_assinar')
                tentaLogar()

    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Tela de login nao localizada: ' + str(e))
        else:
            logger('Tela de login nao localizada')
