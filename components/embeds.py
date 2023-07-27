# embed.py

# Contains embeds that need to be updated often

import discord
from discord.ext import commands
from resources import settings, constants
from database import users, guilds

# Settings
async def settingsEmbed(interaction: discord.Interaction) -> discord.Embed:

    row = await users.getRow(interaction.user.id)

    main_settings = (
        f"💫 **Donator Tier**: {constants.DONATOR_EMOJIS[row[2]]} `{constants.DONATOR_TIER[row[2]]}`\n" 
        f"💫 **Energy Regeneration Upgrade Level**: `{row[3]}`\n"
        f"💫 **Energy Notification Mode**: `{constants.ENERGY_REGENERATED_MODE_MESSAGES[row[4]]}`" 
    )

    embed = discord.Embed(color=discord.Color.from_str(settings.EMBED_HEX),title=f"{interaction.user.name.upper()}'S SETTINGS", description="\n\nGeneral Settings. More may be added in the future\n\n")

    embed.add_field(name="MAIN", value=main_settings,inline=False)

    return embed

# Guild Settingd
async def guild_settings_embed(interaction: discord.Interaction) -> discord.Embed:

    row = await guilds.getRow(interaction.guild.id)

    if row[1]:
        ohmmm = f"<@&{row[1]}>"
    else:
        ohmmm = "`None`"
    
    if row[2]:
        pack = f"<@&{row[2]}>"
    else:
        pack = "`None`"
    
    if row[3]:
        lucky = f"<@&{row[3]}>"
    else:
        lucky = "`None`"

    events_pings = (
        f"💫 **OHMMM...**: {ohmmm}\n" 
        f"💫 **Pack**: {pack}\n"
        f"💫 **Lucky Reward**: {lucky}" 
    )

    embed = discord.Embed(color=discord.Color.from_str(settings.EMBED_HEX),title=f"{interaction.guild.name}'S SETTINGS", description="\n\nEvent Ping Settings. More may be added in the future\n\n")

    embed.add_field(name="EVENTS PING", value=events_pings,inline=False)

    return embed