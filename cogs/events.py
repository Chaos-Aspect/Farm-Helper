import discord
from discord.ext import commands
from database import guilds


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):


        if msg.author.id != 1085406806492319784: return
        if not msg.embeds: return

        embed = msg.embeds[0]

        if not embed.fields: return

        row = await guilds.getRow(msg.guild.id)

        if "Lucky reward!" in embed.fields[0].name:
            if row[3]:
                await msg.channel.send(f"<@&{row[3]}> Join")
            return

        if "Say OHMMM..." in embed.fields[0].name: # descript has players, fild got energy worht
            if row[1]:
                await msg.channel.send(f"<@&{row[1]}> OHMMM")
            return

        if "quatrillion of items need some packing!" in embed.fields[0].name:
            if row[2]:
                await msg.channel.send(f"<@&{row[2]}> Pack")
            return

async def setup(bot):
    await bot.add_cog(EventsCog(bot))
