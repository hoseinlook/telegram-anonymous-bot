import asyncio
import datetime
import re
from datetime import datetime

import telethon.tl.types
from telethon import TelegramClient, events, Button
from telethon.events import NewMessage
from telethon.events.inlinequery import InlineQuery

from .models import User
from .repository import UserRepository, MessageRepository
from .config import API_KEY, API_ID, BOT_TOKEN, PROXY, PATH_SESSION, COMMANDS, MESSAGES, TEMPLATES_MESSAGES

user_repository = UserRepository()
message_repository = MessageRepository()
client = TelegramClient(str(PATH_SESSION.joinpath('bot')), API_ID, API_KEY, proxy=PROXY, connection_retries=10000).start(
    bot_token=BOT_TOKEN)

print('BOT CONNECTED...')


@client.on(events.NewMessage(pattern=COMMANDS.START))
async def start(event):
    user: telethon.tl.types.User = event.chat
    UserRepository().insert(User(user_id=user.id, access_hash=user.access_hash, full_name=f'{user.first_name}_{user.last_name}', username=user.username, status=User.STATUS.ACTIVE))
    await event.respond(MESSAGES.AFTER_START_COMMAND, buttons=[
        [Button.text(COMMANDS.CONNECT, resize=True, single_use=True)],
        [Button.text(COMMANDS.GIVE_MY_LINK, resize=True, single_use=True)],
    ])


@client.on(events.NewMessage(pattern=COMMANDS.CONNECT))
async def do_connection(event):
    async with client.conversation(event.chat) as conv:
        await conv.send_message(MESSAGES.AFTER_CONNECT_COMMAND, buttons=[Button.text(COMMANDS.CANCEL_CONNECT, resize=True, single_use=True)])
        response = await conv.get_response()
        if response.message == COMMANDS.CANCEL_CONNECT: return

        if response.message.startswith('@'):
            username = re.findall('^@[^\s]+', response.message)
        else:
            username = "asd"


@client.on(events.NewMessage(pattern=COMMANDS.CANCEL_CONNECT))
async def do_cancel(event):
    await start(event)


client.run_until_disconnected()
