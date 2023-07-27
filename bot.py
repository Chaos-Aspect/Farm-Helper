# bot.py

# Main bot file.

import discord
from discord.ext import commands

from resources import settings

TEST_GUILD = 1066975743172689920

class MyBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("fh ","Fh ","FH ","fH "),
            intents=intents
        )

        self.COGS = [
            "cogs.dev",
            "cogs.register",
            "cogs.events",
            "cogs.settings",
            "cogs.claim",
            "cogs.energy",
            "cogs.items"
        ]

    async def setup_hook(self):

        for cogs in self.COGS:
            try:
                await self.load_extension(cogs)
            except:
                print(f"{cogs} not loaded.")
                raise

        self.tree.copy_global_to(guild=discord.Object(id=TEST_GUILD))

bot = MyBot()

bot.run(settings.BOT_TOKEN)