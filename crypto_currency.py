import cryptocompare
import json
from pathlib import Path

try:
    with open(f'crypto_settings.json', 'r', encoding='utf-8') as f:
        settings = json.load(f)
    cryptocompare.cryptocompare._set_api_key_parameter(settings["token"])
except FileNotFoundError:
    print("WARNING: Токен для модуля crypto_currency не указан")



def cryptocurrency():
    (cryptocompare.get_price(["BTC", "LTC", "XMR", "ETH"], ["USD", "RUB"]))
    msg = ""
    for cc, value in cryptocompare.get_price(["BTC", "LTC", "XMR", "ETH"], ["USD", "RUB"]).items():
        USD = value["USD"]
        RUB = value["RUB"]
        msg += f"{cc} {USD} дол. ({RUB} руб.)\n"
    return msg
