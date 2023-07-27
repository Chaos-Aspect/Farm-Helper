# messages.py

# Contains various messages

from database import users

BOT_NOT_ENABLED = "You need to enable me first! </enable:1133914180064391189>"

FIRST_ENABLED_MESSAGE = "Hey! I'll begin helping you now!\nI highly recommend you check out my settings at </settings:1133957594726281337>."

ENABLE_MESSAGE = "Welcome back! I'll start helping you again."

DISABLE_MESSAGE = "I am now disabled. Hope to see you again!"

ALREADY_ENABLED = "I am already enabled...."

ALREADY_DISABLED = "I was already disabled."

async def get_update_message(userID):
    row = await users.getRow(userID)
    msg = f"**Energy:** {row[7]}/{row[10]}\n**Last Claimed Farms**: <t:{row[6]}:R>"
    if (row[1]) >= 4:
        msg += "\n**Avaliable Commands**\n:dizzy: `idle roll`"
    if (row[1]) >= 5:
        msg += "\n:dizzy: `idle claim`"
    if (row[1]) >= 40:
        msg += "\n:dizzy: `idle raid`"
    return msg