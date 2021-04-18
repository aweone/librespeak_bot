import json
import vk_api
import os
from pathlib import Path
from vk_api.bot_longpoll import VkBotLongPoll


print("INFO: authentication...")

with open("config/bot_config.json", "r") as f:
    data = json.load(f)

GROUP_ID = data["bot"]["id"]

vk_session = vk_api.VkApi(token=data["bot"]["token"])
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

vkAdmin = vk_api.VkApi(token=data["admin"]["token"]).get_api()
print("INFO: authentication is successful!")

