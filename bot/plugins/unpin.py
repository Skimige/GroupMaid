import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors.exceptions import FloodWait, ChatAdminRequired
from ..bot import Bot


@Bot.on_message(filters.group & (filters.linked_channel | filters.pinned_message))
async def unpin(app: Bot, message: Message):
    while True:
        try:
            if message.service:
                await message.delete()
            else:
                await app.unpin_chat_message(
                    message.chat.id,
                    message.message_id
                )
            break
        except FloodWait as e:
            time.sleep(e.x)
        except ChatAdminRequired:
            pass


@Bot.on_message(filters.group & filters.new_chat_members)
async def kick(app: Bot, message: Message):
    while True:
        try:
            srv_msg = await app.kick_chat_member(
                message.chat.id,
                message.from_user.id,
                until_date=int(time.time()) + 60
            )
            await message.delete()
            await srv_msg.delete()
            break
        except FloodWait as e:
            time.sleep(e.x)
        except ChatAdminRequired:
            pass
