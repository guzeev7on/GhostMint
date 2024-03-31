import json
import math
from statistics import mean
import time
from web3 import Web3
from eth_abi import encode
import requests
import random
from datetime import datetime
import config
import fun
from fun import log, log_error, save_wallet_to
from ghost import Ghost


# Ошибка ERROR: Ошибка: execution reverted  чаще всего из-за того что данное направление закрыто


current_datetime = datetime.now()
print(f"\n\n {current_datetime}")

keys_list = []
with open("private_keys.txt", "r") as f:
    for row in f:
        private_key=row.strip()
        if private_key:
            keys_list.append(private_key)

random.shuffle(keys_list)
i=0
for private_key in keys_list:
    i+=1
    fun.get_new_prices()
    flag_no_money = 1
    
    ghost = Ghost(private_key)
    wallet = ghost.address

    if random.randint(0, 100) > config.veroyatnost:
        log("skip")
        continue

    if config.proxy_use == 2:
        while True:
            try:
                requests.get(url=config.proxy_changeIPlink)
                fun.timeOut("teh")            
                result = requests.get(url="https://yadreno.com/checkip/", proxies=config.proxies)
                print(f'Ваш новый IP-адрес: {result.text}')
                break
            except Exception as error:
                print(' !!! Не смог подключиться через Proxy, повторяем через 2 минуты... ! Чтобы остановить программу нажмите CTRL+C или закройте терминал')
                time.sleep(120)

    log(f"I-{i}: Начинаю работу с {wallet}")
    skolko_trans = random.randint(config.skolko_trans[0],config.skolko_trans[1])
    for _ in range(skolko_trans):
        random.shuffle(config.networks_from)
        for network_from in config.networks_from:
            log(f"{network_from}:::")
            try:
                ghost.get_contract(network_from)
                balance, balance_decimal, balance_USD = ghost.get_balance()
                if(balance_USD <= config.min_balance):
                    log(f"{network_from}: low balance , меньше {config.min_balance}$")
                    continue                
            except Exception as error:
                fun.log_error(f"Ошибка подключения к RPC {fun.address[network_from]['rpc']}: {error}")
                continue

            try:
                full_fee, full_fee_USD = ghost.get_full_fee_mint()
             
                if(balance < full_fee*config.gas_kef):
                    log("low balance")
                    continue
                flag_no_money = 0 # флаг снимается потому что найден марш для котрого хватает денег
                if(config.max_komissia < full_fee_USD):
                    log(f"скипаю такую высокую комиссию $ = {full_fee_USD}")
                    continue
                log(f"полные затраты в $ = {full_fee_USD}")
                
                # Подписываем и отправляем транзакцию
                
                if ghost.mint():
                    # fun.log_ok(f'MINT OK: {fun.address[network_from]["scan"]}/{tx_hash}')
                    skolko_trans = skolko_trans - 1
                else:
                    fun.timeOut("teh") 
                    # fun.log_error(f'MINT false: {fun.address[network_from]["scan"]}/{tx_hash}')
                fun.timeOut("teh") 

                # уровень перебора сетей
                if skolko_trans <= 0:
                    break
            except Exception as error:
                fun.log_error(f"Ошибка: {error}")
        # уровень перебора количества транзакций
        if skolko_trans <= 0:
            break
        if(flag_no_money):
            break
  

    # уровень приватников
    if(flag_no_money):
        log_error("Не достаточно нативки на кошельке")
        # save_wallet_to("no_money", private_key)
        save_wallet_to("no_money_aw", wallet)
        fun.timeOut("teh")  
        continue


    log("pausa")
    fun.timeOut() 
    
log("Завершение работы")