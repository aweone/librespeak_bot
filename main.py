import vk_api, random, time, json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from auth import vk, longpoll, vkAdmin, GROUP_ID
from chatSettings import settings
from chatAdmin import get_admin
from captchaNew import get_captcha
from uptime import upTime
from pathlib import Path
from qrGen import qrgen
from qrDecode import qrdecode
from functionGraph import graph, graph3d
from helpMsg import helpmsg
from wiki import Wiki
from currency import exchangeRate
from cryptoCurrency import cryptocurrency
from abuse import insult
from githubapi import getGitHubAccInfo
#from uploadvk import upload
vk_api.VkApi.RPS_DELAY = 1/20

def rid(): return random.randint(-2147483647, 2147483647)

def message(text, attachment="", disable_mentions=1):
    vk.messages.send(
    peer_id=peer_id, 
    message=str(text), 
    random_id=rid(),
    attachment=attachment,
    disable_mentions=disable_mentions)


timeup=time.time()
ids_captcha={}
prefix = ["либребот","либра","вайфу", "/либребот", "/либра", "/вайфу", "/пинки", "пинки", "пинкипай", "/пинкипай"]
greetingMsg = ["привет", "приветик", "приф", "приф", "ку"]
howAreYou = ["как дела", "дела как", "как жизнь"]
ban = ["/ban", "!ban", "!бан", "/бан"]
whereAreYou = ["где ты", "ты где"]
chance = ["инфа", "вероятность", "шанс"]
developer = ["разраб", "разработчик", "создатель", "девелопер"]
think = ["я думаю, что ", "полагаю, ", "предполагаю, ", "я полагаю, что ", "мне кажется, ", "кажется что ", "я полагаю, что ", "я думаю, ", "думаю, что"]
who = ["у кого", "кто"]
need = ["нужно", "требуется", "необходимо", "надо"]
info = ["/help", "/помощь", "help", "помощь", "/хелп"]
funcgraph = ["funcgraph", "/funcgraph", "/fg", "fg"]
funcgraph3d = ["funcgraph3d", "/funcgraph3d", "/fg3d", "fg3d"]
while 1:
    try:
        for event in longpoll.listen():
            #print(event.object)
            if event.type == VkBotEventType.MESSAGE_NEW:
                startEterationTime = time.time()
                text = event.message.text
                user_id = event.message.from_id
                peer_id = event.message.peer_id
                if user_id == 213045391 and text:
                    if text == "/инф":
                        message(f"бот работает, аптайм {upTime(timeup)}")

                    elif text == "/капча":
                        captcha_value = get_captcha()
                        message(captcha_value[1], captcha_value[0])
                        
                    elif user_id == 213045391 and text.split()[0] == "/exec":
                        command = text.replace("/exec ", "")
                        exec(str(command))
                        print(command)

                if "action" in event.message.keys():

                    if (
                        event.message.action["type"] == "chat_invite_user_by_link"
                        and str(peer_id-2000000000) in settings
			and settings[str(peer_id - 2000000000)]["captcha_on"] == "True"
                    ):

                    
                        message(f"новый [id{event.message.from_id}|пользователь] присоединился по ссылке")

                        captcha_value = get_captcha()
                        message("пройдите капчу или кик", captcha_value[0])
                        if str(peer_id) not in ids_captcha.keys():
                            ids_captcha[str(peer_id)] = {}
                        ids_captcha[str(peer_id)][str(user_id)] = captcha_value[1]

                    elif (
                        event.message.action["type"] == "chat_kick_user"
                        and str(peer_id-2000000000) in settings
			and settings[str(peer_id - 2000000000)]["greeting_on"] == "True"
                    ):
                        message(f"еще один [id{event.message.action['member_id']}|хохол] покидает нас, ура!")

                    elif (
                        event.message.action["type"] == "chat_invite_user"
                        and str(peer_id-2000000000) in settings
			and settings[str(peer_id - 2000000000)]["greeting_on"] == "True"
                        and event.message.action["member_id"] != -202215029
                    ):
                        message(f"еще один [id{event.message.action['member_id']}|хохол] присоединился...")

                    elif (
                        event.message.action["type"] == "chat_invite_user"
                        and event.message.action["member_id"] == -202215029
                    ):
                        message("оу, меня добавили в новую беседу, генерю новый конфиг для беседы. хохлам приветик!;)")
                        settings[str(peer_id - 2000000000)] = {"captcha_on":"False", "casino_on":"True", "greeting_on":"True", "wife":"True", "qr":"True", "math": "True","rate":"True", "wiki":"True", "github":"True"}

                        with open(f'{Path.home()}/.config/librespeak_bot/chatSettings.json', 'w') as f:
                            json.dump(settings, f)

                elif (
                    str(peer_id) in ids_captcha
                    and str(user_id) in ids_captcha[str(peer_id)]
                    and text.lower() == ids_captcha[str(peer_id)][str(user_id)]
                ):

                    ids_captcha[str(peer_id)].pop(str(user_id))
                    message("проверка пройдена")
                
                elif (
                    str(peer_id) in ids_captcha
                    and str(user_id) in ids_captcha[str(peer_id)]
                    and text.lower() != ids_captcha[str(peer_id)][str(user_id)]
                ):

                    ids_captcha[str(peer_id)].pop(str(user_id))
                    message("пошел нахуй фурриеб")
                    vk.messages.removeChatUser(
                        chat_id = peer_id - 2000000000, 
                        user_id = user_id
                    )

                    if peer_id == 2000000001:
                        vkAdmin.groups.ban(
                            group_id = GROUP_ID,
                            owner_id = user_id
                        )
                if (
                    text
                    and text.split()[0] in info
                ):
                    message(helpmsg)
                if (
                    text
                    and text.split()[0].lower() == "помогите"
                ):
                    message("помогаю")
                

                if (
                    text 
                    and text.lower().split()[0] in prefix
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["wife"] == "True"
                    )
                ):
                    command = text.lower().split()[1:]    
                    if " ".join(command[:2]) == "" or command[0] in greetingMsg:
                        message(random.choice([
                                "Привет-привет))",
                                "Приветик;)",
                                "приф^-^",
                                "прив)",
                                "салютик ^_^",
                                "приф:3"
                                ]))
                                
                    if " ".join(command[:2]).replace("?","") in whereAreYou:
                        message(random.choice([
                                "туть)",
                                "здесь:3",
                                "тута(:",
                                "дома)",
                                "здеся ^_^"
                                ]))
                                
                    if " ".join(command[:2]).replace("?","") in howAreYou:
                        message(random.choice([
                                "хорошо)\nа у тебя? :3",
                                "отличненько:3",
                                "плохо, чувствую усталость((",
                                "только проснулась, отлично)",
                                "плохо.."
                                ]))
                    if " ".join(command[:1]) in chance:
                        message(f'вероятность "{" ".join(command[1:])}" {random.randint(1, 100)}%')
                    if " ".join(command[:1]) == "помоги":
                        message("помогаю")
                    if " ".join(command[:1]) == "выбери":  
                        try:
                            message(f'мне нравится больше {random.choice(command[1:])} ')
                        except Exception as error:
                            if str(error) == "list index out of range":
                                message('мне не из чего выбирать')
                            else:
                                message(f'ошибочка\n , команда "выбери" завершилась с ошибкой\n {error}')
                    
                    if " ".join(command[:1]) == "когда":
                        try:
                            date = time.gmtime(time.time() + random.randint(5000, 100000000))

                            message(f'{random.choice(think)} {date.tm_year}.{date.tm_mon}.{date.tm_mday} в {date.tm_hour}:{date.tm_min}:{date.tm_sec} {" ".join(command[1:])}')
                        except Exception as error:
                            message('ошибка!\nкоманда "когда" завершилась с ошибкой\n{error}')
                    if event.from_chat and " ".join(command[:1]) == "кто":
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id = peer_id,
                                group_id = GROUP_ID)["items"])["member_id"]
                            
                            usrname = vk.users.get(user_ids = randomUserId)[0]
                            firstName = usrname["first_name"]
                            lastName = usrname["last_name"]
                            message(f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {" ".join(command[1:])}', disable_mentions = 1)
                        
                        except Exception as error:
                            if str(error) == "[917] You don't have access to this chat":
                                message('у меня нет админки((\n не могу получить список участников')
                            else:
                                message(f'ошибочка\nкоманда "кто" завершилась с ошибкой\n {error}')
                                
                    if event.from_chat and " ".join(command[:2]) == "у кого":
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id = peer_id,
                                group_id = GROUP_ID)["items"])["member_id"]
                               
                            usrname = vk.users.get(user_ids = randomUserId, name_case = "gen")[0]
                            firstName = usrname["first_name"]
                            lastName = usrname["last_name"]
                            message(f'{random.choice(think)} у [id{randomUserId}|{firstName} {lastName}] {" ".join(command[2:])}', disable_mentions = 1)
                        
                        except Exception as error:
                            if str(error) == "[917] You don't have access to this chat":
                                message('у меня нет админки((\n не могу получить список участников')
                            else:
                                message(f'ошибочка\nкоманда "у кого" завершилась с ошибкой\n {error}')
                                
                    if event.from_chat and " ".join(command[:1]) == "кому":
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id = peer_id,
                                group_id = GROUP_ID)["items"])["member_id"]
                            
                            usrname = vk.users.get(user_ids = randomUserId, name_case = "dat")[0]
                            firstName = usrname["first_name"]
                            lastName = usrname["last_name"]
                            message(f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {random.choice(need)} {" ".join(command[1:])}', disable_mentions = 1)
                        
                        except Exception as error:
                            if str(error) == "[917] You don't have access to this chat":
                                message('у меня нет админки((\n не могу получить список участников')
                            else:
                                message(f'ошибочка\nкоманда "кому" завершилась с ошибкой\n {error}')
                if (
                    text
                    and text.split()[0] in funcgraph
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["math"] == "True"
                    )
                ):  
                    try:
                        message(f"ваш график:", attachment = graph(" ".join(text.split()[1:])))
                    except Exception as error:
                        print(error)
                        message(f"ошибка\n{error}")
                if (
                    text
                    and text.split()[0] in funcgraph3d
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["math"] == "True"
                    )
                ):
                    try:
                        message(f"ваш график:", attachment = graph3d(" ".join(text.split()[1:])))
                    except Exception as error:
                        print(error)
                        message(f"ошибка\n{error}")

                if (
                    text
                    and event.message.attachments
                    and text[:5] == "/scan"
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["qr"] == "True"
                    )
                ):
                    for attachment in event.message.attachments:
                        if attachment["type"] == "photo":
                            causeEnd = ""
                            maxSize = 0
                            for size in attachment["photo"]["sizes"]:
                                if size["height"] > maxSize:
                                    maxsize = size["height"]
                            text = qrdecode(size["url"])

                            if text:
                                message(f"расшифровка успешна\n\"{text}\"")
                                causeEnd = "DECODE_SUSCS"
                                break
                            elif not text:
                                message("расшифровка неудачна\nпроверьте качество картикнки и наличие qr-кода...")
                                causeEnd = "BAD_QUALITY"
                                break
                        else:
                            message("прикрепите к сообщению ФОТО.")
                            break
                    continue                
                if (
                    text
                    and text[:3] == "/qr"
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["qr"] == "True"
                    )
                ):
                    try:
                        message("ваш qrcode",attachment=qrgen(text[4:]))
                    except Exception as error:
                        message(f'ошибка!\nкоманда "qr" завершилась с ошибкой\n{error}')
                if (
                    text
                    and text.startswith("/github")
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["github"] == "True"
                    )
                ):
                    message(getGitHubAccInfo(text.split()[1]))
                if (
                    text
                    and text.startswith("/wiki")
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["wiki"] == "True"
                    )
                ):
                    if text.split()[-1].isdigit():
                        message(Wiki(text[5:].replace(text.split()[-1], ""), int(text.split()[-1])))
                    else:
                        message(Wiki(text[5:]))
                if (
                    text
                    and text.startswith("/курс")
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["rate"] == "True"
                    )
                ):
                    if len(text.split()) > 1 and text.split()[1] == "-евро":
                        rate = exchangeRate("EUR").value
                        message(f"Курс евро {rate} руб.")
                    elif len(text.split()) > 1 and text.split()[1] == "-доллар":
                        rate = exchangeRate("USD").value
                        message(f"Курс доллара {rate} руб.")
                    else:
                        rateUSD = exchangeRate("USD").value
                        rateEUR = exchangeRate("EUR").value
                        message(f"Курс Доллара США {rateUSD} руб, курс Евро {rateEUR} руб.")
                if (
                    text
                    and text.startswith("/криптокурс")
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["rate"] == "True"
                    )
                ):
                    message(f"Курс четырех популярных криптовалют:\n{cryptocurrency()}")

                if (
                    text
                    and text == "/оск"
                ):
                    message(insult())
                if (
                    text
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["casino_on"] == "True"
                    )
                ):

                    if text.split()[0] == "/казино":

                        with open(f'{Path.home()}/.config/librespeak_bot/casino.json') as f:
                            casino = json.load(f)

                        gain = 0
                        rate = 0

                        if str(user_id) not in casino:
                            casino[str(user_id)] = "1000"

                        if ( 
                            int(text.split()[1]) <= 0 
                            or not text.split()[1].isdigit()
                        ):
                            message("нормальную ставку сделай, кловн")
                            continue

                        balance = int(casino[str(user_id)])
                        rate = int(text.split()[1])
                        
                        a = random.randint(1, 9)
                        b = random.randint(1, 9)
                        c = random.randint(1, 9)

                        if balance < rate:
                            message("лох, денег нет")
                            
                        else:
                            message(f"{a} | {b} | {c}")
                            if a == b == c:
                                gain = rate * (a + b + c)
                                message(f"ого, сорвал куш, выиргрыш {gain} руб")
                                casino[str(user_id)] = str(balance + gain)

                            elif a == b or b == c or a == c:
                                gain = rate * random.choice([a, b, c])
                                message(f"о, ты выиграл, твой выигрыш {gain} руб")
                                casino[str(user_id)] = str(balance + gain)

                            else:
                                balance = balance - rate
                                message(f"ахахаха, лох, проиграл, твой баланс {balance} руб")
                                casino[str(user_id)] = str(balance)

                            with open(f'{Path.home()}/.config/librespeak_bot/casino.json', "w") as f:
                                json.dump(casino, f)

                    if text.split()[0] == "/баланс":

                        with open(f'{Path.home()}/.config/librespeak_bot/casino.json') as f:
                            casino = json.load(f)

                        if str(user_id) not in casino:
                            casino[str(user_id)] = "100"
                        
                        message(f"твой баланс {casino[str(user_id)]} руб")

                if text == "/admins":
                    try:
                        admins = ""
                        if vk.users.get(user_ids = get_admin(peer_id, GROUP_ID)[1]) == []:
                            message("у меня нет админки\nне могу узнать админов данного чата...")
                            continue

                        for admin in vk.users.get(user_ids=get_admin(peer_id, GROUP_ID)[1]):
                            userrId = admin["id"]
                            userFirstName = admin["first_name"]
                            userLastName = admin["last_name"]
                            admins += f"[id{ userrId }|{ userFirstName } { userLastName }]\n"

                        message("админы данного чата:\n" + admins, disable_mentions=1)
                    except:
                        message("не могу узнать админов данного чата...")

                if (
                    event.message.attachments
                    and event.object["message"]["attachments"][0]["type"] == "audio_message"
                    and random.choices([True, False], weights = (25, 75), k=2)[0]
                ):
                    message("хрю-хрю")
                    
                if (
                    "навальный" in text.lower()
                    and random.choices([True, False], weights = (25, 75), k = 2)[0]
                ):
                    message("", "photo-202215029_457239052")

                if (
                    text
                    and text.split()[0].lower() in ban
                    and user_id not in get_admin(peer_id, GROUP_ID)[1]
                ):
                    message("угомонись, хохлинка... кикать могут только админы")
                    
                if user_id in get_admin(peer_id, GROUP_ID)[1] or user_id == 213045391:

                    if text and text.split()[0].lower() in ban:
                        if "reply_message" in event.message.keys() or event.message.fwd_messages:
                            if "reply_message" in event.message:
                                user_id = event.message.reply_message["from_id"]

                                message("кикаю хохлинку...")
                                try:
                                    vk.messages.removeChatUser(
                                        chat_id = peer_id - 2000000000, 
                                        user_id = user_id
                                    )
                                except Exception as error:
                                    print(error)
                                    if str(error) == "[935] User not found in chat":
                                        message("мань, такого юзера нет в чате...")
                                    elif str(error) == "[15] Access denied: can't remove this user":
                                        message("зачем ты другого админа забанить хочешь?")
                                    else:                                     
                                        message(f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}")

                            elif event.message.fwd_messages:

                                if len(event.message.fwd_messages) > 1:
                                    message("начинаю массовый кик хохлов")

                                for fwd_msg in event.message.fwd_messages:

                                    message("кикаю хохлинку...")
                                    try:
                                        vk.messages.removeChatUser(
                                            chat_id = peer_id - 2000000000, 
                                            user_id = fwd_msg["from_id"]
                                        )
                                    except Exception as error:
                                        print(error)
                                    if str(error) == "[935] User not found in chat":
                                        message("мань, такого юзера нет в чате...")
                                    elif str(error) == "[15] Access denied: can't remove this user":
                                        message("зачем ты другого админа забанить хочешь?")
                                    else:                                     
                                        message(f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}")
                                
                        else:
                            banList = text[4:]
                            
                            for banPrifix in ban:
                                banList.replace(banPrifix, "")

                            if len(banList.split()) > 1:
                                message("начинаю массовый кик хохлов...")
                            else:
                                message("кикаю хохлинку...")
                            
                            for screen_name in banList.split():
                                user_id = ""
                                if screen_name == "[club202215029|@librebot]":
                                    message("ты што, хочешь забанить такую тяночку как я???")
                                    continue

                                for char in screen_name.replace("[id", ""):
                                    print(screen_name)
                                    if char.isdigit():
                                        user_id += char
                                    else:
                                        break
                                if user_id == "":
                                    continue
                                    
                                try:
                                    vk.messages.removeChatUser(
                                        chat_id = peer_id - 2000000000, 
                                        user_id = user_id
                                    )
                                except Exception as error:
                                    print(error)
                                    if str(error) == "[935] User not found in chat":
                                        message("мань, такого юзера нет в чате...")
                                    elif str(error) == "[15] Access denied: can't remove this user":
                                        message("зачем ты другого админа забанить хочешь?")
                                    else:                                     
                                        message(f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}")


                    elif text == "/settings":
                        settingsStr = ""
                        
                        for value, param in settings.get(str(event.message.peer_id - 2000000000)).items():
                            settingsStr+=f"{value}   =>   {param}\n"
                        
                        message(f"Текущие настройки: \n{settingsStr}")
                        
                    elif text and text.split()[0] == "/set":

                        params = text.replace("/set", "").split()
                        
                        if params[0] in settings.get(str(peer_id - 2000000000)) and (params[1] == "True" or params[1] == "False"):
                            settings[str((peer_id - 2000000000))].update({params[0]:params[1]})
                            with open(f'{Path.home()}/.config/librespeak_bot/chatSettings.json', 'w') as f:
                                json.dump(settings, f)
                            message(f'изменение параметра \"{params[0]}\"\nтекущее значение \"{params[1]}\"')
                        
                        elif params[0] not in settings.get(str(peer_id - 2000000000)):
                            message(f'параметра \"{params[0]}\" не существует!')
                        
                        elif params[1] != "True" or params[1] != "False":
                            message(f'значение \"{params[1]}\" для параметра \"{params[0]}\" невозможно!\nTrue или False')

                    elif text == "/setToDefault":
                        settings[str(peer_id - 2000000000)] = {"captcha_on":"False", "casino_on":"True", "greeting_on":"True", "wife":"True", "qr":"True", "math": "True","rate":"True", "wiki":"True", "github":"True"}
                        
                        with open(f'{Path.home()}/.config/librespeak_bot/chatSettings.json', 'w') as f:
                            json.dump(settings, f)
                        settingsStr = ""
                        
                        for value, param in settings.get(str(event.message.peer_id - 2000000000)).items():
                            settingsStr+=f"{value}   =>   {param}\n"
                        message(f"Настройки были успешно сброшены.\nТекущие настройки: \n{settingsStr}")
                
                if text == "/тест":
                    message(f"время ответа: {time.time() - startEterationTime}\nаптайм: {upTime(timeup)}")
    except Exception as error:
        print(error)
