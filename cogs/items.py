import discord, re
from discord.ext import commands
from discord import app_commands
from resources import regex, messages
from database import users


class ItemsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, msg_before: discord.Message, msg_aft: discord.Message):
        if msg_before.pinned != msg_aft.pinned: return

        for i in msg_aft.components:
            for comp in i.children:
                if comp.disabled:
                    return
                
        await self.on_message(msg_aft)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id != 1085406806492319784: return
        if msg.embeds: return
        if "was recovered!" in msg.content:
            energyRecovered = re.search(regex.ENERGY_ITEM, msg.content)
            usernameRecovered = msg.content.replace("*","").split(" ")[0]
            userRecovered = msg.guild.get_member_named(usernameRecovered)

            row = await users.getRow(userRecovered.id)

            if not row or row[1] == 0: return
            userID = userRecovered.id

            if (row[7]+int(energyRecovered.group(1))) > row[10]:
                newEnergy = row[10]
            else:
                newEnergy = (row[7]+int(energyRecovered.group(1)))

            await users.updateRow(userID,"energy", newEnergy)
            await users.updateRow(userID,"reminder_channel", msg.channel.id)

            await msg.channel.send((await messages.get_update_message(userID)))

async def setup(bot):
    await bot.add_cog(ItemsCog(bot))
