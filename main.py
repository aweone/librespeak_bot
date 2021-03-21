import vk_api, random, time, json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from auth import vk, longpoll, vkAdmin, GROUP_ID
from chatSettings import settings
from chatAdmin import get_admin
from captcha import get_captcha
from uptime import upTime

timeup=time.time()
ids_captcha={}

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

                #print(                        event.object["message"]["text"] == "/admins" and
                #        event.object["message"]["from_id"] == 213045391)         
                    #print
                    #vk.messages.send(peer_id=event.peer_id, message = captcha_value[1], random_id=random.randint(1,999999), attachment=captcha_value[0])
                    
                    #if event.raw[6].get("source_act") == "chat_invite_user_by_link":
                if (
                    event.from_chat
                ):
                    if (
                        "action" in event.object["message"]
                    ):

                        if (
                            event.object["message"]["action"]["type"] == "chat_invite_user_by_link"
                            and (settings.get(str(event.object["message"]["peer_id"] - 2000000000)).get("captcha_on")) == "True"
                        ):

                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = ("новый [id"+str(event.object["message"]["from_id"])+"|пользователь] присоединился по ссылке"), 
                                random_id = random.randint(1,999999)
                            )
                            #print("новый юзер")
                            #   if event.object["message"]["text"] == "1234":
                            captcha_value = get_captcha()
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = "пройдите капчу или кик", 
                                random_id = random.randint(1,999999), 
                                attachment = captcha_value[0]
                            )
                            ids_captcha[str(event.object["message"]["from_id"])] = captcha_value[1]

                        #print(ids_captcha)
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
                            and (settings.get(str(event.object["message"]["peer_id"] - 2000000000)).get("greeting_on")) == "True"
                        ):
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = "еще один [id"+str(event.object["message"]["action"]["member_id"])+"|хохол] присоединился...", 
                                random_id = random.randint(1,999999)
                            )

                    elif (
                        str(event.object["message"]["from_id"]) in ids_captcha and
                        event.object["message"]["text"] == ids_captcha[str(event.object["message"]["from_id"])]
                    ):

                        ids_captcha.pop(str(event.object["message"]["from_id"]))
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"], 
                            message = "проверка пройдена", 
                            random_id = random.randint(1,999999)
                        )


                        #print( ids_captcha[str(event.user_id)] )
                    
                    elif (
                        str(event.object["message"]["from_id"]) in ids_captcha and
                        event.object["message"]["text"] != ids_captcha[str(event.object["message"]["from_id"])]
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
                        event.object["message"]["text"] and
                        event.object["message"]["text"].split()[0] == "/казино" and
                        settings.get(str(event.object["message"]["peer_id"] - 2000000000)).get("casino_on") == "True"
                    ):
                        with open("casino.json") as f:
                            casino = json.load(f)

                        gain = 0
                        rate = 0

                        if str(event.object["message"]["from_id"]) not in casino:
                            casino[str(event.object["message"]["from_id"])] = "100"
                        
                        balance = int(casino[str(event.object["message"]["from_id"])])
                        rate = int(event.object["message"]["text"].split()[1])
                        #print(123)
                        
                        a = random.randint(1, 9)
                        b = random.randint(1, 9)
                        c = random.randint(1, 9)

                        if balance < rate:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "лох, денег нет",
                                random_id = random.randint(1, 999999)
                            )
                        elif rate <= 0:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "нормальную ставку сделай, кловн",
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
                                message = "ого, сорвал куш, выиргрыш {} руб".format(gain),
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
                                message = "о, ты выиграл, твой выиргрыш {} руб".format(gain),
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
                                message = "ахахаха, лох, проиграл,  твой баланс {} руб".format(balance),
                                random_id = random.randint(1, 999999)
                            )
                            casino[str(event.object["message"]["from_id"])] = str(balance)

                        with open("casino.json", "w") as f:
                            json.dump(casino, f)


                    if (
                        event.object["message"]["text"] and
                        event.object["message"]["text"].split()[0] == "/баланс" and
                        settings.get(str(event.object["message"]["peer_id"] - 2000000000)).get("casino_on") == "True"
                    ):
                        with open("casino.json") as f:
                            casino = json.load(f)
                        
                        if str(event.object["message"]["from_id"]) not in casino:
                            casino[str(event.object["message"]["from_id"])] = "100"
                        
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"],
                            message = "твой баланс {} руб".format(casino[str(event.object["message"]["from_id"])]),
                            random_id = random.randint(1, 999999)
                        )

                    if (
                        event.object["message"]["text"] == "/admins"
                    ):
                        try:
                            vk.messages.send(
                                peer_id =event.object["message"]["peer_id"],
                                message = "админы данного чата: "+get_admin(event.object["message"]["peer_id"], GROUP_ID)[0],
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
                        event.object["message"]["text"] != ""
                        and event.object["message"]["text"].split()[0] == "/ban"
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
                            event.object["message"]["text"].split()[0] == "/ban"
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
                                        user_id = event.object["message"]["fwd_messages"][0]["from_id"]

                                        vk.messages.send(
                                            peer_id = event.object["message"]["peer_id"],
                                            message = "кикаю хохлинку...",
                                            random_id = random.randint(1, 999999)
                                        )

                                        vk.messages.removeChatUser(
                                            chat_id = event.object["message"]["peer_id"] - 2000000000, 
                                            user_id = user_id
                                        )
                                    
                                except:
                                    vk.messages.send(
                                        peer_id = event.object["message"]["peer_id"], 
                                        message = f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}", 
                                        random_id = random.randint(1,999999)
                                    )
                            else:
                                if len(event.object["message"]["text"].replace("/ban", "").split()) > 1:
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
                                for screen_name in event.object["message"]["text"].replace("/ban", "").replace("[id", "").replace("]", "").split():
                                    #print(event.object["message"]["text"].replace("/ban", "").split())
                                    user_id = ""
                                    for char in screen_name:
                                        print(screen_name)
                                        if char.isdigit():
                                            user_id+=char
                                        else:
                                            break
                                    #print(get_admin(event.object["message"]["peer_id"], GROUP_ID)[1])
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
                                message = str(settings.get(str(event.object["message"]["peer_id"] - 2000000000))),
                                random_id = random.randint(1, 999999)
                            )
                            
                        elif (
                            "text" in event.object["message"] and
                            event.object["message"]["text"].split()[0] == "/set" and
                            event.object["message"]["from_id"] in get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[1]
                        ):

                            params = event.object["message"]["text"].replace("/set", "").split()
                            if params[0] in settings.get(str(event.object["message"]["peer_id"] - 2000000000)):
                                settings[str((event.object["message"]["peer_id"] - 2000000000))].update({params[0]:params[1]})
                                with open('settings.json', 'w') as f:
                                    json.dump(settings, f)

                        elif (
                            event.object["message"]["text"] == "/setToDefault" and
                            event.object["message"]["from_id"] in get_admin(event.object["message"]["peer_id"], GROUP_ID, event)[1]
                        ):
                            settings[str(event.object["message"]["peer_id"] - 2000000000)] = {"captcha_on":"True", "casino_on":"False", "greeting_on":"False"}
                            with open('settings.json', 'w') as f:
                                json.dump(settings, f)

                elif (
                    event.from_user
                ):
                    #print("text" in event.object["message"], event.object["message"]["text"].split()[0] == "/казино")
                    if (
                        "text" in event.object["message"] and
                        event.object["message"]["text"].split()[0] == "/казино"
                    ):
                        with open("casino.json") as f:
                            casino = json.load(f)
                        gain = 0
                        rate = 0
                        if str(event.object["message"]["from_id"]) not in casino:
                            casino[str(event.object["message"]["from_id"])] = "100"
                        balance = int(casino[str(event.object["message"]["from_id"])])
                        rate = int(event.object["message"]["text"].split()[1])
                        #print(123)
                        a = random.randint(1, 9)
                        b = random.randint(1, 9)
                        c = random.randint(1, 9)

                        if balance < rate:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "лох, денег нет",
                                random_id = random.randint(1, 999999)
                            )
                        elif rate <= 0:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "нормальную ставку сделай, кловн",
                                random_id = random.randint(1, 999999)
                            )

                        elif a == b or b == c or a == c:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = (str(a)+" "+str(b)+" "+str(c)), 
                                random_id = random.randint(1,999999)
                            )

                            gain = rate * random.choice([a, b, c])
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "о, ты выиграл, твой выиргрыш {} руб".format(gain),
                                random_id = random.randint(1, 999999)
                            )
                            casino[str(event.object["message"]["from_id"])] = str(balance + gain)
                        elif a == b == c:
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"], 
                                message = (str(a)+" "+str(b)+" "+str(c)), 
                                random_id = random.randint(1,999999)
                            )

                            gain = rate * a * b * c
                            vk.messages.send(
                                peer_id = event.object["message"]["peer_id"],
                                message = "ого, сорвал куш, выиргрыш {} руб".format(gain),
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
                                message = "ахахаха, лох, проиграл,  твой баланс {} руб".format(balance),
                                random_id = random.randint(1, 999999)
                            )
                            casino[str(event.object["message"]["from_id"])] = str(balance)
                    
                    if (
                        "text" in event.object["message"] and
                        event.object["message"]["text"].split()[0] == "/баланс"
                    ):
                        with open("casino.json") as f:
                            casino = json.load(f)
                        
                        if str(event.object["message"]["from_id"]) not in casino:
                            casino[str(event.object["message"]["from_id"])] = "100"
                        
                        vk.messages.send(
                            peer_id = event.object["message"]["peer_id"],
                            message = "твой баланс {} руб".format(casino[str(event.object["message"]["from_id"])]),
                            random_id = random.randint(1, 999999)
                        )

    except Exception as error:
        print(error)

