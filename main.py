import vk_api, random, time, json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from auth import vk, longpoll, vkAdmin, GROUP_ID
from chatSettings import settings
from chatAdmin import get_admin
from captchaNew import get_captcha
from uptime import upTime

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

while 1:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if (
                        event.object["message"]["from_id"] == 213045391 and
                        event.object["message"]["text"] != ""
                    ):


                        if (
                            event.object["message"]["text"] == "/инф"
                        ):

                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = "бот работает, аптайм "+upTime(timeup), 
                                random_id = random.randint(1,999999)
                            )


                        elif (
                            event.object["message"]["text"] == "/капча"
                        ):
                            
                            captcha_value = get_captcha()
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = captcha_value[1], 
                                random_id = random.randint(1,999999), 
                                attachment = captcha_value[0]
                            )
                        elif (
                            event.object["message"]["from_id"] == 213045391 and
                            event.object["message"]["text"].split()[0] == "/exec"
                        ):

                            command = event.object["message"]["text"].replace("/exec ", "")
                            exec(str(command))
                            print(command)

                if (
                    "action" in event.object["message"]
                ):

                    if (
                        event.object["message"]["action"]["type"] == "chat_invite_user_by_link"
                        and (settings.get(str(event.object["message"]["peer_id"] - 2000000000)).get("captcha_on")) == "True"
                    ):

                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = ("новый [id" + str(event.object["message"]["from_id"]) + "|пользователь] присоединился по ссылке"), 
                            random_id = random.randint(1,999999)
                        )

                        captcha_value = get_captcha()
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = "пройдите капчу или кик", 
                            random_id = random.randint(1,999999), 
                            attachment = captcha_value[0]
                        )
                        ids_captcha[str(event.object["message"]["from_id"])] = captcha_value[1]

                    elif (
                        event.object["message"]["action"]["type"] == "chat_kick_user"
                        and (settings.get(str(event.object["message"]["peer_id"] - 2000000000)).get("greeting_on")) == "True"
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = "еще один [id"+str(event.object["message"]["action"]["member_id"])+"|хохол] покидает нас, ура!", 
                            random_id = random.randint(1,999999)
                        )

                    elif (
                        event.object["message"]["action"]["type"] == "chat_invite_user"
                        and event.object["message"]["action"]["member_id"] != -202215029
                        and (settings.get(str(event.object["message"]["peer_id"] - 2000000000)).get("greeting_on")) == "True"
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = "еще один [id"+str(event.object["message"]["action"]["member_id"])+"|хохол] присоединился...", 
                            random_id = random.randint(1,999999)
                        )

                    elif (
                        event.object["message"]["action"]["type"] == "chat_invite_user"
                        and event.object["message"]["action"]["member_id"] == -202215029
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = "оу, меня добавили в новую беседу, генерю новый конфиг для беседы. хохлам приветик!;)", 
                            random_id = random.randint(1,999999)
                        )
                        settings[str(event.object["message"]["peer_id"] - 2000000000)] = {"captcha_on":"True", "casino_on":"False", "greeting_on":"False", "wife":"True"}
                        with open('settings.json', 'w') as f:
                            json.dump(settings, f)

                elif (
                    str(event.object["message"]["from_id"]) in ids_captcha and
                    event.object["message"]["text"].lower() == ids_captcha[str(event.object["message"]["from_id"])]
                ):

                    ids_captcha.pop(str(event.object["message"]["from_id"]))
                    vk.messages.send(
                        peer_id = event.object["message"]["peer_id"], 
                        message = "проверка пройдена", 
                        random_id = random.randint(1,999999)
                    )
                
                elif (
                    str(event.object["message"]["from_id"]) in ids_captcha
                    and event.object["message"]["text"] != ids_captcha[str(event.object["message"]["from_id"])]
                ):

                    ids_captcha.pop(str(event.object["message"]["from_id"]))

                    vk.messages.send(
                        peer_id = event.object["message"]["peer_id"], 
                        message = "пошел нахуй фурриеб", 
                        random_id = random.randint(1,999999)
                    )

                    vk.messages.removeChatUser(
                        chat_id = event.object["message"]["peer_id"]-2000000000, 
                        user_id = event.object["message"]["from_id"]
                    )

                    if event["message"]["peer_id"] == 2000000001:
                        vkAdmin.groups.ban(
                            group_id = GROUP_ID,
                            owner_id = event.object["message"]["from_id"]
                        )

                if (
                    event.message.text
                    and event.message.text.lower().split()[0] in prefix
                    and (
                        event.from_user
                        or str(event.object["message"]["peer_id"] - 2000000000) in settings
                        and settings[str(event.object["message"]["peer_id"] - 2000000000)]["wife"] == "True"
                    )
                ):
                    command = event.message.text.lower().split()[1:]
                    #print(event.message.text    
                    if (
                        " ".join(command[:2]) == ""
                        or command[0] in greetingMsg
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = random.choice([
                                "Привет-привет))",
                                "Приветик;)",
                                "приф^-^",
                                "прив)",
                                "салютик ^_^",
                                "приф:3"
                                ]), 
                            random_id = random.randint(1,999999)
                        )
                    if (
                        " ".join(command[:2]).replace("?","") in whereAreYou
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = random.choice([
                                "туть)",
                                "здесь:3",
                                "тута(:",
                                "дома)",
                                "здеся ^_^"
                                ]), 
                            random_id = random.randint(1,999999)
                        )
                    if (
                        " ".join(command[:2]).replace("?","") in howAreYou
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = random.choice([
                                "хорошо)\nа у тебя? :3",
                                "отличненько:3",
                                "плохо, чувствую усталость((",
                                "только проснулась, отлично)",
                                "плохо.."
                                ]), 
                            random_id = random.randint(1,999999)
                        )
                    if (
                        " ".join(command[:1]) in chance
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = f'вероятность "{" ".join(command[1:])}" {random.randint(1, 100)}%', 
                            random_id = random.randint(1,999999)
                        )
                    if (
                        " ".join(command[:1]) == "выбери"
                    ):  
                        try:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'мне нравится больше {random.choice(command[1:])} ', 
                                random_id = random.randint(1,999999)
                            )
                        except Exception as error:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'OOOPS... ошибочка\n команда "выбери" завершилась с ошибкой\n {error}', 
                                random_id = random.randint(1,999999)
                            )
                    if (
                        event.from_chat
                        and " ".join(command[:1]) == "кто"
                    ):
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id = event.object["message"]["peer_id"],
                                group_id = GROUP_ID)["items"])["member_id"]
                            #print(randomUserId)
                            firstName = vk.users.get(user_ids = randomUserId)[0]["first_name"]
                            #print(firstName)
                            lastName = vk.users.get(user_ids = randomUserId)[0]["last_name"]
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {" ".join(command[1:])}', 
                                random_id = random.randint(1,999999),
                                disable_mentions = 1
                            )
                        except Exception as error:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'OOOPS... ошибочка\n команда "кто" завершилась с ошибкой\n {error}', 
                                random_id = random.randint(1,999999)
                            )
                    if (
                        event.from_chat
                        and " ".join(command[:2]) == "у кого"
                    ):
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id = event.object["message"]["peer_id"],
                                group_id = GROUP_ID)["items"])["member_id"]
                               
                            print(randomUserId)
                            firstName = vk.users.get(user_ids = randomUserId, name_case = "gen")[0]["first_name"]
                            #print(firstName)
                            lastName = vk.users.get(user_ids = randomUserId, name_case = "gen")[0]["last_name"]
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'{random.choice(think)} у [id{randomUserId}|{firstName} {lastName}] {" ".join(command[2:])}', 
                                random_id = random.randint(1,999999),
                                disable_mentions = 1
                            )
                        except Exception as error:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'OOOPS... ошибочка\n команда "у кого" завершилась с ошибкой\n {error}', 
                                random_id = random.randint(1,999999)
                            )
                    if (
                        event.from_chat
                        and " ".join(command[:1]) == "кому"
                    ):
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id = event.object["message"]["peer_id"],
                                group_id = GROUP_ID)["items"])["member_id"]
                               
                            print(randomUserId)
                            firstName = vk.users.get(user_ids = randomUserId, name_case = "dat")[0]["first_name"]
                            #print(firstName)
                            lastName = vk.users.get(user_ids = randomUserId, name_case = "dat")[0]["last_name"]
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {random.choice(need)} {" ".join(command[1:])}', 
                                random_id = random.randint(1,999999),
                                disable_mentions = 1
                            )
                        except Exception as error:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = f'OOOPS... ошибочка\n команда "кому" завершилась с ошибкой\n {error}', 
                                random_id = random.randint(1,999999)
                            )
                if (
                    event.object["message"]["text"]
                    and (
                        event.from_user
                        or str(event.object["message"]["peer_id"] - 2000000000) in settings
                        and settings[str(event.object["message"]["peer_id"] - 2000000000)]["casino_on"] == "True"
                    )
                ):

                    with open("casino.json") as f:
                        casino = json.load(f)

                    if event.object["message"]["text"].split()[0] == "/казино":

                        gain = 0
                        rate = 0

                        if str(event.object["message"]["from_id"]) not in casino:
                            casino[str(event.object["message"]["from_id"])] = "100"

                        if (
                            int(event.object["message"]["text"].split()[1]) <= 0 
                            or not event.object["message"]["text"].split()[1].isdigit()
                        ):
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "нормальную ставку сделай, кловн",
                                random_id = random.randint(1, 999999)
                            )
                            continue

                        balance = int(casino[str(event.object["message"]["from_id"])])
                        rate = int(event.object["message"]["text"].split()[1])
                        
                        a = random.randint(1, 9)
                        b = random.randint(1, 9)
                        c = random.randint(1, 9)

                        if balance < rate:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "лох, денег нет",
                                random_id = random.randint(1, 999999)
                            )

                        elif a == b == c:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = (str(a)+" "+str(b)+" "+str(c)), 
                                random_id = random.randint(1,999999)
                            )

                            gain = rate * (a + b + c)

                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = f"ого, сорвал куш, выиргрыш {gain} руб",
                                random_id = random.randint(1, 999999)
                            )
                            casino[str(event.object["message"]["from_id"])] = str(balance + gain)


                        elif a == b or b == c or a == c:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = (str(a)+" "+str(b)+" "+str(c)), 
                                random_id = random.randint(1,999999)
                            )

                            gain = rate * random.choice([a, b, c])

                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = f"о, ты выиграл, твой выиргрыш {gain} руб",
                                random_id = random.randint(1, 999999)
                            )

                            casino[str(event.object["message"]["from_id"])] = str(balance + gain)

                        else:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = (str(a)+" "+str(b)+" "+str(c)), 
                                random_id = random.randint(1,999999)
                            )

                            balance = balance - rate

                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = f"ахахаха, лох, проиграл,  твой баланс {balance} руб",
                                random_id = random.randint(1, 999999)
                            )
                            casino[str(event.object["message"]["from_id"])] = str(balance)

                        with open("casino.json", "w") as f:
                            json.dump(casino, f)

                    if event.object["message"]["text"].split()[0] == "/баланс":
                        if str(event.object["message"]["from_id"]) not in casino:
                            casino[str(event.object["message"]["from_id"])] = "100"
                        
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"],
                            message = f"твой баланс {casino[str(event.message.from_id)]} руб",
                            random_id = random.randint(1, 999999)
                        )

                if (
                    event.object["message"]["text"] == "/admins"
                ):
                    try:
                        vk.messages.send(
                            peer_id =event.object["message"]["peer_id"],
                            message = "админы данного чата: "+get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[0],
                            random_id = random.randint(1,999999),
                            disable_mentions = 1
                        )
                    except:
                        vk.messages.send(
                            peer_id =event.object["message"]["peer_id"],
                            message = "не могу узнать админов данного чата...",
                            random_id = random.randint(1,999999)
                        )

                if (
                    event.object["message"]["attachments"] and
                    event.object["message"]["attachments"][0]["type"] == "audio_message" and
                    random.choices([True, False], weights = (25, 75), k=2)[0]
                ):

                    vk.messages.send(
                        peer_id = event.object["message"]["peer_id"],
                        message = "хрю-хрю",
                        random_id = random.randint(1, 999999)
                    )

                if (
                    "навальный" in event.object["message"]["text"].lower() and
                    random.choices([True, False], weights = (25, 75), k = 2)[0]
                ):

                    vk.messages.send(
                        peer_id = event.object["message"]["peer_id"],
                        random_id = random.randint(1, 999999),
                        attachment = "photo-202215029_457239052"
                    )

                if (
                    event.object["message"]["text"]
                    and event.object["message"]["text"].split()[0].lower() in ban
                    and event.object["message"]["from_id"] not in get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[1]
                ):
                    vk.messages.send(
                        peer_id = event.object["message"]["peer_id"],
                        message = "угомонись, хохлинка... кикать могут только админы",
                        random_id = random.randint(1, 999999)
                    )
                if (
                    event.object["message"]["from_id"] in get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[1]
                ):

                    if (
                        event.object["message"]["text"] and
                        event.object["message"]["text"].split()[0].lower() in ban
                    ):
                        if (
                            "reply_message" in event.object["message"] or
                            event.object["message"]["fwd_messages"]
                        ):
                            try:
                                if (
                                    "reply_message" in event.object["message"]
                                ):
                                    user_id = event.object["message"]["reply_message"]["from_id"]

                                    vk.messages.send(
                                        peer_id = event.object["message"]["peer_id"],
                                        message = "кикаю хохлинку...",
                                        random_id = random.randint(1, 999999)
                                    )

                                    vk.messages.removeChatUser(
                                        chat_id = event.object["message"]["peer_id"] - 2000000000, 
                                        user_id = user_id
                                    )

                                elif (
                                    event.object["message"]["fwd_messages"]
                                ):

                                    if len(event.object["message"]["fwd_messages"]) > 1:
                                        vk.messages.send(
                                            peer_id = event.object["message"]["peer_id"],
                                            message = "начинаю массовый кик хохлов",
                                            random_id = random.randint(1, 999999)
                                        )

                                    for fwd_msg in event.object["message"]["fwd_messages"]:

                                        vk.messages.send(
                                            peer_id = event.object["message"]["peer_id"],
                                            message = "кикаю хохлинку...",
                                            random_id = random.randint(1, 999999)
                                        )
                                        try:
                                            vk.messages.removeChatUser(
                                                chat_id = event.object["message"]["peer_id"] - 2000000000, 
                                                user_id = fwd_msg["from_id"]
                                            )
                                        except Exception as error:
                                            vk.messages.send(
                                                peer_id = event.object["message"]["peer_id"], 
                                                message = f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}", 
                                                random_id = random.randint(1,999999)
                                            )
                                
                            except Exception as error:
                                vk.messages.send(
                                    peer_id = event.object["message"]["peer_id"], 
                                    message = f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}", 
                                    random_id = random.randint(1,999999)
                                )
                        else:
                            banList = event.message.text
                            for banPrifix in ban:
                                banList.replace(banPrifix, "")

                            if len(banList.split()) > 1:
                                vk.messages.send(
                                    peer_id = event.object["message"]["peer_id"], 
                                    message = "начинаю массовый кик хохлов...", 
                                    random_id = random.randint(1,999999)
                                )
                            else:
                                vk.messages.send(
                                    peer_id = event.object["message"]["peer_id"], 
                                    message = "кикаю хохлинку...", 
                                    random_id = random.randint(1,999999)
                                )
                            for screen_name in banList.replace("[id", "").replace("[club", "").split():
                                #print(event.object["message"]["text"].replace("/ban", "").split())
                                user_id = ""
                                for char in screen_name:
                                    print(screen_name)
                                    if char.isdigit():
                                        user_id+=char
                                    else:
                                        break

                                try:
                                    vk.messages.removeChatUser(
                                        chat_id = event.object["message"]["peer_id"] - 2000000000, 
                                        user_id = user_id
                                    )
                                except Exception as error:
                                    vk.messages.send(
                                        peer_id = event.object["message"]["peer_id"], 
                                        message = f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}", 
                                        random_id = random.randint(1,999999)
                                    )

                    elif (
                        event.object["message"]["text"] == "/settings" and
                        event.object["message"]["from_id"] in get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[1]
                    ):
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"],
                            message = f" текущие настройки \n{str(settings.get(str(event.message.peer_id - 2000000000)))}",
                            random_id = random.randint(1, 999999)
                        )
                        
                    elif (
                        event.object["message"]["text"] and
                        event.object["message"]["text"].split()[0] == "/set" and
                        event.object["message"]["from_id"] in get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[1]
                    ):

                        params = event.object["message"]["text"].replace("/set", "").split()
                        if params[0] in settings.get(str(event.object["message"]["peer_id"] - 2000000000)):
                            settings[str((event.object["message"]["peer_id"] - 2000000000))].update({params[0]:params[1]})
                            with open('settings.json', 'w') as f:
                                json.dump(settings, f)
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = f'изменение параметра \"{params[0]}\"\n текущее значение \"{params[1]}\"',
                                random_id = random.randint(1, 999999)
                            )
                        else:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = f'параметра \"{params[0]}\" не существует!',
                                random_id = random.randint(1, 999999)
                            )

                    elif (
                        event.object["message"]["text"] == "/setToDefault" and
                        event.object["message"]["from_id"] in get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[1]
                    ):
                        settings[str(event.object["message"]["peer_id"] - 2000000000)] = {"captcha_on":"True", "casino_on":"False", "greeting_on":"False", "wife":"True"}
                        with open('settings.json', 'w') as f:
                            json.dump(settings, f)
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"],
                            message = f"настройки были сброшены, текущие настройки\n {str(settings[str(event.message.peer_id - 2000000000)])}",
                            random_id = random.randint(1, 999999)
                        )
    except Exception as error:
        print(error)
