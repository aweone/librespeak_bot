import json
import vk_api
import os
from pathlib import Path
from vk_api.bot_longpoll import VkBotLongPoll


print("INFO: authentication...")

GROUP_ID = os.getenv("BOT_ID")

vk_session = vk_api.VkApi(token=os.getenv("BOT_TOKEN"))
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

vkAdmin = vk_api.VkApi(token=os.getenv("ADMIN_TOKEN")).get_api()
print("INFO: authentication is successful!")

