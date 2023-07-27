import re

# User Info Extraction
userIDFromIconURL = re.compile(r"avatars\/(.+?)\/")
GET_ENERGY_VALUES_FROM_PROFILE = re.compile(r"\b(\d+/\d+)\b")
ENERGY_ITEM = re.compile(r":energy:\s+(\d+)")

# General Uti
EXTRACT_INTEGERS = re.compile(r'\b(\d+)\b')