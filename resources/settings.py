# settings.py

# File with .env constants and connecting to the sqlite db

import sqlite3
import os
from dotenv import load_dotenv

DB = sqlite3.connect(r"database/db.sqlite")

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

EMBED_HEX = os.getenv("EMBED_HEX")