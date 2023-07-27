# register.py

# Allows the user to enable and disable the bot.

from typing import Optional, Literal
from resources import settings, emojis, messages
from database import users

import discord
from discord.ext import commands
from discord import app_commands

import time


class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["register"])
    async def on(self, ctx):
        await self.enable(ctx)

    @commands.hybrid_command(description="Enable Farm Helper")
    async def enable(self, ctx: commands.Context):

        row = await users.getRow(ctx.author.id)

        if row:
            if row[1] == 0:
                await users.updateRow(ctx.author.id,"bot_enabled",1)
                await ctx.reply(messages.ENABLE_MESSAGE)
            else:
                await ctx.reply(messages.ALREADY_ENABLED)
        else:
            cursor = settings.DB.cursor()

            cursor.execute("""
                INSERT INTO users (user_id, bot_enabled, donator_tier, energy_regeneration_upgrade, energy_regenerated_mode, reminder_channel, last_claimed_farms, energy, energy_regen_rate, last_gained_energy, energy_max, reminded_farm_claim) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (ctx.author.id, 1, 0, 0, 0, ctx.channel.id,0,0,360,int(time.time()),100,1))
            settings.DB.commit()

            await ctx.reply(messages.FIRST_ENABLED_MESSAGE)

    @commands.command(aliases=["unregister"])
    async def off(self, ctx):
        await self.disable(ctx)

    @commands.hybrid_command(description="Disable Farm Helper")
    async def disable(self, ctx: commands.Context):

        row = await users.getRow(ctx.author.id)

        if row:
            if row[1] == 1:
                await users.updateRow(ctx.author.id,"bot_enabled",0)
                await ctx.reply(messages.DISABLE_MESSAGE)
            else:
                await ctx.reply(messages.ALREADY_DISABLED)
        else:
            await ctx.reply(messages.ALREADY_DISABLED)

async def setup(bot):
    await bot.add_cog(RegisterCog(bot))
