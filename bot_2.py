import time
import schedule
import os

from logger import logger

# telas
import tela_login
import treasure_hunt
import botao_ok
import init_trabalhar
import trabalhar
import voltar_mapa
import new_map
import atualiza_pagina

try:
    schedule.every(2).seconds.do(tela_login.tentaLogar)
    schedule.every(2).seconds.do(treasure_hunt.tentaClickar)
    schedule.every(2).seconds.do(botao_ok.tentaClickar)
    schedule.every(2).seconds.do(init_trabalhar.go)
    schedule.every(2).seconds.do(trabalhar.go)
    schedule.every(2).seconds.do(new_map.go)
    schedule.every(3).minutes.do(voltar_mapa.go)
    #schedule.every(30).minutes.do(atualiza_pagina.go)
    # schedule.every(2).seconds.do(trabalhar.botaPraCasaSeExistir)
except Exception as e:
    print("Error: unable to start thread - " + str(e))

while True:
    print('ping')
    schedule.run_pending()
    time.sleep(5)
