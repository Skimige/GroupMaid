import os
import re
import json
import time
from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions import ChannelInvalid

from ..bot import Bot
from ..utils.help_text import error_message_generator, help_text_all
from ..utils.helpers import logger_plugins


with open(os.path.join('bot', 'conf', 'config.json'), 'r', -1, 'utf_8') as config_fp:
    config = json.load(config_fp)

default_config = {
    'kick': False,
    'unpin': False,
    'ban_channel_message': False
}

for i in config['groups']:
    for j in default_config:
        if j not in config['groups'][i]:
            config['groups'][i][j] = default_config[j]


@Bot.on_message(filters.chat(config['admin']) & filters.user(config['admin']) & filters.command('help'))
async def print_help(app: Bot, message: Message):
    await message.reply_text(help_text_all, parse_mode='md')


@Bot.on_message(filters.chat(config['admin']) & filters.user(config['admin']) & filters.command('status'))
async def status(app: Bot, message: Message):
    status_text = ''
    for i in config['groups']:
        if i != '0':
            status_text += f'**{i}** | {(await app.get_chat(i)).title}\n' \
                           f'自动踢人: {config["groups"][i]["kick"]}, ' \
                           f'解除置顶: {config["groups"][i]["unpin"]}, ' \
                           f'禁止频道消息: {config["groups"][i]["ban_channel_message"]}\n'
    await message.reply_text(
        text='已添加的群组：\n\n' + status_text,
        parse_mode='md'
    )
    logger_plugins('status', message)


@Bot.on_message(filters.chat(config['admin']) & filters.user(config['admin']) & filters.command('req'))
async def req(app: Bot, message: Message):
    if len(message.command) != 2:
        await message.reply_text(error_message_generator('req'), parse_mode='md')
    else:
        chat_id = int(message.command[1])
        try:
            bot_chat = await app.get_chat(chat_id)
        except ChannelInvalid:
            await message.reply_text('请先将 Bot 添加到对应群组。', reply_to_message_id=message.message_id)
            logger_plugins('req', message, f'Bot is not in the target group {chat_id}')
            return
        with BytesIO(str.encode(str(bot_chat))) as result_doc:
            now = int(time.time())
            result_doc.name = f'{chat_id}_{now}.log'
            await message.reply_document(
                document=result_doc,
                caption=f'Data of **{chat_id}**\nGenerated at {now}'
            )
        logger_plugins('req', message)


@Bot.on_message(filters.chat(config['admin']) & filters.user(config['admin']) & filters.command('add_group'))
async def add_group(app: Bot, message: Message):
    if len(message.command) != 2:
        await message.reply_text(error_message_generator('add_group'), parse_mode='md')
    else:
        chat_id = int(message.command[1])
        try:
            bot_member = await app.get_chat_member(chat_id, 'me')
        except ChannelInvalid:
            await message.reply_text('请先将 bot 添加到对应群组。', reply_to_message_id=message.message_id)
            logger_plugins('add_group', message, f'Bot is not in the target group {chat_id}')
            return
        if bot_member.can_pin_messages and bot_member.can_delete_messages and bot_member.can_restrict_members:
            config['groups'][str(chat_id)] = {'kick': False, 'unpin': False, 'ban_channel_message': False}
            with open(os.path.join('bot', 'conf', 'config.json'), 'w', -1, 'utf_8') as config_fp_save:
                json.dump(config, config_fp_save)
            await message.reply_text(
                text=f'已添加群组 **{chat_id}**\n默认未启用功能，请对其配置。',
                reply_to_message_id=message.message_id
            )
            logger_plugins('add_group', message, f'added group {chat_id}')
        else:
            await message.reply_text(
                text='请授予 Bot 以下必要权限后再试：\n删除消息、封禁用户、置顶消息。',
                reply_to_message_id=message.message_id
            )
            logger_plugins('add_group', message, f'missing permission(s) in group {chat_id}')


@Bot.on_message(filters.chat(config['admin']) & filters.user(config['admin']) & filters.command('remove_group'))
async def remove_group(app: Bot, message: Message):
    if len(message.command) != 2:
        await message.reply_text(error_message_generator('remove_group'), parse_mode='md')
    else:
        chat_id = int(message.command[1])
        try:
            del config['groups'][str(chat_id)]
        except KeyError:
            await message.reply_text('ID 有误或未添加。')
            return
        with open(os.path.join('bot', 'conf', 'config.json'), 'w', -1, 'utf_8') as config_fp_save:
            json.dump(config, config_fp_save)
        await message.reply_text(
            text=f'已移除群组 **{chat_id}**',
            reply_to_message_id=message.message_id
        )
        logger_plugins('remove_group', message, f'removed group {chat_id}')


@Bot.on_message(filters.chat(config['admin']) & filters.user(config['admin']) & filters.command('config_group'))
async def config_group(app: Bot, message: Message):
    if len(message.command) != 2:
        await message.reply_text(error_message_generator('config_group'), parse_mode='md')
    else:
        chat_id = int(message.command[1])
        if str(chat_id) in config['groups']:
            bot_chat = await app.get_chat(chat_id)
            button_reverse_kick = \
                InlineKeyboardButton('修改「自动踢人」状态', f'reverse_kick_{chat_id}')
            button_reverse_unpin = \
                InlineKeyboardButton('修改「解除置顶」状态', f'reverse_unpin_{chat_id}')
            button_reverse_ban_channel_message = \
                InlineKeyboardButton('修改「禁止频道消息」状态', f'reverse_ban_channel_message_{chat_id}')
            await message.reply_text(
                text=f'**{chat_id}** | {bot_chat.title}\n\n'
                     f'「自动踢人」: {config["groups"][str(chat_id)]["kick"]}\n'
                     f'「解除置顶」: {config["groups"][str(chat_id)]["unpin"]}\n'
                     f'「禁止频道消息」: {config["groups"][str(chat_id)]["ban_channel_message"]}',
                reply_to_message_id=message.message_id,
                reply_markup=InlineKeyboardMarkup(
                    [[button_reverse_kick], [button_reverse_unpin], [button_reverse_ban_channel_message]]
                )
            )
        else:
            await message.reply_text(
                text=f'请先使用 /add_group {chat_id} 添加群组后再配置。',
                reply_to_message_id=message.message_id
            )
            logger_plugins('config_group', message, f'group {chat_id} is not added yet')


callback_regex = r'reverse_(kick|unpin|ban_channel_message)_([0-9-]*?)$'


@Bot.on_callback_query(filters.user(config['admin']) & filters.regex(callback_regex))
async def config_group_callback(app: Bot, callback: CallbackQuery):
    message = callback.message
    data = re.findall(callback_regex, callback.data)
    config['groups'][data[0][1]][data[0][0]] = not config['groups'][data[0][1]][data[0][0]]
    with open(os.path.join('bot', 'conf', 'config.json'), 'w', -1, 'utf_8') as config_fp_save:
        json.dump(config, config_fp_save)

    bot_chat = await app.get_chat(int(data[0][1]))
    await message.edit_text(
        text=f'**{data[0][1]}** | {bot_chat.title}\n\n'
             f'「自动踢人」: {config["groups"][str(data[0][1])]["kick"]}\n'
             f'「解除置顶」: {config["groups"][str(data[0][1])]["unpin"]}\n'
             f'「禁止频道消息」: {config["groups"][str(data[0][1])]["ban_channel_message"]}',
        reply_markup=message.reply_markup
    )
    await app.answer_callback_query(callback.id, f'已设置 {data[0][1]} 的 {data[0][0]} '
                                                 f'为 {config["groups"][data[0][1]][data[0][0]]}')
    logger_plugins('config_group_callback', message,
                   f'config {data[0][1]} -> {data[0][0]}: {config["groups"][data[0][1]][data[0][0]]}')


@Bot.on_message(filters.chat(config['admin']) & filters.user(config['admin']) & filters.command('raw_config'))
async def read_raw_config(app: Bot, message: Message):
    with open(os.path.join('bot', 'conf', 'config.json'), 'r', -1, 'utf_8') as temp_fp:
        temp = json.load(temp_fp)
    await message.reply_text('Current config in memory:\n```' + str(config) +
                             '```\nCurrent config in file:\n```' + str(temp) + '```')
