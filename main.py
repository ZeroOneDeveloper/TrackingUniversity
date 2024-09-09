from discord import Intents, Object, app_commands
from discord.ext.commands import Bot
from discord.ext.commands.errors import NoEntryPointError

import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class ControlSystem(Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            description="This is a bot that helps you to manage your server",
            intents=Intents.all(),
        )

    async def on_ready(self) -> None:
        for path, dirs, files in os.walk("extensions"):
            for file in files:
                if file.endswith(".py"):
                    try:
                        await self.load_extension(
                            f'{path.replace("/", ".")}.{file[:-3]}'
                        )
                        print(f'Loaded extension: {path.replace("/", ".")}.{file[:-3]}')
                    except NoEntryPointError:
                        print(
                            f'Failed to load extension: {path.replace("/", ".")}.{file[:-3]}'
                        )

        print(f"Logged in as {self.user} ({self.user.id})")


if __name__ == "__main__":
    bot = ControlSystem()
    bot.run(os.getenv("TOKEN"))
