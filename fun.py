import json
import os
from datetime import datetime
import random
from statistics import mean
import time
import requests
from web3 import Web3
import config
from urllib.parse import quote



# option bsc / avax / fantom / polygon / arbitrum / optimism
address = {
    'polygon': {
        'type': 2,
        'chainId': 137,
        'rpc': config.rpc_links['polygon'],
        "scan": "https://polygonscan.com/tx",
        'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
        'MATIC': 'native',
        'native': 'MATIC',
        'WMATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
        'lzChainId': 109,
        'ghost_contract': '0x03e9044d7e8da61815ebed0a5b265fbc9cbdfa4f',        

    },
    'arbitrum': {
        'type': 2,
        'rpc': config.rpc_links['arbitrum'],
        "scan": "https://arbiscan.io/tx",
        'USDC': '0xff970a61a04b1ca14834a43f5de4533ebddb5cc8',
        'USDT': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
        'ETH': 'native',
        'native': 'ETH',
        'WETH': '0x82af49447d8a07e3bd95bd0d56f35241523fbab1',
        'lzChainId': 110,
        'ghost_contract': '0x03f18BfE1413b2bcF94b7C4D41DDFE3e5e49822d',

    },
    'optimism': {
        'type': 2,
        'rpc': config.rpc_links['optimism'],
        "scan": "https://optimistic.etherscan.io/tx",
        'USDC': '0x7f5c764cbc14f9669b88837ca1490cca17c31607',
        'ETH': 'native',
        'native': 'ETH',
        'WETH': '0x4200000000000000000000000000000000000006',
        'lzChainId': 111,
        'ghost_contract': '0xDAb290F956DA2486F188f6F98a34c8bB319bff0C',

    },
    'bsc': {
        'type': 0,
        'chainId': 56,
        'rpc': config.rpc_links['bsc'],
        "scan": "https://bscscan.com/tx",
        'USDT': '0x55d398326f99059ff775485246999027b3197955',
        'BUSD': '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56',
        'BNB': 'native',
        'native': 'BNB',
        'WBNB': '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',
        'lzChainId': 102,
        'ghost_contract': '0x03e9044d7e8da61815ebed0a5b265fbc9cbdfa4f',

    },
    'fantom': {
        'type': 2,
        'rpc': config.rpc_links['fantom'],
        'USDC': '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75',
        'FTM': 'native',
        'native': 'FTM',
        'WFTM': '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',
        'lzChainId': 112,
        'ghost_contract': '0xF56605276cefffe32DFD8B6bF80B93c2A6840136',

    },
    'avax': {
        'type': 2,        
        'rpc': config.rpc_links['avax'],
        'USDC': '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        'USDT': '0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7',
        'AVAX': 'native',
        'native': 'AVAX',
        'WAVAX': '0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7',
        'lzChainId': 106,
        'ghost_contract': '0x5C9BBE51F7F19f8c77DF7a3ADa35aB434aAA86c5',

    },
    'aptos': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 108,
        'ghost_contract': '',

    },
    'dfk': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 115,
        'ghost_contract': '',

    },
    'harmony': {
        'type': 2,        
        'rpc': 'https://api.harmony.one',
        'ONE': 'native',
        'native': 'ONE',         
        'lzChainId': 116,
        'ghost_contract': '0x671861008497782F7108D908D4dF18eBf9598b82',

    },
    'dexalot': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 118,
        'ghost_contract': '',

    },
    'celo': {
        'type': 0,        
        'rpc': 'https://rpc.ankr.com/celo',
        'CELO': 'native',
        'native': 'CELO',          
        'lzChainId': 125,
        'ghost_contract': '0xC20A842e1Fc2681920C1A190552A2f13C46e7fCF',

    },
    'moonbeam': {
        'type': 2,        
        'rpc': 'https://rpc.api.moonbeam.network',
        'GLMR': 'native',
        'native': 'GLMR',          
        'lzChainId': 126,
        'ghost_contract': '0x671861008497782F7108D908D4dF18eBf9598b82',

    },
    'fuse': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 138,
        'ghost_contract': '',

    },
    'gnosis': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 145,
        'ghost_contract': '',

    },
    'klaytn': {
        'type': 2,        
        'rpc': 'https://rpc.ankr.com/klaytn',
        'KLAY': 'native',
        'native': 'KLAY',          
        'lzChainId': 150,
        'ghost_contract': '0x79DB0f1A83f8e743550EeB5DD5B0B83334F2F083',

    },
    'metis': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 151,
        'ghost_contract': '',

    },
    'coredao': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 153,
        'ghost_contract': '',

    },
    'okt': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 155,
        'ghost_contract': '',

    },
    'canto': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 159,
        'ghost_contract': '',

    },
    'zkevm': {
        'type': 0,        
        'rpc': 'https://rpc.ankr.com/polygon_zkevm',
        'ETH': 'native',
        'native': 'ETH',          
        'lzChainId': 158,
        'ghost_contract': '0xE62d19Df93D84b3552498260188D19A772296B10',

    },
    'zksyncera': {
        'type': 0,        
        'rpc': 'https://rpc.ankr.com/zksync_era',
        'ETH': 'native',
        'native': 'ETH',        
        'lzChainId': 165,
        'ghost_contract': '0x5673B6e6e51dE3479B8deB22dF46B12308db5E1e',

    },
    'base': {
        'type': 2,        
        'rpc': 'https://rpc.ankr.com/base',
        "scan": "https://basescan.org/tx",
        'ETH': 'native',
        'native': 'ETH',        
        'lzChainId': 184,
        'ghost_contract': '0x03e9044d7e8da61815ebed0a5b265fbc9cbdfa4f',

    },
    'linea': {
        'type': 2,        
        'rpc': 'https://rpc.linea.build',
        "scan": "https://lineascan.build/tx",
        'ETH': 'native',
        'native': 'ETH',        
        'lzChainId': 183,
        'ghost_contract': '0x03e9044d7e8da61815ebed0a5b265fbc9cbdfa4f',

    },
    'scroll': {
        'type': 0,        
        'rpc': 'https://rpc.ankr.com/scroll',
        "scan": "https://scrollscan.com/tx",
        'ETH': 'native',
        'native': 'ETH',        
        'lzChainId': 214,
        'ghost_contract': '0x03e9044d7e8da61815ebed0a5b265fbc9cbdfa4f',

    },
    'moonriver': {
        'type': 2,        
        'rpc': 'https://moonriver.publicnode.com',
        'MOVR': 'native',
        'native': 'MOVR',          
        'lzChainId': 167,
        'ghost_contract': '0xd379c3D0930d70022B3C6EBA8217e4B990705540',

    },
    'tenet': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 173,
        'ghost_contract': '',

    },
    'nova': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 175,
        'ghost_contract': '',

    },
    'meter': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 176,
        'ghost_contract': '',

    },
    'sepolia': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 161,
        'ghost_contract': '',

    },
    'kava': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 177,
        'ghost_contract': '',

    },
    'XPLA': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 216,
        'ghost_contract': '',

    },
    'Horizen': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 215,
        'ghost_contract': '',

    },
    'Orderly': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 213,
        'ghost_contract': '',

    },
    'Telos': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 199,
        'ghost_contract': '',

    },
    'Conflux': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 212,
        'ghost_contract': '',

    },
    'Aurora': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 211,
        'ghost_contract': '',

    },
    'Astar': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 210,
        'ghost_contract': '',

    },
    'opBNB': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 202,
        'ghost_contract': '',

    },
    'TomoChain': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 196,
        'ghost_contract': '',

    },
    'zora': {
        'type': 0,        
        'rpc': 'https://rpc.zora.energy',
        "scan": "https://zora.superscan.network/tx",
        'ETH': 'native',
        'native': 'ETH',           
        'lzChainId': 195,
        'ghost_contract': '0x03e9044D7E8da61815EbeD0a5B265Fbc9CBDfA4f',

    },
    'Loot': {
        'type': 0,        
        'rpc': '',
        'lzChainId': 197,
        'ghost_contract': '',

    },
    'mantle': {
        'type': 0,        
        'rpc': 'https://mantle-mainnet.public.blastapi.io',
        "scan": "https://explorer.mantle.xyz/tx",
        'MNT': 'native',
        'native': 'MNT',        
        'lzChainId': 181,
        'ghost_contract': '0x03e9044D7E8da61815EbeD0a5B265Fbc9CBDfA4f',

    },

    'blast': {
        'type': 0,        
        'rpc': 'https://blast.blockpi.network/v1/rpc/public',
        "scan": "https://blastscan.io/tx",
        'ETH': 'native',
        'native': 'ETH',        
        'lzChainId': 243,
        'ghost_contract': '0xc0F14A9a8d3Bc913E660c473c1932FFBDda71b45',

    },


}


log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = f"{log_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"

erc20_abi = json.load(open('abi/erc20_abi.json'))
bridge_abi = json.load(open('abi/brige_abi.json'))
ghost_abi = json.load(open('abi/abi.json'))

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

def check_trx_count(wallet):
    while True:
        try:
            headers = {
            'Referer': f'https://layerzeroscan.com/address/{wallet}',
            }
            original_string = '{"stage":"mainnet","address":"'+wallet+'"}'
            encoded_string = quote(original_string, safe='')
            url = "https://layerzeroscan.com/api/trpc/metrics.volume?input=" + encoded_string

            if config.proxy_use:
                result = requests.get(url=url, proxies=config.proxies, headers=headers)
            else:
                result = requests.get(url=url, headers=headers)     
            data = json.loads(result.text)

            return data["result"]["data"]["volumeTotal"]

        except Exception as error:
            log_error(f' Ошибка сети: Проблема либо в layerzeroscan, либо в proxy, либо проблемы с самой сетью. ctrl+c для остановки скрипта.')
            timeOut("teh")


def get_token_balance(wallet, network, token ):
    try:
        web3 = Web3(Web3.HTTPProvider(address[network]['rpc'], request_kwargs=config.request_kwargs))
        wallet = Web3.to_checksum_address(wallet)

        if address[network][token]=="native":
            balance = web3.eth.get_balance(wallet)
            balance = Web3.from_wei(balance, 'ether')
        else:
            erc20_address = web3.to_checksum_address(address[network][token])
            erc20_contract = web3.eth.contract(address=erc20_address, abi=erc20_abi)
            token_decimals = erc20_contract.functions.decimals().call()
            balance = erc20_contract.functions.balanceOf(wallet).call() / 10 ** token_decimals
        time.sleep(2)    
            
        return balance

    except Exception as error:
        return log_error(f'{network} {token} | Ошибка при получении баланса токенов: Проблема либо в rpc, либо в связке rpc-proxy, либо проблемы с самой сетью.')


def get_token_balance_USD(wallet, network, token ):
    try:
        result = get_token_balance(wallet, network, token )
        if result == "error":
            return "error"
        balance = float(result)
        return balance*config.prices[token]

    except Exception as error:
        return log_error(f'{network} {token} | Ошибка при переводе баланса токенов в USD: {error}')


def log(text, status=""):
    now = datetime.now()
    log_text = now.strftime('%d %H:%M:%S')+": "
    with open(log_file, "a", encoding='utf-8') as f:
        if status == "error":
            color_code = "\033[91m"  # red
            log_text = log_text + "ERROR: "
        elif status == "ok":
            color_code = "\033[92m"  # green
            log_text = log_text + "OK: "
        else:
            color_code = "\033[0m"  # white
        log_text = log_text + f"{text}"
        log_text_color = f"{color_code}{log_text}\033[0m"
        f.write(log_text + "\n")
        print(log_text_color)

def log_error(text):
    log(text, "error")
    return "error"

def log_error_critical(text):
    log(text, "error")
    f=open(f"{log_dir}/critical.log", "a", encoding='utf-8')
    f.write(text + "\n")    
    return "error"

def log_ok(text):
    log(text, "ok")
    return "ok"

def save_wallet_to(filename, wallet):
    f=open(f"{log_dir}/{filename}.log", "a", encoding='utf-8')
    f.write(wallet + "\n")    


def timeOut(type="main"):
    if type=="main":
        time_sleep=random.randint(config.timeoutMin, config.timeoutMax)
    if type=="teh":
        time_sleep=random.randint(config.timeoutTehMin, config.timeoutTehMax)
        
    if int(time_sleep/60) > 0:
        log(f"пауза {int(time_sleep/60)} минут")
    time.sleep(time_sleep)

def get_new_prices(token = False):


    if token:
        try:
            url =f'https://min-api.cryptocompare.com/data/price?fsym={token}&tsyms=USDT'
            if config.proxy_use:
                result = requests.get(url=url, proxies=config.proxies)
            else:
                result = requests.get(url=url) 
            if result.status == 200:
                resp_json = result.json(content_type=None)
                new_price = float(resp_json['USDT'])
                config.prices[token] = new_price
                log(f"Обновил цену для {token}= {new_price}")
        except Exception as error:
            log_error(f'Не смог узнать цену для {token}: {error}')

    else:
            
        if config.prices["last_update"] > int(time.time()-3600):
            return False
        config.prices["last_update"] = int(time.time())

        for token, price in config.prices.items():    
            if token == "last_update":
                continue

            try:
                url =f'https://min-api.cryptocompare.com/data/price?fsym={token}&tsyms=USDT'
                if config.proxy_use:
                    result = requests.get(url=url, proxies=config.proxies)
                else:
                    result = requests.get(url=url)                    
                if result.status_code == 200:
                    resp_json = result.json()
                    new_price = float(resp_json['USDT'])
                    config.prices[token] = new_price
                    log(f"Обновил цену для {token}= {new_price}")
            except Exception as error:
                log_error(f'Не смог узнать цену для {token}: {error}')

            time.sleep(1)

    return True