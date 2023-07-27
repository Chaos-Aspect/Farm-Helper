import discord
from discord.ext import commands
from discord import app_commands
from components import embeds, settings_dropdown, guild_settings_dropdown
from database import users, guilds
from resources import settings


class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Change your settings here.")
    async def settings(self, interaction: discord.Interaction):
        embed = await embeds.settingsEmbed(interaction)
        await interaction.response.defer()
        view = settings_dropdown.SettingsView()
        view.user = interaction.user
        view.message = await interaction.followup.send(embed=embed, view=view)
        
        await users.updateRow(interaction.user.id,"reminder_channel",interaction.channel.id)

    @commands.command(aliases=["config","set","settings"])
    async def setting(self, ctx):
        await ctx.send(f"Please use </settings:1133957594726281337> to modify your settings.")

    @app_commands.command(description="Change the server settings here.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def serversettings(self, interaction: discord.Interaction):
        if not (await guilds.getRow(interaction.guild.id)): 
            cursor = settings.DB.cursor()
            cursor.execute("""
                INSERT INTO guilds (guild_id, ohmm_event_role_id, pack_event_role_id, lucky_reward_event_role_id) VALUES (?,?,?,?)
            """, (interaction.guild.id))
            
        embed = await embeds.guild_settings_embed(interaction)
        await interaction.response.defer()
        view = guild_settings_dropdown.GuildSettingsView()
        view.user = interaction.user
        view.message = await interaction.followup.send(embed=embed, view=view)
        
        await users.updateRow(interaction.user.id,"reminder_channel",interaction.channel.id)

    @commands.command(aliases=["serverconfig","serverset","serversettings"])
    async def serversetting(self, ctx):
        await ctx.send(f"Please use </settings:1134230857289322607> to modify the server settings.")

    @serversettings.error
    async def server_settings_error(self, interaction: discord.Interaction, error):
        error = getattr(error, "original", error)
        if isinstance(error,app_commands.MissingPermissions):
            await interaction.response.send_message("You need `MANAGE_SERVER` to use this command.")

async def setup(bot):
    await bot.add_cog(SettingsCog(bot))
