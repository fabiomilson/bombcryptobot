import pyautogui
from logger import logger
import config
from cv2 import cv2
import mss
import numpy as np
from random import random
import time
import bot_click

pyautogui.FAILSAFE = False
global hero_clicks
global hero_clicks_home
hero_clicks = 0
hero_clicks_home = 0


def isHeroiCharacterApareceu():
    try:
        x, y = pyautogui.locateCenterOnScreen(config.IMG_CHARACTERS, confidence=config.TAXA_IMG_CHARACTERS)
        logger('Characteres nao apareceu')
        return x, y
    except Exception as e:
        if config.DEBUG_ERROR:
            logger('Characteres nao apareceu: ' + str(e))
        else:
            logger('Characteres nao apareceu')
        return None, None


def go():
    x, y = isHeroiCharacterApareceu()
    if (x is not None):
        y = y + config.OFFSET_LOCAL_CLICK_SCROLL
        for _ in range(5):
            acoesTrabalho()
            acaoMoverClicar(x, y)

        tentaPorHeroisExtraCasa()
        try:
            x, y = pyautogui.locateCenterOnScreen(config.IMG_FECHAR_TELA_HEROIS, confidence=0.6)
            bot_click.click(x, y)
            time.sleep(2)
            bot_click.click(x, y)
        except Exception as e:
            if config.DEBUG_ERROR:
                logger('Nao conseguiu fechar tela de herois: ' + str(e))
            else:
                logger('Nao conseguiu fechar tela de herois')


def acoesTrabalho():
    clickGreenBarButtons()
    time.sleep(2)
    botaPraCasaSeExistir()
    time.sleep(4)


def acaoMoverClicar(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.dragRel(0, -150, duration=1, button='left')
    time.sleep(3)


def botaPraCasaSeExistir():
    if config.CASINHA:
        # ele clicka nos q tao trabaiano mas axo q n importa
        offset = config.OFFSET_LOCAL_BOTAO_HOME

        """epics = positions(cv2.imread(constants.IMG_EPIC_1), threshold=constants.TAXA_IMG_SUPER_HEROES)
        buttons_1 = positions(cv2.imread(constants.IMG_GO_HOME), threshold=constants.TAXA_IMG_GO_HOME)
        logger('epic_1 detectado %d' % len(epics))"""

        fora_da_casa = getHerosCasa()
        buttons_home_super = positions(cv2.imread(config.IMG_GO_HOME), threshold=config.TAXA_IMG_GO_HOME)
        # buttons_green = positions(cv2.imread(constants.IMG_GO_WORK), threshold=constants.TAXA_IMG_GREEN_BAR)
        logger('Supers detectado %d' % len(fora_da_casa))

        # fora_da_casa = []
        """for epic in epics:
            if not isForaCasa(epic, buttons_1):
                fora_da_casa.append(epic)"""

        if len(fora_da_casa) > 0:
            logger('Colocando para casa %d heroes' % len(fora_da_casa))

        hero_clicks_home_cnt = 0
        for (y, x) in fora_da_casa:
            # isWorking(y, buttons)
            w = 60
            h = 20
            #moveToWithRandomness(x+offset+50,y,1)
            try:
                pyautogui.moveTo(x+offset+50, y+20, 2)
                pyautogui.click()
            except Exception as e:
                logger('Deu erro e nao devia: ' + str(e))
            
            global hero_clicks_home
            hero_clicks_home = hero_clicks_home + 1
            hero_clicks_home_cnt = hero_clicks_home_cnt + 1
            if hero_clicks_home_cnt > 20:
                logger('⚠️ Too many hero clicks, try to increase the go_home threshold')
                return
            # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[config.MONITOR_EM_EXECUCAO - 1]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:, :, :3]


def positions(target, threshold=config.TAXA_IMG_GREEN_BAR, img=None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = config.OFFSET_LOCAL_BOTAO_WORK

    green_bars = positions(cv2.imread(config.IMG_GREEN_BAR), threshold=config.TAXA_IMG_GREEN_BAR)
    logger('🟩 %d green bars detected' % len(green_bars))
    buttons = positions(cv2.imread(config.IMG_GO_WORK), threshold=config.TAXA_IMG_GREEN_BAR)
    logger('🆗 %d buttons detected' % len(buttons))

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        logger('👆 Clicking in %d heroes' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    hero_clicks_cnt = 0
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        moveToWithRandomness(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        hero_clicks_cnt = hero_clicks_cnt + 1
        if hero_clicks_cnt > 20:
            logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)


def isWorking(bar, buttons):
    y = bar[1]

    for (_, button_y, _, button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True


def isForaCasa(super, buttons):
    y = super.y

    for (_, button_y, _, button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True


def moveToWithRandomness(x, y, t):
    pyautogui.moveTo(addRandomness(x, 10), addRandomness(y, 10), t + random() / 2)


def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)


def getHerosCasa():
    h, w = 62, 490  # h, w = hero.shape[:-1] # pegar altura e largura
    tela_bomb = printSreen()
    super_hero_01 = cv2.imread('testes/super_hero_01.png')
    super_hero_02 = cv2.imread('testes/super_hero_02.png')
    super_hero_03 = cv2.imread('testes/super_hero_03.png')
    super_hero_04 = cv2.imread('testes/super_hero_04.png')

    rest_mode_output_house = cv2.imread('testes/rest_mode_output_house.png')
    green_bar = cv2.imread('testes/green_bar.png')

    loc_01 = getLoc(tela_bomb, super_hero_01)
    loc_02 = getLoc(tela_bomb, super_hero_02)
    loc_03 = getLoc(tela_bomb, super_hero_03)
    loc_04 = getLoc(tela_bomb, super_hero_04)

    isLoc1AindaNaoFoi = True
    isLoc2AindaNaoFoi = True
    isLoc3AindaNaoFoi = True
    isLoc4AindaNaoFoi = True
    posicoes_herois = []

    for pt in zip(*loc_01[::-1]):
        #cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (93, 0, 255), 2)
        super_hero_01_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w + pt[0]]
        loc_pos_hero = getLoc(super_hero_01_cropped, rest_mode_output_house)
        is_hero_01_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_01_green_bar = getLoc(super_hero_01_cropped, green_bar)[0].size != 0
        if is_hero_01_rest_mode_output_house and isLoc1AindaNaoFoi:
            isLoc1AindaNaoFoi = False
            posicoes_herois.append(loc_01)

    for pt in zip(*loc_02[::-1]):
        #cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (30, 144, 255), 2)
        super_hero_02_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w + pt[0]]
        loc_pos_hero = getLoc(super_hero_02_cropped, rest_mode_output_house)
        is_hero_02_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_02_green_bar = getLoc(super_hero_02_cropped, green_bar)[0].size != 0
        if is_hero_02_rest_mode_output_house and isLoc2AindaNaoFoi:
            isLoc2AindaNaoFoi = False
            posicoes_herois.append(loc_02)

    for pt in zip(*loc_03[::-1]):
        #cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (64, 224, 208), 2)
        super_hero_03_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w + pt[0]]
        loc_pos_hero = getLoc(super_hero_03_cropped, rest_mode_output_house)
        is_hero_03_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_03_green_bar = getLoc(super_hero_03_cropped, green_bar)[0].size != 0
        if is_hero_03_rest_mode_output_house and isLoc3AindaNaoFoi:
            isLoc3AindaNaoFoi = False
            posicoes_herois.append(loc_03)

    for pt in zip(*loc_04[::-1]):
        #cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (255, 0, 255), 2)
        super_hero_04_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w + pt[0]]
        loc_pos_hero = getLoc(super_hero_04_cropped, rest_mode_output_house)
        is_hero_04_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_04_green_bar = getLoc(super_hero_04_cropped, green_bar)[0].size != 0
        if is_hero_04_rest_mode_output_house and isLoc4AindaNaoFoi:
            isLoc4AindaNaoFoi = False
            posicoes_herois.append(loc_04)

    return posicoes_herois


def getLoc(tela_bomb, hero):
    res = cv2.matchTemplate(tela_bomb, hero, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    return loc
# getHerosCasa()


def tentaPorHeroisExtraCasa():
    try:
        offset = 160
        rest_mode_output_house = cv2.imread('testes/rest_mode_output_house.png')
        tela_bomb = printSreen()
        loc_01 = getLoc(tela_bomb, rest_mode_output_house)
        for (x, y) in zip(*loc_01[::-1]):
                # isWorking(y, buttons)
                w = 60
                h = 20
                #moveToWithRandomness(x+offset+50,y,1)
                try:
                    pyautogui.moveTo(x+offset, y+20, 2)
                    pyautogui.click()
                except Exception as e:
                    logger('Deu erro e nao devia: ' + str(e))
                
                # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    except Exception as e:
        print('by pass tentativa herois extra ' + str(e))

tentaPorHeroisExtraCasa()