
#то что ниже обязательно заполнить своими данными
proxy_use = 0 #  0 - не использовать, 1 - Ротируемый прокси(Каждый запрос с нового ip адресса) , 2 - прокси со ссылкой для смены ip
proxy_login = 'plude'
proxy_password = '5l'
proxy_address = 'gate.nodemaven.com'
proxy_port = '8080'
proxy_changeIPlink = "none"


#то что ниже желательно настроить под себя
max_komissia = 2 # указывается в $ (пример 1.2 или 0.15) в нее входит плата за подписание транзакции (но не во всех сетях это учитывается верно) Для минта, сюда так же входит цена картинки.
min_balance = 1.5 # указывается в $. Кошелек с таким балансом и ниже, будет пропускать, считаться пустым.
veroyatnost = 100 # вероятность что кошелек отработает указывается в %
skolko_trans = [1,5] # указывайте диапазон сколько делать транзакций на каждом кошельке. Если это модуль минт, то будет делать столько минтов сколько вы укажете
predel_trans = 100 # количество транзакций в Л0. кошельки пропускаются если уже достигли этого значения по транзакциям

#networks_from: 
# networks_from = ["arbitrum" , "polygon", "bsc", "zora", "scroll", "base", "linea", "mantle", "optimism", "blast"]
networks_from = ["arbitrum" , "polygon", "bsc", "zora", "scroll", "base", "linea", "mantle", "optimism", "blast"]

# networks_to = ["arbitrum" , "polygon", "bsc", "zora", "scroll", "base", "linea", "mantle", "optimism", "blast"]
networks_to = ["arbitrum" , "polygon", "bsc", "zora", "scroll", "base", "linea", "mantle", "optimism", "blast"]


#укажите паузу в работе между кошельками, минимальную и максимальную. 
#При смене каждого кошелька будет выбрано случайное число. Значения указываются в секундах
timeoutMin = 10 #минимальная 
timeoutMax = 30 #максимальная
#задержки между операциями в рамках одного кошелька
timeoutTehMin = 3 #минимальная 
timeoutTehMax = 10 #максимальная



#то что ниже можно менять только если понимаешь что делаешь
proxies = { 'all': f'http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}',}
if proxy_use:
    request_kwargs = {"proxies":proxies, "timeout": 120}
else:
    request_kwargs = {"timeout": 120}
gas_kef=1.4 #коэфициент допустимого расхода газа на подписание транзакций. можно выставлять от 1.1 до 2


rpc_links = {
    'eth': 'https://rpc.ankr.com/eth',
    'polygon': 'https://polygon-rpc.com/',
    'arbitrum': 'https://arb1.arbitrum.io/rpc',
    'optimism':  'https://rpc.ankr.com/optimism',
    'bsc': 'https://bscrpc.com',
    'fantom': 'https://rpc.ftm.tools/',
    'avax': 'https://api.avax.network/ext/bc/C/rpc',
}


prices = {
    "MATIC": 0.945,
    "BNB": 446,
    "ETH": 3690,
    "MNT": 22,
    "last_update": 0
}



