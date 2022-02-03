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
MYSQL_DB = getenv('MYSQL_DATABASE', 'database')
MYSQL_USER = getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = getenv('MYSQL_PASSWORD', 'password')
MYSQL_PORT = int(getenv('MYSQL_PORT', '3306'))
MYSQL_HOST = getenv('MYSQL_HOST', 'localhost')


# commands configs
class COMMANDS:
    START = '/start'
    CONNECT = "💌 به مخاطب خاصم وصلم کن!"
    GIVE_MY_LINK = 'لینک ناشناس من 📬'
    INSTAGRAM = '/Instagram'


# messages
class MESSAGES:
    START = """حله!

چه کاری برات انجام بدم؟"""
    AFTER_BAD_COMMAND = """متوجه نشدم :/

چه کاری برات انجام بدم؟"""
    AFTER_CONNECT_COMMAND = """برای اینکه بتونم به مخاطب خاصت بطور ناشناس وصلت کنم، یکی از این ۲ کار رو انجام بده:

راه اول 👈 : Username@ یا همون آی‌دی تلگرام اون شخص رو الان وارد ربات کن!

راه دوم 👈 : الان یه پیام متنی از اون شخص به این ربات فوروارد کن تا ببینم عضو هست یا نه!"""
    AFTER_GIVE_MY_LINK_COMMAND_EXTRA = F"""☝️ پیام بالا رو به دوستات و گروه‌هایی که می‌شناسی فـوروارد کن یا لـینک داخلش رو تو شبکه‌های اجتماعی بذار و توئیت کن، تا بقیه بتونن بهت پیام ناشناس بفرستن. پیام‌ها از طریق همین برنامه بهت می‌رسه.

اینستاگرام داری و میخوای دنبال کننده های اینستاگرامت برات پیام ناشناس بفرستن؟
پس روی دستور 👈🏻 {COMMANDS.INSTAGRAM} کلیک کن!"""


class TEMPLATES_MESSAGES:
    @staticmethod
    def AFTER_GIVE_MY_LINK_COMMAND(name: str, link: str):
        return f"""سلام {name} هستم ✋️

لینک زیر رو لمس کن و هر حرفی که تو دلت هست یا هر انتقادی که نسبت به من داری رو با خیال راحت بنویس و بفرست. بدون اینکه از اسمت باخبر بشم پیامت به من می‌رسه. خودتم می‌تونی امتحان کنی و از بقیه بخوای راحت و ناشناس بهت پیام بفرستن، حرفای خیلی جالبی می‌شنوی! 😉

👇👇
{link}"""
