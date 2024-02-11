# Parser_teleBot
 ## Как установить

Python 3.10 должен быть уже установлен.
Затем используйте `pip`  для установки зависимостей:
```
pip install -r requirements.txt
```
### будет установлен:

aiofiles==23.1.0
aiogram==3.1.1
aiohttp==3.8.6
aiosignal==1.3.1
annotated-types==0.6.0
async-timeout==4.0.3
attrs==23.1.0
bcrypt==3.2.0
beautifulsoup4==4.12.2
blinker==1.4
cattrs==23.2.3
certifi==2023.7.22
cffi==1.16.0
chardet==4.0.0
charset-normalizer==3.3.2
click==8.0.3
colorama==0.4.4
cryptography==3.4.8
distlib==0.3.7
distro==1.7.0
et-xmlfile==1.1.0
exceptiongroup==1.1.3
fasteners==0.14.1
filelock==3.12.2
fpdf==1.7.2
frozenlist==1.4.1
future==0.18.2
h11==0.14.0
httplib2==0.20.2
idna==3.3
importlib-metadata==4.6.4
jeepney==0.7.1
keyring==23.5.0
launchpadlib==1.10.16
lazr.restfulclient==0.14.4
lazr.uri==1.0.6
lockfile==0.12.2
macaroonbakery==1.3.1
magic-filter==1.0.12
Mako==1.1.3
MarkupSafe==2.0.1
monotonic==1.6
more-itertools==8.10.0
multidict==6.0.4
netifaces==0.11.0
numpy==1.26.3
oauthlib==3.2.0
olefile==0.46
openpyxl==3.1.2
outcome==1.2.0
pandas==2.2.0
paramiko==2.9.3
pexpect==4.8.0
Pillow==9.0.1
platformdirs==3.10.0
protobuf==3.12.4
psycopg2==2.9.9
ptyprocess==0.7.0
pycparser==2.21
pydantic==2.3.0
pydantic_core==2.6.3
PyJWT==2.3.0
pymacaroons==0.13.0
PyNaCl==1.5.0
pyparsing==2.4.7
pyRFC3339==1.1
PySocks==1.7.1
python-dateutil==2.8.1
python-dotenv==1.0.1
pytz==2022.1
pyxdg==0.27
reportlab==3.6.8
requests==2.25.1
requests-cache==1.1.1
SecretStorage==3.3.1
selenium==4.12.0
six==1.16.0
sniffio==1.3.0
sortedcontainers==2.4.0
soupsieve==2.5
trio==0.22.2
trio-websocket==0.10.4
typing_extensions==4.7.1
tzdata==2023.4
url-normalize==1.4.3
urllib3==1.26.5
virtualenv==20.24.3
wadllib==1.3.6
wsproto==1.2.0
xdg==5.0.0
xlwt==1.3.0
yarl==1.9.4
zipp==1.0.0

Создание бота:
BotFather: Зайдите в Telegram и найдите бота BotFather.
Создание: Введите команду /newbot и следуйте инструкциям, чтобы создать нового бота.
Токен: Вам будет предоставлен токен бота, который нужно сохранить в .env(BOT_TOKEN)


Установите PostgreSQL( можно установить PgAdmin4)
*Потребуется PASSWORD И USER_NAME 

Запустите файл create_db.py 
для создания базы данных

Запустите файл create_tables.py 
для создания таблиц в базе данных

Запустите файл Filling_cities.py
для заполнения таблицы cities