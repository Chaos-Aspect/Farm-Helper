# dev.py

# Used to manage cogs.

from typing import Optional, Literal
from resources import settings, emojis

import discord
from discord.ext import commands
from discord import app_commands


class DevCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("Sync Complete")

    @commands.group(aliases=["cog"], invoke_without_command=True)
    @commands.is_owner()
    async def cogs(self, ctx: commands.Context):

        self.embed = discord.Embed(title="COGS",color=discord.Color.from_str(settings.EMBED_HEX))
        self.embed.description = "\n\n*Developer Command. Used to load, unload and reload cogs.*\n\n"
        
        loaded = []

        for i in self.bot.cogs:

            cog_check_string = str(self.bot.get_cog(i)).split(".")[1]

            loaded.append(f"cogs.{cog_check_string}")

        for i in self.bot.COGS:
            
            if i not in loaded:
                self.embed.description += f"`{i}` - {emojis.DISABLED}\n"
            else:
                self.embed.description += f"`{i}` - {emojis.ENABLED}\n"

        await ctx.send(embed=self.embed)

    @cogs.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        await self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Cog `{cog.capitalize()}` loaded.")
    
    @cogs.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        await self.bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Cog `{cog.capitalize()}` unloaded.")

    @cogs.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        await self.bot.unload_extension(f"cogs.{cog}")
        await self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Cog `{cog.capitalize()}` reloaded.")

    @load.error
    async def loadError(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.NotOwner):
            await ctx.send("You cannot run this command.")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Missing Argument")
        elif isinstance(error,commands.ExtensionNotFound):
            await ctx.send("Cog Not Found.")
        elif isinstance(error,commands.ExtensionAlreadyLoaded):
            await ctx.send("That cog is already loaded.")
        else:
            await ctx.send(f"Unexpected Error:\n```{error}```")

    @unload.error
    async def unloadError(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.NotOwner):
            await ctx.send("You cannot run this command.")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Missing Argument")
        elif isinstance(error,commands.ExtensionNotFound):
            await ctx.send("Cog Not Found.")
        elif isinstance(error,commands.ExtensionNotLoaded):
            await ctx.send("That cog is already unloaded.")
        else:
            await ctx.send(f"Unexpected Error:\n```{error}```")

    @reload.error
    async def reloadError(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error,commands.NotOwner):
            await ctx.send("You cannot run this command.")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Missing Argument")
        elif isinstance(error,commands.ExtensionNotFound):
            await ctx.send("Cog Not Found.")
        else:
            await ctx.send(f"Unexpected Error:\n```{error}```")


async def setup(bot):
    await bot.add_cog(DevCog(bot))
