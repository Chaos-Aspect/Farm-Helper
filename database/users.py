# users.py

# Access to the users table

import sqlite3
from resources import settings

async def getRow(user_id):

    cursor = settings.DB.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id == ?", (user_id,))
    row = cursor.fetchone()
    return row

async def updateRow(user_id, column, value):
    
    cursor = settings.DB.cursor()
    cursor.execute(f"""UPDATE users
                   SET {column} = ?
                   WHERE user_id == ?""", (value, user_id))
    settings.DB.commit()
    return