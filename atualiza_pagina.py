import keyboard
import time
import voltar_mapa

def go():
    voltar_mapa.go()
    time.sleep(12)
    keyboard.press_and_release('ctrl + shift + r, \n')
    time.sleep(2)
    keyboard.press_and_release('ctrl + f5, \n')