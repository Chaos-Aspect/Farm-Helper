import discord
import re
import time
from discord.ext import commands, tasks
from database import users
from resources import regex, settings


class ClaimCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.farm_claim_reminder.start()

    def cog_unload(self):
        self.farm_claim_reminder.cancel()
    
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
        if not msg.embeds: return

        embed = msg.embeds[0]
    
        if not embed.author: return

        userID = re.search(regex.userIDFromIconURL, embed.author.icon_url)
        userID = int(userID.group(1))

        if not (await users.getRow(userID)) or (await users.getRow(userID))[1] == 0: return

        if " — claim" in embed.author.name:
            await users.updateRow(userID, "last_claimed_farms", int(time.time()))
            await users.updateRow(userID,"reminder_channel", msg.channel.id)
            await users.updateRow(userID,"reminded_farm_claim",0)

    @commands.hybrid_command(description="Shows when you last claimed your farms.") 
    async def lastclaimed(self, ctx):
        if not (await users.getRow(ctx.author.id)) or (await users.getRow(ctx.author.id))[1] == 0: await ctx.send("You need to enable me first! </enable:1133914180064391189>"); return
        await ctx.send(f"**Last Claimed Farms**: <t:{(await users.getRow(ctx.author.id))[6]}:R>")
    
    @commands.command(aliases=["lc","lcl"])
    async def lastclaim(self,ctx):
        await self.lastclaimed(ctx)

    @tasks.loop(seconds=10.0)
    async def farm_claim_reminder(self):

        day_ago = int(time.time()) - (1 * 60 * 60) 

        cursor = settings.DB.cursor()
        cursor.execute(f"SELECT * FROM users WHERE last_claimed_farms <= {day_ago}")
        for i in cursor.fetchall():
            if i[1] == 0: continue
            if i[11] == 1: continue

            channel = self.bot.get_channel(i[5])
            await users.updateRow(i[0],"reminded_farm_claim",1)

            await channel.send(f"<@!{i[0]}>, it has been 24 hours since your last claim!\nYour farms are now capped and should be claimed ASAP.")
                
    @farm_claim_reminder.before_loop
    async def before_farm_claim_reminder(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ClaimCog(bot))
