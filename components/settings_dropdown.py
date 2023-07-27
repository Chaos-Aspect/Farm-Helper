# donor_dropdown.py

# Contains the donor tier dropdown and view

import discord
from cogs import energy
from database import users
from resources import emojis, messages, constants
from components import embeds

class DonatorDropdown(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(label="Non Donor", value=0),
            discord.SelectOption(label="Common Donator", emoji=emojis.COMMON_WORKER, value=1),
            discord.SelectOption(label="Talented Donator", emoji=emojis.TALENTED_WORKER, value=2),
            discord.SelectOption(label="Wise Donator", emoji=emojis.WISE_WORKER, value=3),
            discord.SelectOption(label="Expert Donator", emoji=emojis.EXPERT_WORKER, value=4),
            discord.SelectOption(label="Masterful Donator", emoji=emojis.MASTERFUL_WORKER, value=5),
        ]

        super().__init__(placeholder="Change Donor Tier", min_values=1, max_values=1, options=options, custom_id="donor_dropdown")

    
    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

        row = await users.getRow(interaction.user.id)

        if not row: await interaction.response.send_message(messages.BOT_NOT_ENABLED); return

        await users.updateRow(interaction.user.id,"donator_tier",self.values[0])

        embed = await embeds.settingsEmbed(interaction)
        
        await interaction.message.edit(embed=embed)

        await energy.EnergyCog.update_energy_regen_rate(interaction.user.id)

class EnergyRegenerationUpgradeDropdown(discord.ui.Select):

    def __init__(self):

        options = []

        for i in range(8):
            options.append(discord.SelectOption(label=f"Level {i}",value=i))  

        super().__init__(placeholder="Change Energy Regeneration Level", min_values=1, max_values=1, options=options, custom_id="energy_regeneration_upgrade_dropdown")

    
    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

        row = await users.getRow(interaction.user.id)

        if not row: await interaction.response.send_message(messages.BOT_NOT_ENABLED); return

        await users.updateRow(interaction.user.id,"energy_regeneration_upgrade",self.values[0])

        embed = await embeds.settingsEmbed(interaction)
        
        await interaction.message.edit(embed=embed)

        await energy.EnergyCog.update_energy_regen_rate(interaction.user.id)

class EnergyRegeneratedModeDropdown(discord.ui.Select):

    def __init__(self):

        options = [ ]

        for i in range(len(constants.ENERGY_REGENERATED_MODE_MESSAGES)):
            options.append(discord.SelectOption(label=constants.ENERGY_REGENERATED_MODE_MESSAGES[i],value=i))

        super().__init__(placeholder="Change Energy Notification Mode", min_values=1, max_values=1, options=options, custom_id="energy_regenerated_mode_dropdown")

    
    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

        row = await users.getRow(interaction.user.id)

        if not row: await interaction.response.send_message(messages.BOT_NOT_ENABLED); return

        await users.updateRow(interaction.user.id,"energy_regenerated_mode",self.values[0])

        embed = await embeds.settingsEmbed(interaction)
        
        await interaction.message.edit(embed=embed)
    
class SettingsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

        self.add_item(DonatorDropdown())
        self.add_item(EnergyRegenerationUpgradeDropdown())
        self.add_item(EnergyRegeneratedModeDropdown())

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return False
        return True
    
    async def on_timeout(self):
        await self.message.edit(view=None)