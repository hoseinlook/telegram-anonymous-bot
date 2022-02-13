import re
from typing import Union, List
import telethon.tl.types
from telethon import TelegramClient, events, Button
from .config import API_KEY, API_ID, BOT_TOKEN, PROXY, PATH_SESSION, COMMANDS, MESSAGES, TEMPLATES_MESSAGES
from .exceptions import CanceledError
from .logger import error_logger, info_log, TELEGRAM_LOG_LEVEL
from .models import User, Message, Action
from .repository import UserRepository, MessageRepository, ActionRepository

user_repository = UserRepository()
message_repository = MessageRepository()
info_log.log(level=TELEGRAM_LOG_LEVEL, msg='BOT CONNECTED TO SQLDB ...')
if PROXY is not None:
    client = TelegramClient(str(PATH_SESSION.joinpath('bot')), API_ID, API_KEY, proxy=PROXY, connection_retries=100000).start(
        bot_token=BOT_TOKEN)
else:
    client = TelegramClient(str(PATH_SESSION.joinpath('bot')), API_ID, API_KEY, connection_retries=100000).start(
        bot_token=BOT_TOKEN)

info_log.log(level=TELEGRAM_LOG_LEVEL, msg='BOT CONNECTED TO TELEGRAM ...')


async def reset_btns(event, message):
    await event.respond(message, buttons=[
        [Button.text(COMMANDS.CONNECT, resize=True, single_use=True)],
        [Button.text(COMMANDS.GIVE_MY_LINK, resize=True, single_use=True)],
    ])


# @client.on(events.NewMessage())
# async def bad_command(event):
#     user: telethon.tl.types.User = event.chat
#     UserRepository().insert(User(user_id=user.id, access_hash=user.access_hash, first_name=user.first_name, last_name=user.last_name, username=user.username, status=User.STATUS.ACTIVE))
#     if event.message.message not in COMMANDS.command_list() and not str(event.message.message).startswith(COMMANDS.START):
#         await reset_btns(event, MESSAGES.AFTER_BAD_COMMAND)


@client.on(events.NewMessage(pattern=COMMANDS.START))
async def start(event):
    user: telethon.tl.types.User = event.chat
    UserRepository().insert(User(user_id=user.id, access_hash=user.access_hash, first_name=user.first_name, last_name=user.last_name, username=user.username, status=User.STATUS.ACTIVE))
    if len(event.message.message.split()) >= 2:
        info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{user} clicked {COMMANDS.START}')
        target_user_id = event.message.message.split()[1]
        user = UserRepository().get_user_with_id(target_user_id)
        await do_connection(event, user)
    else:
        await reset_btns(event, MESSAGES.AFTER_START_COMMAND)


@client.on(events.NewMessage(pattern=COMMANDS.CONNECT))
async def do_connection(event, the_user=None):
    async def loop_to_get_target(conv) -> Union[User, None]:
        while True:
            response = await conv.get_response()
            if response.message == COMMANDS.CANCEL_CONNECT: raise CanceledError()
            if response.message.startswith('@'):
                username = re.findall('^@[^\s]+', response.message)[0]
                target_user = await client.get_entity(username)
                target_user_id = target_user.id
            else:

                if not hasattr(response, "forward") or response.forward is None:
                    await conv.send_message(MESSAGES.RETRY_CONNECT)
                    continue
                target_user_id = response.forward.chat_id
                if target_user_id is None:
                    await conv.send_message(MESSAGES.RETRY_CONNECT)
                    continue
            user = UserRepository().get_user_with_id(target_user_id)
            return user

    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} clicked {COMMANDS.CONNECT}')
    async with client.conversation(event.chat) as conv:
        await conv.send_message(MESSAGES.AFTER_CONNECT_COMMAND, buttons=[Button.text(COMMANDS.CANCEL_CONNECT, resize=True, single_use=True)])

        try:
            if the_user is None:
                the_user: Union[User, None] = await loop_to_get_target(conv)
            if the_user is None:
                await reset_btns(event, MESSAGES.USER_NOT_FOUND)
                return

            await conv.send_message(TEMPLATES_MESSAGES.READY_TO_SEND_MESSAGE(the_user.first_name))
            response = await conv.get_response()
            if response.message == COMMANDS.CANCEL_CONNECT: raise CanceledError()
            new_message = Message(from_user_id=event.chat.id, to_user_id=the_user.id, message=response.message, msg_id=response.id)
            MessageRepository().insert(new_message)
            try:
                target_entity = await client.get_entity(telethon.tl.types.InputPeerUser(user_id=the_user.id, access_hash=int(the_user.access_hash)))
                await client.send_message(target_entity, MESSAGES.GET_MESSAGE_INSTRUCTION)
                await reset_btns(event, MESSAGES.SEND_SUCCESSFULLY)
                new_message.status = Message.STATUS.SENT
                MessageRepository().commit()
                return
            except Exception as e:
                new_message.status = Message.STATUS.FAILED
                error_logger.error(f"send_anonymous_message_error {type(e)}-{e}-{event.chat}")
                MessageRepository().commit()
                print('SENDING ERROR:', type(e), e)
                await reset_btns(event, MESSAGES.YOUR_TARGET_STOPPED_THE_BOT)
                return

        except CanceledError as e:
            pass
        except Exception as e:
            error_logger.error(f"do_connection_error {type(e)}-{e}")
            await reset_btns(event, MESSAGES.USER_NOT_FOUND)
            return


@client.on(events.NewMessage(pattern=COMMANDS.GET_UNSEEN_MESSAGES))
async def get_new_messages(event):
    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} clicked {COMMANDS.GET_UNSEEN_MESSAGES}')
    user_id = event.chat.id
    message_list: List[Message] = list(MessageRepository().all_unseen_messages(user_id))
    if len(message_list) == 0:
        await reset_btns(event, MESSAGES.NO_ANY_MESSAGES)
        return

    for message_orm in message_list:
        sender_user = UserRepository().get_user_with_id(message_orm.from_user_id)
        sender_entity = await client.get_entity(telethon.tl.types.InputPeerUser(user_id=sender_user.id, access_hash=int(sender_user.access_hash)))
        await client.send_message(entity=sender_entity, message=MESSAGES.YOUR_MSG_WAS_READ, reply_to=message_orm.msg_id)
        # builder: InlineBuilder = event.builder
        the_message = await  client.get_messages(sender_entity, ids=message_orm.msg_id)
        if len(the_message.message) < 10:
            the_message.message = F"‌                                                 ‌ ‌‌‌    ‌‌\n{the_message.message}"
        await event.respond(the_message, buttons=[
            [Button.inline(MESSAGES.BTN_BLOCK, data=1), Button.inline(MESSAGES.BTN_ANSWER, data=TEMPLATES_MESSAGES.RESPOND_TO_MESSAGE(message_orm.id))],
        ])

        message_orm.status = Message.STATUS.SEEN
        MessageRepository().commit()


@client.on(events.CallbackQuery())
async def handel_callback(event):
    body = event.data.decode('utf8')
    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} clicked a callback btn - btn_body={body}')
    if body.startswith(TEMPLATES_MESSAGES.RESPOND_LIKE):
        message_orm_id = int(body.split('_')[-1])
        sender_message_orm = MessageRepository().get_with_message_id(message_orm_id)

        async with client.conversation(event.chat) as conv:
            await conv.send_message(MESSAGES.WAITING_TO_ANSWER, buttons=[Button.text(COMMANDS.CANCEL_CONNECT, resize=True, single_use=True)])
            response = await conv.get_response()
            if response.message == COMMANDS.CANCEL_CONNECT: return
            new_message = Message(from_user_id=sender_message_orm.to_user_id, to_user_id=sender_message_orm.from_user_id, message=response.message, msg_id=response.id)
            MessageRepository().insert(new_message)
            try:
                the_user = UserRepository().get_user_with_id(new_message.to_user_id)
                target_entity = await client.get_entity(telethon.tl.types.InputPeerUser(user_id=the_user.id, access_hash=int(the_user.access_hash)))
                await client.send_message(target_entity, MESSAGES.GET_MESSAGE_INSTRUCTION)
                await reset_btns(event, MESSAGES.SEND_SUCCESSFULLY)
                new_message.status = Message.STATUS.SENT
                MessageRepository().commit()
                return
            except Exception as e:
                new_message.status = Message.STATUS.FAILED
                error_logger.error(f"{type(e)}-{e}-{body}-{event.chat}")
                MessageRepository().commit()
                print('SENDING ERROR:', type(e), e)
                await reset_btns(event, MESSAGES.YOUR_TARGET_STOPPED_THE_BOT)
                return


@client.on(events.NewMessage(pattern=COMMANDS.LINK))
async def do_link(event):
    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} clicked {COMMANDS.LINK}')
    user = UserRepository().get_user_with_id(event.chat.id)
    link = TEMPLATES_MESSAGES.YOUR_LINK(user.id)
    await reset_btns(event, TEMPLATES_MESSAGES.AFTER_GIVE_MY_LINK_COMMAND(user.first_name, link))
    await reset_btns(event, MESSAGES.AFTER_GIVE_MY_LINK_COMMAND_EXTRA)


@client.on(events.NewMessage(pattern=COMMANDS.GIVE_MY_LINK))
async def do_link(event):
    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} clicked {COMMANDS.GIVE_MY_LINK}')
    user = UserRepository().get_user_with_id(event.chat.id)
    link = TEMPLATES_MESSAGES.YOUR_LINK(user.id)
    await reset_btns(event, TEMPLATES_MESSAGES.AFTER_GIVE_MY_LINK_COMMAND(user.first_name, link))
    await reset_btns(event, MESSAGES.AFTER_GIVE_MY_LINK_COMMAND_EXTRA)


@client.on(events.NewMessage(pattern=COMMANDS.INSTAGRAM))
async def do_link(event):
    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} clicked {COMMANDS.INSTAGRAM}')
    user = UserRepository().get_user_with_id(event.chat.id)
    link = TEMPLATES_MESSAGES.YOUR_LINK(user.id)
    await reset_btns(event, MESSAGES.INSTAGRAM_DESCRIPTION)
    await reset_btns(event, link)


@client.on(events.NewMessage(pattern=COMMANDS.CANCEL_CONNECT))
async def do_cancel(event):
    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} clicked {COMMANDS.CANCEL_CONNECT}')
    await start(event)


@client.on(events.NewMessage())
async def capture_all_actions_for_debugging(event):
    msg_id = event.message.id
    user_id = event.chat.id
    action = event.message.message
    ActionRepository().insert(Action(msg_id=msg_id, user_id=user_id, action=action))
    info_log.log(level=TELEGRAM_LOG_LEVEL, msg=f'{event.chat.first_name} sent-> {action}')


client.run_until_disconnected()
