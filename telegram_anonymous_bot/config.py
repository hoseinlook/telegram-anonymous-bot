import os
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# PATH
PATH_ROOT = Path(os.path.abspath(__file__)).parent.parent
PATH_SESSION = PATH_ROOT.joinpath('sessions')
if not PATH_SESSION.exists():
    PATH_SESSION.mkdir()

# telethon configs
BOT_TOKEN = getenv('BOT_TOKEN')
API_ID = int(getenv('API_ID'))
API_KEY = getenv('API_KEY')

PROXY = (getenv('PROXY_PROTOCOL', 'socks5'), getenv('PROXY_HOST', 'localhost'), int(getenv('PROXY_PORT', 9050)))

# sql
MYSQL_DB = getenv('MYSQL_DB', 'database')
MYSQL_USER = getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = getenv('MYSQL_PASSWORD', 'password')
MYSQL_PORT = int(getenv('MYSQL_PORT', '3306'))
MYSQL_HOST = getenv('MYSQL_HOST', 'localhost')
