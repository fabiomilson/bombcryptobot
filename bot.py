import pyautogui
from pynput import keyboard
import sys
import time
import _thread
import threading 
import random
import schedule
import win32api
import win32con



debug = True
global trabalhar_normais
trabalhar_normais = False


def native_click(x, y, w,  h):
	x = int(x + w/2)
	y = int(y + h/2)
    	
	win32api.SetCursorPos((x, y))
	time.sleep(1)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
	time.sleep(1)

def click(img, threadName, delay, locked=False, nextFunction = None, img_callBack = None):
	if locked:
		return
	while True:
		try:
			print(threadName)
			time.sleep(delay)
			x, y = pyautogui.locateCenterOnScreen(img, confidence=0.6)
			pyautogui.moveTo(x, y)
			#time.sleep(1)
			pyautogui.click()
			time.sleep(1)
			pyautogui.moveTo(1713, 464)
			pyautogui.click()
			if nextFunction != None: 
				nextFunction(img_callBack, threadName, delay)
		except Exception as e:
			if debug:
				print(img + ' ' + str(e))

def analisar_trabalhadores_parados():
	#print_tela = pyautogui.screenshot('teste.png', region=(1481, 313, 955, 537))
	heroes_dormindo = list(pyautogui.locateAllOnScreen(
		'balao.png', confidence=0.6, region=(1481, 313, 955, 537)))
	
	for pos in heroes_dormindo:
		pyautogui.screenshot('teste'+str(pos.left)+'.png', region=(
			pos.left, pos.top, pos.width, pos.height))
		#time.sleep(1)
	print('testando ' + str(len(heroes_dormindo)))
	bla = globals()
	if len(heroes_dormindo) >= 12 and not globals()['trabalhar_normais']:
		globals()['trabalhar_normais'] = True

def bota_pra_trabalhar():
	if True:
		click('botao_voltar.png', 'Thread-Botando-Pra-Trabalhar-Voltar', 2)
		click('botao_heroes.png', 'Thread-Botando-Pra-Trabalhar-Heroes', 2)
		time.sleep(3)
		posicoes_go_work = list(pyautogui.locateAllOnScreen(
                    'go_work.png', confidence=0.9, region=(1481, 313, 955, 537)))

		for pos in posicoes_go_work:
			native_click(pos.left, pos.top, pos.width, pos.height)
			time.sleep(2)
		
		globals()['trabalhar_normais'] = False
		
		print('terminou')
		
		
		

def click_meta_mask_tab_open(threadName, delay):
	while True:
		try:
			x, y = pyautogui.locateCenterOnScreen('tab_meta_mask_open.png')
			#print('ei' ,x, y)
			#pyautogui.moveTo(x, y - 15)
			#pyautogui.click(x, y - 15)
			pyautogui.click(x, y - 15, clicks=2)
			click_bota_assinar(threadName, delay)
		except Exception as e:
			print('não achou tab open meta mask > ' + str(e))

def click_fechar_overloaded(img_callBack, threadName, delay):
	while True:
		try:
			print(threadName)
			time.sleep(delay)
			x, y = pyautogui.locateCenterOnScreen(img_callBack)
			#print('ei' ,x, y)
			#pyautogui.moveTo(x, y - 15)
			#pyautogui.click(x, y - 15)
			pyautogui.moveTo(x, y)
			time.sleep(1)
			pyautogui.click()
		except Exception as e:
			if debug:
				print('não achou click_fechar_overloaded > ' + str(e))

# Create two threads as follows
#try:
	#schedule.every(1).seconds.do(analisar_trabalhadores_parados)
	#schedule.every(10).seconds.do(bota_pra_trabalhar)
#except:
	#print("Error: unable to start thread")

try:
   # login
	login_locked = True
	#bota_pra_trabalhar()
   #analisar_trabalhadores_parados()
   #schedule.every(1).seconds.do(analisar_trabalhadores_parados)
   #schedule.every(10).seconds.do(bota_pra_trabalhar)
	_thread.start_new_thread( click, ('server_overloaded.png', 'Thread-1', random.randint(2, 5), login_locked))
	_thread.start_new_thread( click, ('ok_server_overloaded.png', 'Thread-2', random.randint(2, 5), login_locked))
   #_thread.start_new_thread( click, ('connect_wallet.png', 'Thread-3', random.randint(2, 5), login_locked))
   #_thread.start_new_thread( click, ('meta_mask.png', 'Thread-4', random.randint(2, 5), login_locked))
   #_thread.start_new_thread( click, ('botao_assinar.png', 'Thread-5', random.randint(2, 5), login_locked))
   
   #botar pra trabalhar
   #print(pyautogui.position())
   #_thread.start_new_thread( click, ('botao_voltar_mapa.png', 'Thread-6', random.randint(2, 5)) )
   #_thread.start_new_thread( click, ('botao_voltar_mapa.png', 'Thread-6', random.randint(2, 5)) )

   #new map
	_thread.start_new_thread( click, ('botao_new_map.png', 'Thread-7', 8) )
	_thread.start_new_thread( click, ('server_overloaded_in_game.png', 'Thread-8', 4, False, click_fechar_overloaded, 'botao_fechar_overloaded.png') )
except:
   print("Error: unable to start thread")

#im = pyautogui.screenshot('botao_voltar.png', region=(1492, 255, 55, 45))
#im = pyautogui.screenshot('botao_heroes.png', region=(2342, 737, 69, 107))
#while True:
   # schedule.run_pending()
   # time.sleep(1)


while True:
	print('ping')
	time.sleep(5)
	#print(pyautogui.position())
	#print(pyautogui.displayMousePosition())
	#print(pyautogui.locateOnScreen('botao_voltar.png'))
	#print(pyautogui.locateOnScreen('botao_heroes.png', confidence=0.3))
#hello('botao_play.png')
#hello('botao_heroes.png')
#hello('botao_go_work.png')
# class MyException(Exception): pass

# def on_press(key):
    # if key == keyboard.Key.esc:
        # sys.exit()

# Collect events until released
# listener = keyboard.Listener(
    # on_press=on_press)
# listener.start()
# distance = 200
# while distance > 0:
	# pyautogui.drag(distance, 0, duration=0.5)   # move right
	# distance -= 5
	# pyautogui.drag(0, distance, duration=0.5)   # move down
	# pyautogui.drag(-distance, 0, duration=0.5)  # move left
	# distance -= 5
	# pyautogui.drag(0, -distance, duration=0.5)  # move up