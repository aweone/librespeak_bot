import cryptocompare
import json
from pathlib import Path

with open(f'{Path.home()}/.config/librespeak_bot/cryptoSettings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)
cryptocompare.cryptocompare._set_api_key_parameter(settings["token"])


def cryptocurrency():
    (cryptocompare.get_price(["BTC", "LTC", "XMR", "ETH"], ["USD", "RUB"]))
    msg = ""
    for cc, value in cryptocompare.get_price(["BTC", "LTC", "XMR", "ETH"], ["USD", "RUB"]).items():
        # print(a, b)
        USD = value["USD"]
        RUB = value["RUB"]
        msg += f"{cc} {USD} дол. ({RUB} руб.)\n"
    return msg

# wprint(cryptocurrency())
