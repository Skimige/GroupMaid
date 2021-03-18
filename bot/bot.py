from configparser import ConfigParser
from pyrogram import Client
from . import __version__


class Bot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = f"{name}.ini"

        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root=f"{name}/plugins")
        super().__init__(
            session_name=name,
            app_version=f"GroupUnpinBot v{__version__}",
            workdir=".",
            config_file=config_file,
            workers=8,
            plugins=plugins,
        )

    async def start(self):
        await super().start()
        print(f"Bot v{__version__} started.")

    async def stop(self, block: bool = True):
        await super().stop(block)
        print("Bot has stopped. See you next time :)")
