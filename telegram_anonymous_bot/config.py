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
YOUR_BOT_USERNAME = getenv('YOUR_BOT_USERNAME')
API_ID = int(getenv('API_ID'))
API_KEY = getenv('API_KEY')

# proxy for connecting
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
    LINK = '/link'
    CANCEL_CONNECT = 'انصراف'
    GET_UNSEEN_MESSAGES = '/newmsg'


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
    WAITING_TO_ANSWER ="☝️ در حال پاسخ دادن به فرستنده این پیام هستی ... ؛ منتظریم بفرستی :)"


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
