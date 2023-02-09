import datetime
import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from ..bot import Bot
from ..utils.helpers import logger_chat
from .setting import config_groups


@Bot.on_message(filters.linked_channel | filters.pinned_message)
async def unpin(app: Bot, message: Message):
    if str(message.chat.id) in config_groups:
        if config_groups[str(message.chat.id)]['unpin']:
            while True:
                try:
                    if message.service:
                        await message.delete()
                        logger_chat('unpin', message, f'service message id {message.id} removed')
                    else:
                        await app.unpin_chat_message(message.chat.id, message.id)
                        logger_chat('unpin', message, f'linked channel message id {message.id} unpinned')
                    break
                except FloodWait as e:
                    logger_chat('unpin', message, f'FloodWait {message.id} for {e.value}s')
                    time.sleep(e.value)


@Bot.on_message(filters.new_chat_members)
async def kick(app: Bot, message: Message):
    if str(message.chat.id) in config_groups:
        if config_groups[str(message.chat.id)]['kick']:
            while True:
                try:
                    srv_msg = await app.ban_chat_member(
                        message.chat.id,
                        message.from_user.id,
                        until_date=datetime.datetime.now() + datetime.timedelta(seconds=60)
                    )
                    await message.delete()
                    await srv_msg.delete()
                    logger_chat('kick', message,
                                f'user {message.from_user.id} kicked and deleted service messages')
                    break
                except FloodWait as e:
                    logger_chat('kick', message, f'FloodWait {message.id} for {e.value}s')
                    time.sleep(e.value)


@Bot.on_message(filters.group & ~ filters.service)
async def ban_channel_message(bot: Bot, message: Message) -> None:
    if str(message.chat.id) in config_groups:
        if config_groups[str(message.chat.id)]['ban_channel_message']:
            while True:
                try:
                    white_list = [message.chat.id]
                    if message.chat.linked_chat:
                        white_list.append(message.chat.linked_chat.id)

                    # allow: linked_channel, anonymous_admin
                    if message.sender_chat and message.sender_chat.id not in white_list:
                        await message.delete()
                        await bot.ban_chat_member(message.chat.id, message.sender_chat.id)
                        logger_chat('ban_channel_message', message,
                                    f'channel {message.sender_chat.id} banned')
                    break
                except FloodWait as e:
                    logger_chat('ban_channel_message', message, f'FloodWait {message.id} for {e.value}s')
                    time.sleep(e.value)
