from configparser import ConfigParser
from pyrogram import Client
from . import __version__


class Bot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = f"{name}.ini"

        config = ConfigParser()
        config.read(config_file, encoding='utf-8')

        if config['GroupMaid'].getint('admin') == 0:
            import sys
            print(f'Bot Admin User is not configured!\n'
                  f'Please edit "{config_file}" - [GroupMaid] section, '
                  f'and set "admin" to your Telegram ID, then start the bot again.')
            sys.exit(1)

        self.proxy_enabled = config.getboolean('proxy', 'enabled')
        if self.proxy_enabled:
            self.proxy = {
                'scheme': config.get('proxy', 'scheme'),
                'hostname': config.get('proxy', 'hostname'),
                'port': config.getint('proxy', 'port'),
                'username': config.get('proxy', 'username'),
                'password': config.get('proxy', 'password')
            }

        super().__init__(
            name=name,
            app_version=f"GroupMaid v{__version__}",
            workdir=".",
            api_id=config.getint('pyrogram', 'api_id'),
            api_hash=config.get('pyrogram', 'api_hash'),
            proxy=self.proxy if self.proxy_enabled else None,
            plugins={'root': f'{name}.plugins'},
            workers=8,
        )

    async def start(self):
        await super().start()
        print(f"Bot v{__version__} started.")

    async def stop(self, block: bool = True):
        await super().stop(block)
        print("Bot has stopped. See you next time :)")
