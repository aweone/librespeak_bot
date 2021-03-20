import toml, vk_api, os, sys
from vk_api.bot_longpoll import VkBotLongPoll

repo_path = os.path.dirname(__file__)

print("INFO: reading config file...")

try:
    with open(os.path.join(repo_path, "config.toml"), 'r', encoding='utf-8') as f: 
        config = toml.load(f)
except Exception as error:
    print(f"ERROR: failed reading {os.path.join(repo_path, 'config.toml')} file")
    print(error)
    exit(1)
    
print("INFO: config loaded successfully!")

print("INFO: authentication...")
GROUP_ID = config["user"]["id"]

try:
    vk_session = vk_api.VkApi(token=config["group"]["token"])
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, config["group"]["id"])
    vk_sessionAdmin = vk_api.VkApi(token=config["user"]["token"])
    vkAdmin = vk_sessionAdmin.get_api()
    print("INFO: authentication is successful!")

except Exception as error:
    print("ERROR: failed auth")
    print(error)
    exit(1)
