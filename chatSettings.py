import json
from pathlib import Path

with open(f'{Path.home()}/.config/librespeak_bot/chatSettings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)
