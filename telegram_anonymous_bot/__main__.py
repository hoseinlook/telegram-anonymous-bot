import asyncio
import datetime
import re
from datetime import datetime
from typing import Union
import telethon.tl.types
from telethon import TelegramClient, events, Button
from telethon.events import NewMessage
from telethon.events.inlinequery import InlineQuery

from .exceptions import CanceledError
from .models import User, Message
from .repository import UserRepository, MessageRepository
from .config import API_KEY, API_ID, BOT_TOKEN, PROXY, PATH_SESSION, COMMANDS, MESSAGES, TEMPLATES_MESSAGES

user_repository = UserRepository()
message_repository = MessageRepository()
client = TelegramClient(str(PATH_SESSION.joinpath('bot')), API_ID, API_KEY, proxy=PROXY, connection_retries=10000).start(
    bot_token=BOT_TOKEN)

print('BOT CONNECTED...')


async def reset_btns(event, message):
    await event.respond(message, buttons=[
        [Button.text(COMMANDS.CONNECT, resize=True, single_use=True)],
        [Button.text(COMMANDS.GIVE_MY_LINK, resize=True, single_use=True)],
    ])


@client.on(events.NewMessage(pattern=COMMANDS.START))
async def start(event):
    user: telethon.tl.types.User = event.chat
    UserRepository().insert(User(user_id=user.id, access_hash=user.access_hash, first_name=user.first_name, last_name=user.last_name, username=user.username, status=User.STATUS.ACTIVE))
    await reset_btns(event, MESSAGES.AFTER_START_COMMAND)


@client.on(events.NewMessage(pattern=COMMANDS.CONNECT))
async def do_connection(event):
    async def loop_to_get_target(conv) -> Union[User, None]:
        while True:
            response = await conv.get_response()
            if response.message == COMMANDS.CANCEL_CONNECT: raise CanceledError()
            if response.message.startswith('@'):
                username = re.findall('^@[^\s]+', response.message)[0]
                target_user = await client.get_entity(username)
                target_user_id = target_user.id
            else:
                print('WITH forwarding')
                print(response)
                if not hasattr(response, "forward") or response.forward is None:
                    await conv.send_message(MESSAGES.RETRY_CONNECT)
                    continue
                target_user_id = response.forward.chat_id
                if target_user_id is None:
                    await conv.send_message(MESSAGES.RETRY_CONNECT)
                    continue
            user = UserRepository().get_user_with_id(target_user_id)
            return user

    async with client.conversation(event.chat) as conv:
        await conv.send_message(MESSAGES.AFTER_CONNECT_COMMAND, buttons=[Button.text(COMMANDS.CANCEL_CONNECT, resize=True, single_use=True)])

        try:
            the_user: Union[User, None] = await loop_to_get_target(conv)
            if the_user is None:
                await reset_btns(event, MESSAGES.USER_NOT_FOUND)
                return

            await conv.send_message(TEMPLATES_MESSAGES.READY_TO_SEND_MESSAGE(the_user.first_name))
            response = await conv.get_response()
            new_message = Message(from_user_id=event.chat.id, to_user_id=the_user.id, message=response.message)
            MessageRepository().insert(new_message)
            try:
                target_entity = await client.get_entity(telethon.tl.types.InputPeerUser(user_id=the_user.id, access_hash=int(the_user.access_hash)))
                await client.send_message(target_entity, response.message)
                new_message.status = Message.STATUS.SENT
                MessageRepository().commit()
            except Exception as e:
                new_message.status = Message.STATUS.FAILED
                MessageRepository().commit()
                print('SENDING ERROR:', type(e), e)
                await reset_btns(event, MESSAGES.YOUR_TARGET_STOPPED_THE_BOT)
                return

        except CanceledError as e:
            pass
        except Exception as e:
            print("error ", type(e), e)
            await reset_btns(event, MESSAGES.USER_NOT_FOUND)
            return


@client.on(events.NewMessage(pattern=COMMANDS.CANCEL_CONNECT))
async def do_cancel(event):
    await start(event)


client.run_until_disconnected()