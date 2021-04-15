import json
import vk_api
from pathlib import Path
from vk_api.bot_longpoll import VkBotLongPoll

print("INFO: reading settings file...")


try:
    print("INFO: check settings file...")
    with open(f'{Path.home()}/.config/librespeak_bot/settings.json', 'r', encoding='utf-8') as f:
        settings = json.load(f)
except Exception as error:
    print("ERROR: failed reading settings file...")
    print(error)
    input()
    exit(1)

print("INFO: reading is successful!")

print("INFO: authentication...")
GROUP_ID = settings["ADMIN"]["GROUP_ID"]
# Bot auth
try:

    vk_session = vk_api.VkApi(token=settings.get("BOT").get("BOT_TOKEN"))
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, settings.get("BOT").get("BOT_ID"))

    vkAdmin = vk_api.VkApi(token=settings.get(
        "ADMIN").get("ADMIN_TOKEN")).get_api()
    print("INFO: authentication is successful!")

except Exception as error:
    print("ERROR: failed auth")
    print(error)


# vk.messages.send(peer_id=2000000001, message = "тест", random_id=0)
