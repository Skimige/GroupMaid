import time
from pyrogram.types import Message


def logger_chat(function: str, message: Message, plugin_message: str = 'triggered', is_print: bool = True):
    log = "{} | {} | Chat {} | Message {} | {}: {}.".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        "CHAT".ljust(6),
        str(message.chat.id).rjust(14),
        str(message.id).rjust(8),
        function,
        plugin_message)
    if is_print:
        print(log)
    return log


def logger_functions(function: str, plugin_message: str = "triggered", is_print: bool = True):
    log = "{} | {} | {} | {}.".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        "FUNC".ljust(6),
        function.ljust(16),
        plugin_message)
    if is_print:
        print(log)
    return log


def logger_plugins(function: str, message: Message, plugin_message: str = 'triggered', is_print: bool = True):
    log = "{} | {} | Chat {} | Message {} | Sender {} | {}: {}.".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        "PLUGIN".ljust(6),
        str(message.chat.id).rjust(14),
        str(message.id).rjust(8),
        str(message.from_user.id).rjust(10),
        function,
        plugin_message)
    if is_print:
        print(log)
    return log
