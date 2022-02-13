import os
from os import getenv
from pathlib import Path
from typing import List
from dotenv import load_dotenv

load_dotenv()

# PATH
PATH_ROOT = Path(os.path.abspath(__file__)).parent.parent
PATH_SESSION = PATH_ROOT.joinpath('sessions')
PATH_STORAGE = PATH_ROOT.joinpath('storage')
if not PATH_SESSION.exists():
    PATH_SESSION.mkdir()
if not PATH_STORAGE.exists():
    PATH_STORAGE.mkdir()

# telethon configs
BOT_TOKEN = getenv('BOT_TOKEN')
YOUR_BOT_USERNAME = getenv('YOUR_BOT_USERNAME')
API_ID = int(getenv('API_ID'))
API_KEY = getenv('API_KEY')

# proxy for connecting
PROXY = (getenv('PROXY_PROTOCOL', 'socks5'), getenv('PROXY_HOST', 'localhost'), int(getenv('PROXY_PORT', 9050)))
if None in PROXY:
    PROXY = None

# sql
SQL_DB = getenv('SQL_DATABASE', 'database')
SQL_USER = getenv('SQL_USER', 'user')
SQL_PASSWORD = getenv('SQL_PASSWORD', 'password')
SQL_PORT = int(getenv('SQL_PORT', '3306'))
SQL_HOST = getenv('SQL_HOST', 'localhost')
SQL_TYPE = getenv('SQL_TYPE', 'mysql')


# commands configs
class COMMANDS:
    START = '/start'
    CONNECT = "💌 به مخاطب خاصم وصلم کن!"
    GIVE_MY_LINK = 'لینک ناشناس من 📬'
    INSTAGRAM = '/Instagram'
    LINK = '/link'
    CANCEL_CONNECT = 'انصراف'
    GET_UNSEEN_MESSAGES = '/newmsg'

    @classmethod
    def command_list(cls) -> List[str]:
        return [getattr(COMMANDS, the_attr) for the_attr in dir(COMMANDS) if not the_attr.startswith('__')]


# messages
class MESSAGES:
    AFTER_START_COMMAND = """حله!

چه کاری برات انجام بدم؟"""
    AFTER_BAD_COMMAND = """متوجه نشدم :/

چه کاری برات انجام بدم؟"""
    AFTER_CONNECT_COMMAND = """برای اینکه بتونم به مخاطب خاصت بطور ناشناس وصلت کنم، یکی از این ۲ کار رو انجام بده:

راه اول 👈 : Username@ یا همون آی‌دی تلگرام اون شخص رو الان وارد ربات کن!

راه دوم 👈 : الان یه پیام متنی از اون شخص به این ربات فوروارد کن تا ببینم عضو هست یا نه!"""
    AFTER_GIVE_MY_LINK_COMMAND_EXTRA = F"""☝️ پیام بالا رو به دوستات و گروه‌هایی که می‌شناسی فـوروارد کن یا لـینک داخلش رو تو شبکه‌های اجتماعی بذار و توئیت کن، تا بقیه بتونن بهت پیام ناشناس بفرستن. پیام‌ها از طریق همین برنامه بهت می‌رسه.

اینستاگرام داری و میخوای دنبال کننده های اینستاگرامت برات پیام ناشناس بفرستن؟
پس روی دستور 👈🏻 {COMMANDS.INSTAGRAM} کلیک کن!"""
    USER_NOT_FOUND = f"""متاسفانه مخاطبت الان عضو ربات نیست!

چطوره یه جوری لینک ربات رو بهش برسونی تا بیاد و عضو بشه؟ مثلا لینک خودت رو بهش بفرستی یا اگه جزء دنبال کننده‌های اینستاگرامته لینکت رو در اینستاگرامت بذاری.

برای دریافت لینک 👈 {COMMANDS.LINK}"""
    RETRY_CONNECT = """👈 یه پیام از مخاطب خاصت برام فوروارد کن و یا آی دیش رو برام بفرست تا بتونم چک کنم که عضو ربات هست یا نه!"""
    YOUR_TARGET_STOPPED_THE_BOT = """مخاطبت ربات رو خاموش کرده و پیام بهش نرسید! هروقت دوباره از ربات استفاده کنه پیامت رو میبینه.

چه کاری برات انجام بدم؟"""
    SEND_SUCCESSFULLY = """پیام شما ارسال شد 😊

چه کاری برات انجام بدم؟"""
    GET_MESSAGE_INSTRUCTION = F"""📬 شما یک پیام ناشناس جدید دارید !

جهت دریافت کلیک کنید 👈 {COMMANDS.GET_UNSEEN_MESSAGES}"""
    NO_ANY_MESSAGES = f"""پیام نخونده‌ای نداری !

چطوره با زدن این دستور 👈 {COMMANDS.LINK} لینک خودت رو بگیری و به دوستات یا گروه‌ها بفرستی تا بتونند بهت پیام ناشناس بفرستند؟ 😊"""
    YOUR_MSG_WAS_READ = """این پیامت ☝️ رو دید!"""

    BTN_ANSWER = '✍️ پاسخ'
    BTN_BLOCK = '⛔️ بلاک'
    WAITING_TO_ANSWER = "☝️ در حال پاسخ دادن به فرستنده این پیام هستی ... ؛ منتظریم بفرستی :)"

    INSTAGRAM_DESCRIPTION = """میخوای دنبال کننده های اینستاگرامت برات پیام ناشناش بفرستن؟ 🤔

کافیه لینک ناشناس رو کپی کنی و توی  پروفایلت وارد کنی

لینک مخصوصت 👇"""


class TEMPLATES_MESSAGES:
    @staticmethod
    def AFTER_GIVE_MY_LINK_COMMAND(name: str, link: str):
        return f"""سلام {name} هستم ✋️

لینک زیر رو لمس کن و هر حرفی که تو دلت هست یا هر انتقادی که نسبت به من داری رو با خیال راحت بنویس و بفرست. بدون اینکه از اسمت باخبر بشم پیامت به من می‌رسه. خودتم می‌تونی امتحان کنی و از بقیه بخوای راحت و ناشناس بهت پیام بفرستن، حرفای خیلی جالبی می‌شنوی! 😉

👇👇
{link}"""

    @staticmethod
    def READY_TO_SEND_MESSAGE(name):
        return f"""در حال ارسال پیام ناشناس به {name} هستی!

با خیال راحت هر حرف یا انتقادی که تو دلت هست بنویس ، این پیام بصورت کاملا ناشناس ارسال میشه :)"""

    RESPOND_LIKE = 'respond'

    @staticmethod
    def RESPOND_TO_MESSAGE(message_orm_id, ):
        return f"{TEMPLATES_MESSAGES.RESPOND_LIKE}_{message_orm_id}"

    @staticmethod
    def YOUR_LINK(user_id):
        return f'https://t.me/{YOUR_BOT_USERNAME}?start={user_id}'
