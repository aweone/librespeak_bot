import vk_api
import random
import time
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from auth import vk, longpoll, vkAdmin, GROUP_ID
from chatSettings import settings
from chatAdmin import get_admin
from captchaNew import get_captcha
from uptime import upTime
from pathlib import Path
from qrGen import qrgen

vk_api.VkApi.RPS_DELAY = 1/20


def rid(): return random.randint(-2147483647, 2147483647)


def message(text, attachment="", disable_mentions=0):
    vk.messages.send(
        peer_id=peer_id,
        message=str(text),
        random_id=rid(),
        attachment=attachment,
        disable_mentions=disable_mentions)


timeup = time.time()
ids_captcha = {}
prefix = ["либребот", "либра", "вайфу", "/либребот", "/либра",
          "/вайфу", "/пинки", "пинки", "пинкипай", "/пинкипай"]
greetingMsg = ["привет", "приветик", "приф", "приф", "ку"]
howAreYou = ["как дела", "дела как", "как жизнь"]
ban = ["/ban", "!ban", "!бан", "/бан"]
whereAreYou = ["где ты", "ты где"]
chance = ["инфа", "вероятность", "шанс"]
developer = ["разраб", "разработчик", "создатель", "девелопер"]
think = ["я думаю, что ", "полагаю, ", "предполагаю, ", "я полагаю, что ",
         "мне кажется, ", "кажется что ", "я полагаю, что ", "я думаю, ", "думаю, что"]
who = ["у кого", "кто"]
need = ["нужно", "требуется", "необходимо", "надо"]
info = ["/help", "/помощь", "help", "помощь"]
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.object["message"]["text"]
                user_id = event.object["message"]["from_id"]
                peer_id = event.object["message"]["peer_id"]
                if user_id == 213045391 and text != "":
                    if text == "/инф":
                        message(f"бот работает, аптайм {upTime(timeup)}")

                    elif text == "/капча":
                        captcha_value = get_captcha()
                        message(captcha_value[1], captcha_value[0])

                    elif user_id == 213045391 and text.split()[0] == "/exec":
                        command = text.replace("/exec ", "")
                        exec(str(command))
                        print(command)

                if "action" in event.object["message"].keys():

                    if (
                        event.object["message"]["action"]["type"] == "chat_invite_user_by_link"
                        and (settings.get(str(peer_id - 2000000000)).get("captcha_on")) == "True"
                    ):

                        message(
                            f"новый [id{event.object['message']['from_id']}|пользователь] присоединился по ссылке")

                        captcha_value = get_captcha()
                        message("пройдите капчу или кик", captcha_value[0])
                        if str(peer_id) not in ids_captcha.keys():
                            ids_captcha[str(peer_id)] = {}
                        ids_captcha[str(peer_id)][str(
                            user_id)] = captcha_value[1]

                    elif event.object["message"]["action"]["type"] == "chat_kick_user" and (settings.get(str(peer_id - 2000000000)).get("greeting_on")) == "True":
                        message(
                            f"еще один [id{event.object['message']['action']['member_id']}|хохол] покидает нас, ура!")

                    elif (
                        event.object["message"]["action"]["type"] == "chat_invite_user"
                        and event.object["message"]["action"]["member_id"] != -202215029
                        and (settings.get(str(peer_id - 2000000000)).get("greeting_on")) == "True"
                    ):
                        message(
                            f'еще один [id{event.object["message"]["action"]["member_id"]}|хохол] присоединился...')

                    elif (
                        event.object["message"]["action"]["type"] == "chat_invite_user"
                        and event.object["message"]["action"]["member_id"] == -202215029
                    ):
                        message(
                            "оу, меня добавили в новую беседу, генерю новый конфиг для беседы. хохлам приветик!;)")
                        settings[str(peer_id - 2000000000)] = {
                            "captcha_on": "False", "casino_on": "True", "greeting_on": "True", "wife": "True", "qr": "True"}
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
                        chat_id=peer_id - 2000000000,
                        user_id=user_id
                    )

                    if peer_id == 2000000001:
                        vkAdmin.groups.ban(
                            group_id=GROUP_ID,
                            owner_id=user_id
                        )
                if (
                    text
                    and text.split()[0] in info
                ):
                    message("coming soon...")
                if (
                    text
                    and text.split()[0].lower() == "помогите"
                ):
                    message("помогаю")

                if (text and text.lower().split()[0] in prefix
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

                    if " ".join(command[:2]).replace("?", "") in whereAreYou:
                        message(random.choice([
                                "туть)",
                                "здесь:3",
                                "тута(:",
                                "дома)",
                                "здеся ^_^"
                                ]))

                    if " ".join(command[:2]).replace("?", "") in howAreYou:
                        message(random.choice([
                                "хорошо)\nа у тебя? :3",
                                "отличненько:3",
                                "плохо, чувствую усталость((",
                                "только проснулась, отлично)",
                                "плохо.."
                                ]))
                    if " ".join(command[:1]) in chance:
                        message(
                            f'вероятность "{" ".join(command[1:])}" {random.randint(1, 100)}%')
                    if " ".join(command[:1]) == "помоги":
                        message("помогаю")
                    if " ".join(command[:1]) == "выбери":
                        try:
                            message(
                                f'мне нравится больше {random.choice(command[1:])} ')
                        except Exception as error:
                            if str(error) == "list index out of range":
                                message('мне не из чего выбирать')
                            else:
                                message(
                                    f'ошибочка\n , команда "выбери" завершилась с ошибкой\n {error}')

                    if " ".join(command[:1]) == "когда":
                        try:
                            date = time.gmtime(
                                time.time() + random.randint(5000, 100000000))

                            message(
                                f'{random.choice(think)} {date.tm_year}.{date.tm_mon}.{date.tm_mday} в {date.tm_hour}:{date.tm_min}:{date.tm_sec} {" ".join(command[1:])}')
                        except Exception as error:
                            message(
                                'ошибка!\nкоманда "когда" завершилась с ошибкой\n{error}')
                    if event.from_chat and " ".join(command[:1]) == "кто":
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id=peer_id,
                                group_id=GROUP_ID)["items"])["member_id"]

                            usrname = vk.users.get(user_ids=randomUserId)[0]
                            firstName = usrname["first_name"]
                            lastName = usrname["last_name"]
                            message(
                                f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {" ".join(command[1:])}', disable_mentions=1)

                        except Exception as error:
                            if str(error) == "[917] You don't have access to this chat":
                                message(
                                    'у меня нет админки((\n не могу получить список участников')
                            else:
                                message(
                                    f'ошибочка\nкоманда "кто" завершилась с ошибкой\n {error}')

                    if event.from_chat and " ".join(command[:2]) == "у кого":
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id=peer_id,
                                group_id=GROUP_ID)["items"])["member_id"]

                            usrname = vk.users.get(
                                user_ids=randomUserId, name_case="gen")[0]
                            firstName = usrname["first_name"]
                            lastName = usrname["last_name"]
                            message(
                                f'{random.choice(think)} у [id{randomUserId}|{firstName} {lastName}] {" ".join(command[2:])}', disable_mentions=1)

                        except Exception as error:
                            if str(error) == "[917] You don't have access to this chat":
                                message(
                                    'у меня нет админки((\n не могу получить список участников')
                            else:
                                message(
                                    f'ошибочка\nкоманда "у кого" завершилась с ошибкой\n {error}')

                    if event.from_chat and " ".join(command[:1]) == "кому":
                        try:
                            randomUserId = random.choice(vk.messages.getConversationMembers(
                                peer_id=peer_id,
                                group_id=GROUP_ID)["items"])["member_id"]

                            usrname = vk.users.get(
                                user_ids=randomUserId, name_case="dat")[0]
                            firstName = usrname["first_name"]
                            lastName = usrname["last_name"]
                            message(
                                f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {random.choice(need)} {" ".join(command[1:])}', disable_mentions=1)

                        except Exception as error:
                            if str(error) == "[917] You don't have access to this chat":
                                message(
                                    'у меня нет админки((\n не могу получить список участников')
                            else:
                                message(
                                    f'ошибочка\nкоманда "кому" завершилась с ошибкой\n {error}')
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
                        message("ваш qrcode", attachment=qrgen(text[3:]))
                    except Exception as error:
                        message(
                            'ошибка!\nкоманда "qr" завершилась с ошибкой\n{error}')
                if (
                    text
                    and (
                        event.from_user
                        or str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["casino_on"] == "True"
                    )
                ):

                    with open(f'{Path.home()}/.config/librespeak_bot/casino.json') as f:
                        casino = json.load(f)

                    if text.split()[0] == "/казино":

                        gain = 0
                        rate = 0

                        if str(user_id) not in casino:
                            casino[str(user_id)] = "100"

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
                            message(f"{a} {b} {c}")
                            if a == b == c:
                                gain = rate * (a + b + c)
                                message(
                                    f"ого, сорвал куш, выиргрыш {gain} руб")
                                casino[str(user_id)] = str(balance + gain)

                            elif a == b or b == c or a == c:
                                gain = rate * random.choice([a, b, c])
                                message(
                                    f"о, ты выиграл, твой выигрыш {gain} руб")
                                casino[str(user_id)] = str(balance + gain)

                            else:
                                balance = balance - rate
                                message(
                                    f"ахахаха, лох, проиграл, твой баланс {balance} руб")
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
                        print(vk.users.get(
                            user_ids=get_admin(peer_id, GROUP_ID)[1]))
                        for admin in vk.users.get(user_ids=get_admin(peer_id, GROUP_ID)[1]):
                            userrId = admin["id"]
                            userFirstName = admin["first_name"]
                            userLastName = admin["last_name"]
                            admins += f"[id{ userrId }|{ userFirstName } { userLastName }]\n"

                        message("админы данного чата:\n" +
                                admins, disable_mentions=1)
                    except:
                        message("не могу узнать админов данного чата...")

                if event.object["message"]["attachments"] and event.object["message"]["attachments"][0]["type"] == "audio_message" and random.choices([True, False], weights=(25, 75), k=2)[0]:
                    message("хрю-хрю")

                if "навальный" in text.lower() and random.choices([True, False], weights=(25, 75), k=2)[0]:

                    message("", "photo-202215029_457239052")

                if text and text.split()[0].lower() in ban and user_id not in get_admin(peer_id, GROUP_ID)[1]:
                    message("угомонись, хохлинка... кикать могут только админы")

                if user_id in get_admin(peer_id, GROUP_ID)[1]:

                    if text and text.split()[0].lower() in ban:
                        if "reply_message" in event.object["message"] or event.object["message"]["fwd_messages"]:
                            if "reply_message" in event.object["message"]:
                                user_id = event.object["message"]["reply_message"]["from_id"]

                                message("кикаю хохлинку...")
                                try:
                                    vk.messages.removeChatUser(
                                        chat_id=peer_id - 2000000000,
                                        user_id=user_id
                                    )
                                except Exception as error:
                                    print(error)
                                    if str(error) == "[935] User not found in chat":
                                        message(
                                            "мань, такого юзера нет в чате...")
                                    elif str(error) == "[15] Access denied: can't remove this user":
                                        message(
                                            "зачем ты другого админа забанить хочешь?")
                                    else:
                                        message(
                                            f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}")

                            elif event.object["message"]["fwd_messages"]:

                                if len(event.object["message"]["fwd_messages"]) > 1:
                                    message("начинаю массовый кик хохлов")

                                for fwd_msg in event.object["message"]["fwd_messages"]:

                                    message("кикаю хохлинку...")
                                    try:
                                        vk.messages.removeChatUser(
                                            chat_id=peer_id - 2000000000,
                                            user_id=fwd_msg["from_id"]
                                        )
                                    except Exception as error:
                                        print(error)
                                    if str(error) == "[935] User not found in chat":
                                        message(
                                            "мань, такого юзера нет в чате...")
                                    elif str(error) == "[15] Access denied: can't remove this user":
                                        message(
                                            "зачем ты другого админа забанить хочешь?")
                                    else:
                                        message(
                                            f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}")

                        else:
                            print(123)
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
                                    message(
                                        "ты што, хочешь забанить такую тяночку как я???")
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
                                        chat_id=peer_id - 2000000000,
                                        user_id=user_id
                                    )
                                except Exception as error:
                                    print(error)
                                    if str(error) == "[935] User not found in chat":
                                        message(
                                            "мань, такого юзера нет в чате...")
                                    elif str(error) == "[15] Access denied: can't remove this user":
                                        message(
                                            "зачем ты другого админа забанить хочешь?")
                                    else:
                                        message(
                                            f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}")

                    elif text == "/settings" and user_id in get_admin(peer_id, GROUP_ID)[1]:
                        message(
                            f"текущие настройки \n{settings.get(str(event.message.peer_id - 2000000000))}")

                    elif text and text.split()[0] == "/set" and user_id in get_admin(peer_id, GROUP_ID)[1]:

                        params = text.replace("/set", "").split()
                        if params[0] in settings.get(str(peer_id - 2000000000)):
                            settings[str((peer_id - 2000000000))
                                     ].update({params[0]: params[1]})
                            with open(f'{Path.home()}/.config/librespeak_bot/chatSettings.json', 'w') as f:
                                json.dump(settings, f)
                            message(
                                f'изменение параметра \"{params[0]}\"\n текущее значение \"{params[1]}\"')
                        else:
                            message(
                                f'параметра \"{params[0]}\" не существует!')

                    elif text == "/setToDefault" and user_id in get_admin(peer_id, GROUP_ID)[1]:
                        settings[str(peer_id - 2000000000)] = {
                            "captcha_on": "False", "casino_on": "True", "greeting_on": "True", "wife": "True", "qr": "True"}
                        with open(f'{Path.home()}/.config/librespeak_bot/chatSettings.json', 'w') as f:
                            json.dump(settings, f)
                        message(
                            f"настройки были сброшены, текущие настройки\n {settings[str(event.message.peer_id - 2000000000)]}")

    except Exception as error:
        print(error)
