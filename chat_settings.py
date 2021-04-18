import json
from pathlib import Path

try:
    with open(f'chat_settings.json', 'r', encoding='utf-8') as f:
        settings = json.load(f)
except FileNotFoundError:
    settings = {}
