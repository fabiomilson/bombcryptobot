import keyboard
import pyautogui
import numpy as np
import pyautogui
import imutils
import cv2

print('press s para pegar mouse position')


def testeRezise():
    # take a screenshot of the screen and store it in memory, then
    # convert the PIL/Pillow image to an OpenCV compatible NumPy array
    # and finally write the image to disk
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("in_memory_to_disk.png", image)
    image = cv2.imread("in_memory_to_disk.png")
    cv2.imshow("Screenshot", imutils.resize(image, width=600))
    cv2.waitKey(0)


def testeSearch():
    h, w = 62, 490  # h, w = hero.shape[:-1] # pegar altura e largura
    tela_bomb = cv2.imread('testes/tela_teste_dois_vamp.png')
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

    is_hero_01_rest_mode_output_house = False
    is_hero_02_rest_mode_output_house = False
    is_hero_03_rest_mode_output_house = False
    is_hero_04_rest_mode_output_house = False

    is_hero_01_green_bar = False
    is_hero_02_green_bar = False
    is_hero_03_green_bar = False
    is_hero_04_green_bar = False

    posicoes_herois = []

    for pt in zip(*loc_01[::-1]):
        cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (93, 0, 255), 2)
        super_hero_01_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w+pt[0]]
        loc_pos_hero = getLoc(super_hero_01_cropped, rest_mode_output_house)
        is_hero_01_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_01_green_bar = getLoc(super_hero_01_cropped, green_bar)[0].size != 0
        if is_hero_01_rest_mode_output_house:
            posicoes_herois.append(loc_pos_hero)

    for pt in zip(*loc_02[::-1]):
        cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (30, 144, 255), 2)
        super_hero_02_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w+pt[0]]
        loc_pos_hero = getLoc(super_hero_02_cropped, rest_mode_output_house)
        is_hero_02_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_02_green_bar = getLoc(super_hero_02_cropped, green_bar)[0].size != 0
        if is_hero_02_rest_mode_output_house:
            posicoes_herois.append(loc_pos_hero)

    for pt in zip(*loc_03[::-1]):
        cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (64, 224, 208), 2)
        super_hero_03_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w+pt[0]]
        loc_pos_hero = getLoc(super_hero_03_cropped, rest_mode_output_house)
        is_hero_03_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_03_green_bar = getLoc(super_hero_03_cropped, green_bar)[0].size != 0
        if is_hero_03_rest_mode_output_house:
            posicoes_herois.append(loc_pos_hero)

    for pt in zip(*loc_04[::-1]):
        cv2.rectangle(tela_bomb, pt, (pt[0] + w, pt[1] + h), (255,0,255), 2)
        super_hero_04_cropped = tela_bomb[pt[1]: h + pt[1], pt[0]: w+pt[0]]
        loc_pos_hero = getLoc(super_hero_04_cropped, rest_mode_output_house)
        is_hero_04_rest_mode_output_house = loc_pos_hero[0].size != 0
        is_hero_04_green_bar = getLoc(super_hero_04_cropped, green_bar)[0].size != 0
        if is_hero_04_rest_mode_output_house:
            posicoes_herois.append(loc_pos_hero)

    cv2.imwrite('testes/res.png', tela_bomb)
    print(is_hero_01_rest_mode_output_house, is_hero_02_rest_mode_output_house, is_hero_03_rest_mode_output_house, is_hero_04_rest_mode_output_house)
    print(is_hero_01_green_bar, is_hero_02_green_bar, is_hero_03_green_bar, is_hero_04_green_bar)
    for t in posicoes_herois:
        x, y = t
        print(x, y)


def getLoc(tela_bomb, hero):
    res = cv2.matchTemplate(tela_bomb, hero, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    return loc


# testeRezise()
testeSearch()


def mousePosition():
    while True:
        pos = pyautogui.position()
        if keyboard.is_pressed('s'):
            a = pyautogui.screenshot(region=(pos.x, pos.y, 150, 100))
            print(pos)


def getColor():
    while True:
        posXY = pyautogui.position()
        print(posXY, pyautogui.pixel(posXY[0], posXY[1]))
        if posXY[0] == 0:
            break


def checkHero():
    pos_sp_hero_amarelo = None
    pos_sp_hero_vampiro_vermelho = None
    pos_sp_hero_vampiro_amarelo = None
    pos_epic_hero_vampiro = None
    pos_sp_hero_amarelo_borda_verde = None
    pos_sp_hero_vampiro_vermelho_borda_verde = None
    pos_sp_hero_vampiro_amarelo_borda_verde = None
    pos_epic_hero_vampiro_borda_verde = None

    try:
        pos_sp_hero_amarelo = pyautogui.locateCenterOnScreen('imgs/sp_hero_amarelo.png')
    except:
        print('achou hero para casa nao ' + 'pos_sp_hero_amarelo')
    try:
        pos_sp_hero_vampiro_vermelho = pyautogui.locateCenterOnScreen('imgs/sp_hero_vampiro_vermelho.png')
    except:
        print('achou hero para casa nao ' + 'pos_sp_hero_vampiro_vermelho')
    try:
        pos_sp_hero_vampiro_amarelo = pyautogui.locateCenterOnScreen('imgs/sp_hero_vampiro_amarelo.png')
    except:
        print('achou hero para casa nao ' + 'pos_sp_hero_vampiro_amarelo')
    try:
        pos_epic_hero_vampiro = pyautogui.locateCenterOnScreen('imgs/epic_hero_vampiro.png')
    except:
        print('achou hero para casa nao ' + 'pos_epic_hero_vampiro')

    try:
        pos_sp_hero_amarelo_borda_verde = pyautogui.locateCenterOnScreen('imgs/sp_hero_amarelo_borda_verde.png')
    except:
        print('achou hero para casa nao ' + 'pos_sp_hero_amarelo_borda_verde')
    try:
        pos_sp_hero_vampiro_vermelho_borda_verde = pyautogui.locateCenterOnScreen(
            'imgs/sp_hero_vampiro_vermelho_borda_verde.png')
    except:
        print('achou hero para casa nao ' + 'pos_sp_hero_vampiro_vermelho_borda_verde')
    try:
        pos_sp_hero_vampiro_amarelo_borda_verde = pyautogui.locateCenterOnScreen(
            'imgs/sp_hero_vampiro_amarelo_borda_verde.png')
    except:
        print('achou hero para casa nao ' + 'pos_sp_hero_vampiro_amarelo_borda_verde')
    try:
        pos_epic_hero_vampiro_borda_verde = pyautogui.locateCenterOnScreen('imgs/epic_hero_vampiro_borda_verde.png')
    except:
        print('achou hero para casa nao ' + 'pos_epic_hero_vampiro_borda_verde')

    pos_hero_para_casa = []
    if pos_sp_hero_amarelo is not None:
        pos_hero_para_casa.append(pos_sp_hero_amarelo)
    elif pos_sp_hero_amarelo_borda_verde is not None:
        pos_hero_para_casa.append(pos_sp_hero_amarelo_borda_verde)

    if pos_sp_hero_vampiro_vermelho is not None:
        pos_hero_para_casa.append(pos_sp_hero_vampiro_vermelho)
    elif pos_sp_hero_vampiro_vermelho_borda_verde is not None:
        pos_hero_para_casa.append(pos_sp_hero_vampiro_vermelho_borda_verde)

    if pos_sp_hero_vampiro_amarelo is not None:
        pos_hero_para_casa.append(pos_sp_hero_vampiro_amarelo)
    elif pos_sp_hero_vampiro_amarelo_borda_verde is not None:
        pos_hero_para_casa.append(pos_sp_hero_vampiro_amarelo_borda_verde)

    if pos_epic_hero_vampiro is not None:
        pos_hero_para_casa.append(pos_epic_hero_vampiro)
    elif pos_epic_hero_vampiro_borda_verde is not None:
        pos_hero_para_casa.append(pos_epic_hero_vampiro_borda_verde)

    print(pos_hero_para_casa)

# mousePosition()
# checkHero()
