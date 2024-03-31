
# Функционал
Скрипт автоматизирует функционал сайта https://ghostmint.tech/ , Основная задача сайта - помощь в прогреве ваших кошельков в различных сетях, большое внимание уделяется сети BLAST, если вы минтите в этой сети нфт вы автоматически претендуете на Airdrop, в случае, если наш проект получит дроп от BLAST. Также основные пользователи нашего проекта будут получать yields от суммы минта, в качестве ретро-вознаграждения (основная технологическая фишка BLAST). Ультрадешевый прогрев доступен и в других сетях, начиная от SCROLL и заканчивая LINEA.

Скрипт позволяет в автоматическом режиме сразу на большом количестве кошельков минтить НФТ от проекта GhostMint и бриджить их через L0 в другие сети.

Скрипт позволят выбрать сети назначения и сети источники, позволяет ограничить выбор направления максимальной комиссией которую вы готовы заплатить и многие другие настройки - читай все комментарии в файле config.py


# Настройка
Сеть зора из РФ работет только с проксями, рекомендую используйте ротируемые/мобильные прокси

Этого вам хватит для работы скрипта на пол года. В настройках надо указать только один проксик, желательно ротируемый, он каждый запрос посылает с нового Ip адреса.

Остальные насйтроки произведите в соответствии с вашими представлениями о прогреве кошельков, каждый параметр подробно описан в комментариях.
все настройки производятся в файле config.py.

Если у вас возникнут вопросы по настройке скрипта, вы всегда можете обратиться за помощью в чат - https://t.me/plushkin_chat

Три варианта запуска:
1. mint.py   -   просто минтит в случайной сети НФТ. сети из которых выбирать указываете в config.py. Не будет минтить если стоимость минта (цена НФТ + комиссия сети) превышает указанный вами порог.
2. bridge.py  -  ищет НФТ в указанных вами сетях и перекидывает их через мост L0 в случайную сеть. Максимальнные комиссии так же ограничиваются в настйроках .
3. main.py - Проверяет если на кошельке нет НФТ в указанных вами сетях, то минтит новую НФТ в случайной сети.  Потом Бриджит либо новую либо уже существующую НФТ в другую сеть (набор сетей указывается в настройках)

# Установка и запуск:

Linux/Mac - https://www.youtube.com/watch?v=8rJ-96cPFwU
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```
Windows - https://www.youtube.com/watch?v=EqC42mnbByc
```
pip install virtualenv
virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py
```


