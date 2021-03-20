import json, getpass, vk_api
from vk_api.bot_longpoll import VkBotLongPoll

print("INFO: reading settings file...")

try:
    with open('/home/{}/.config/librespeak_bot/settings.json'.format(getpass.getuser()), 'r', encoding='utf-8') as f: 
        settings = json.load(f)
except Exception as error:
    print("ERROR: failed reading settings file")
    print(error)
    exit()

print("INFO: reading is successful!")

print("INFO: authentication...")
GROUP_ID = settings.get("ADMIN").get("GROUP_ID")
#Bot auth
try:

    vk_session = vk_api.VkApi(token=settings.get("BOT").get("BOT_TOKEN"))
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, settings.get("BOT").get("BOT_ID"))

    vk_sessionAdmin = vk_api.VkApi(token= settings.get("ADMIN").get("ADMIN_TOKEN"))
    vkAdmin = vk_sessionAdmin.get_api()
    print("INFO: authentication is successful!")

except Exception as error:
    print("ERROR: failed auth")
    print(error)


#vk.messages.send(peer_id=2000000001, message = "тест", random_id=0)
