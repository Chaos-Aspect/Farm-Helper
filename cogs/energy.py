import discord
import re
import time
import math
from discord.ext import commands, tasks
from database import users
from resources import constants, regex, messages, settings


class EnergyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.energy_task.start()

    def cog_unload(self):
        self.energy_task.cancel()

    async def update_energy_regen_rate(id):
        row = await users.getRow(id)

        new_energy_rate = math.ceil(360/(constants.DONATOR_REDUCTIONS[row[2]]*constants.ENERGY_REGENERATION_UPGRADE_VALUES[row[3]]))

        await users.updateRow(id,"energy_regen_rate",new_energy_rate)

    @commands.hybrid_command(description="Displays your current energy")
    async def energy(self, ctx: commands.Context):

        row = await users.getRow(ctx.author.id)

        if not row or row[1] == 0: return

        await ctx.send(f"**Energy:** {row[7]}/{row[10]}")
    
    @commands.command(aliases=["e", "ce"])
    async def currentenergy(self,ctx: commands.Context):
        await self.energy(ctx)

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
        if embed.author:

            userID = re.search(regex.userIDFromIconURL, embed.author.icon_url)
            userID = int(userID.group(1))


            row = await users.getRow(userID)

            if not row or row[1] == 0: return

            if " — profile" in embed.author.name:
                energyBar = re.search(regex.GET_ENERGY_VALUES_FROM_PROFILE, embed.fields[0].value).group(1).split("/")
                await users.updateRow(userID,"energy",int(energyBar[0]))
                await users.updateRow(userID,"energy_max",int(energyBar[1]))
                await users.updateRow(userID,"reminder_channel", msg.channel.id)
                return

            if " — raid" in embed.author.name:

                await users.updateRow(userID,"energy",(row[7]-40))
                await users.updateRow(userID,"reminder_channel", msg.channel.id)

                await msg.channel.send(await messages.get_update_message(userID))
                if row[7] == row[10]:
                    await users.updateReminders(userID,"last_gained_energy", int(time.time()))
                return 
            
            if " — claim" in embed.author.name:
                await users.updateRow(userID,"energy",(row[7]-5))
                await users.updateRow(userID,"reminder_channel", msg.channel.id)

                await msg.channel.send(await messages.get_update_message(userID))
                if row[7] == row[10]:
                    await users.updateReminders(userID,"last_gained_energy", int(time.time()))
                return 
            
            if " — worker roll" in embed.author.name:
                await users.updateRow(userID,"energy",(row[7]-4))
                await users.updateRow(userID,"reminder_channel", msg.channel.id)

                await msg.channel.send(await messages.get_update_message(userID))

                if row[7] == row[10]:
                    await users.updateReminders(userID,"last_gained_energy", int(time.time()))
                return 
            
        elif "Everyone got **" in embed.fields[0].name and "** minutes worth of energy" in embed.fields[0].name:
                #name='Everyone got **12** minutes worth of energy'
                
                players = embed.description.replace("Players:","").replace(" ","").split(",")
                
                minutes_worth = int(re.search(regex.EXTRACT_INTEGERS, embed.fields[0].name).group(1))
                seconds_worth = minutes_worth * 60

                for i in players:
                    looped_user = msg.guild.get_member_named(i)
                    row = await users.getRow(looped_user.id)
                    
                    if not row or row[1] == 0: continue
                    energy_gained = seconds_worth//row[8]
                    remainder_seconds = seconds_worth % int(row[8])

                    await users.updateRow(looped_user.id,"energy",row[7]+energy_gained)
                    await users.updateRow(looped_user.id,"last_gained_energy",row[9]-remainder_seconds)
                    print(f"{looped_user.name} OHMMM Event. Added {energy_gained} Energy with excess {remainder_seconds} seconds ")


    @tasks.loop(seconds=10.0)
    async def energy_task(self):
        cursor = settings.DB.cursor()
        cursor.execute("SELECT * FROM users WHERE (strftime('%s', 'now') - last_gained_energy) >= energy_regen_rate")
        for i in cursor.fetchall():
            if i[1] == i[2]: print(f"Skipped {i[0]}, energy maxed."); continue
            print(f"Updated {i[0]}")

            await users.updateRow(i[0],"energy",(i[7]+1))
            await users.updateRow(i[0],"last_gained_energy",int(time.time()))

            channel = self.bot.get_channel(i[5])

            energySettings = i[4]

            if energySettings == 0:
                if (i[1]+1) == 4:
                    await channel.send(f"<@!{i[0]}>, `idle roll` is avaliable now!\n{await messages.get_update_message(i[0])}")
                if (i[1]+1) == 5:
                    await channel.send(f"<@!{i[0]}>, `idle claim` is avaliable now!\n{await messages.get_update_message(i[0])}")
                if (i[1]+1) == 40:
                    await channel.send(f"<@!{i[0]}>, `idle raid` is avaliable now!\n{await messages.get_update_message(i[0])}")
            
            elif energySettings == 1:
                await channel.send(f"<@!{i[0]}>, you gained 1 Energy.\n{await messages.get_update_message(i[0])}")
            
            elif energySettings == 2:
                if (i[1]+1) == i[2]:
                    await channel.send(f"<@!{i[0]}>, you are now at full energy!\n{await messages.get_update_message(i[0])}")

            else:
                print(f"Skipped notifying {i[0]}. EnergyPing: {energySettings}")
                continue
                
    @energy_task.before_loop
    async def before_energy_task(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(EnergyCog(bot))
