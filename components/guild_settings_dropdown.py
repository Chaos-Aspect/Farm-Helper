# donor_dropdown.py

# Contains the donor tier dropdown and view

import discord
from cogs import energy
from database import guilds
from resources import emojis, messages, constants
from components import embeds

class RoleDropdown(discord.ui.RoleSelect):

    def __init__(self, placeholder, min_value, max_value, column_name):

        self.column_name = column_name

        super().__init__(placeholder=placeholder, min_values=min_value, max_values=max_value, custom_id=f"role_dropdown_{placeholder}")

    
    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

        await guilds.updateRow(interaction.guild.id,self.column_name,self.values[0].id)

        embed = await embeds.guild_settings_embed(interaction)
        
        await interaction.message.edit(embed=embed)

    
class GuildSettingsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

        self.add_item(RoleDropdown("Change OHMMM... Role",1,1,"ohmm_event_role_id"))
        self.add_item(RoleDropdown("Change Pack Role",1,1,"pack_event_role_id"))
        self.add_item(RoleDropdown("Change Lucky Reward",1,1,"lucky_reward_event_role_id"))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return False
        return True
    
    async def on_timeout(self):
        await self.message.edit(view=None)