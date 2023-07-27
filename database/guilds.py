# users.py

# Access to the users table

import sqlite3
from resources import settings

async def getRow(guild_id):

    cursor = settings.DB.cursor()
    cursor.execute(f"SELECT * FROM guilds WHERE guild_id == ?", (guild_id,))
    row = cursor.fetchone()
    return row

async def updateRow(guild_id, column, value):
    
    cursor = settings.DB.cursor()
    cursor.execute(f"""UPDATE guilds
                   SET {column} = ?
                   WHERE guild_id == ?""", (value, guild_id))
    settings.DB.commit()
    return