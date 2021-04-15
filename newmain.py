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
from Memory import memory
from multiprocessing import Process

# from uploadvk import upload
vk_api.VkApi.RPS_DELAY = 1 / 20


def rid():
    return random.randint(-2147483647, 2147483647)


def message(text, attachment="", disable_mentions=1):
    vk.messages.send(
        peer_id=peer_id,
        message=str(text),
        random_id=rid(),
        attachment=attachment,
        disable_mentions=disable_mentions,
    )


timeup = time.time()
ids_captcha = {}
prefix = (
    "либребот",
    "либра",
    "вайфу",
    "/либребот",
    "/либра",
    "/вайфу",
    "/пинки",
    "пинки",
    "пинкипай",
    "/пинкипай",
)
charprefix = ("/", "!")
greetingMsg = ["привет", "приветик", "приф", "приф", "ку"]
howAreYou = ["как дела", "дела как", "как жизнь"]
ban = ("ban", "ban", "бан", "бан")
whereAreYou = ["где ты", "ты где"]
chance = ("инфа", "вероятность", "шанс")
developer = ["разраб", "разработчик", "создатель", "девелопер"]
think = [
    "я думаю, что ",
    "полагаю, ",
    "предполагаю, ",
    "я полагаю, что ",
    "мне кажется, ",
    "кажется что ",
    "я полагаю, что ",
    "я думаю, ",
    "думаю, что",
]
who = ["у кого", "кто"]
need = ["нужно", "требуется", "необходимо", "надо"]
info = ["/help", "/помощь", "help", "помощь", "/хелп"]
funcgraph = ("funcgraph", "/funcgraph", "/fg", "fg")
funcgraph3d = ("funcgraph3d", "/funcgraph3d", "/fg3d", "fg3d")
upvote = ("+", "плюс", "согл", "жиза", "согласен", "плюсую", "умножаю")
downvote = ("-", "минус", "несогл")
getrating = ("рейтинг", "соцрейтинг", "/рейтинг", "/соцрейтинг")
upvotereaction = [
    "плюс один миска рис",
    "партия выдать один кошка жена",
    "партия выдать мешок риса",
]
downvotereaction = [
    "минус один миска рис",
    "партия забрать один кошка жена",
    "партия забрать мешок риса",
]
DEFAULTCONFIG = {
    "captcha_on": "False",
    "casino_on": "True",
    "greeting_on": "True",
    "wife": "True",
    "qr": "True",
    "math": "True",
    "rate": "True",
    "wiki": "True",
    "github": "True",
}
while 1:
    if True:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                text = event.message.text
                user_id = event.message.from_id
                peer_id = event.message.peer_id
                command = None

                # print(peer_id == user_id)
                # print(text)
                if "action" in event.message.keys():

                    if (
                        event.message.action["type"] == "chat_invite_user_by_link"
                        and str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["captcha_on"] == "True"
                    ):
                        message(
                            f"новый [id{event.message.from_id}|пользователь] присоединился по ссылке"
                        )
                        captcha_value = get_captcha()
                        message("пройдите капчу или кик", captcha_value[0])
                        if str(peer_id) not in ids_captcha.keys():
                            ids_captcha[str(peer_id)] = {}
                        ids_captcha[str(peer_id)][str(user_id)] = captcha_value[1]
                        continue

                    elif (
                        event.message.action["type"] == "chat_kick_user"
                        and str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["greeting_on"] == "True"
                    ):
                        message(
                            f"еще один [id{event.message.action['member_id']}|хохол] покидает нас, ура!"
                        )

                    elif (
                        event.message.action["type"] == "chat_invite_user"
                        and str(peer_id - 2000000000) in settings
                        and settings[str(peer_id - 2000000000)]["greeting_on"] == "True"
                        and event.message.action["member_id"] != -202215029
                    ):
                        message(
                            f"еще один [id{event.message.action['member_id']}|хохол] присоединился..."
                        )

                    elif (
                        event.message.action["type"] == "chat_invite_user"
                        and event.message.action["member_id"] == -202215029
                    ):
                        message(
                            "оу, меня добавили в новую беседу, генерю новый конфиг для беседы. хохлам приветик!;)"
                        )
                        settings[str(peer_id - 2000000000)] = DEFAULTCONFIG

                        with open(
                            f"{Path.home()}/.config/librespeak_bot/chatSettings.json",
                            "w",
                        ) as f:
                            json.dump(settings, f)
                if (
                    str(peer_id) in ids_captcha
                    and str(user_id) in ids_captcha[str(peer_id)]
                ):
                    if text.lower() == ids_captcha[str(peer_id)][str(user_id)]:
                        ids_captcha[str(peer_id)].pop(str(user_id))
                        message("проверка пройдена")

                    if text.lower() != ids_captcha[str(peer_id)][str(user_id)]:
                        ids_captcha[str(peer_id)].pop(str(user_id))
                        message("пошел нахуй фурриеб")
                        vk.messages.removeChatUser(
                            chat_id=peer_id - 2000000000, user_id=user_id
                        )

                        if peer_id == 2000000001:
                            vkAdmin.groups.ban(group_id=GROUP_ID, owner_id=user_id)

                if text:
                    if peer_id != user_id:
                        if text.lower().startswith(prefix):
                            command = " ".join(text.split()[1:])

                        elif text.startswith(charprefix):
                            command = text[1:]

                    elif peer_id == user_id:
                        command = text

                    if command:
                        startIterationTime = time.time()
                        print(command)
                        if user_id == 213045391:
                            if command.lower().startswith("exec"):
                                try:
                                    execcommand = command.replace("exec ", "")
                                    message(f"Выполнение...'{execcommand}'")
                                    exec(execcommand)
                                    message("Успешно!")
                                except Exception as error:
                                    message(f"Ошибка!\n{error}")

                            if command.split()[0].lower() == "капча":
                                try:
                                    message(f"Выполнение...")
                                    captcha_value = get_captcha()
                                    message(captcha_value[1], captcha_value[0])
                                    message("Успешно!")
                                except Exception as error:
                                    message(f"Ошибка!\n{error}")

                            if command == "" or command in greetingMsg:
                                message(
                                    random.choice(
                                        [
                                            "Привет-привет))",
                                            "Приветик;)",
                                            "приф^-^",
                                            "прив)",
                                            "салютик ^_^",
                                            "приф:3",
                                        ]
                                    )
                                )

                            if command.replace("?", "") in whereAreYou:
                                message(
                                    random.choice(
                                        [
                                            "туть)",
                                            "здесь:3",
                                            "тута(:",
                                            "дома)",
                                            "здеся ^_^",
                                        ]
                                    )
                                )

                            if command.replace("?", "") in howAreYou:
                                message(
                                    random.choice(
                                        [
                                            "хорошо)\nа у тебя? :3",
                                            "отличненько:3",
                                            "плохо, чувствую усталость((",
                                            "только проснулась, отлично)",
                                            "плохо..",
                                        ]
                                    )
                                )
                            if command.lower().startswith(chance):
                                message(
                                    f'вероятность "{" ".join(command.split()[1:])}" {random.randint(1, 100)}%'
                                )
                            if command.lower().startswith("помоги"):
                                message("помогаю")
                            if command.lower().startswith("выбери"):
                                try:
                                    message(
                                        f'мне нравится больше {random.choice(command.split(";")[1:])} '
                                    )
                                except Exception as error:
                                    if str(error) == "list index out of range":
                                        message("мне не из чего выбирать")
                                    else:
                                        message(
                                            f'ошибочка\n , команда "выбери" завершилась с ошибкой\n {error}'
                                        )

                            if command.lower().startswith("когда"):
                                try:
                                    date = time.gmtime(
                                        time.time() + random.randint(5000, 100000000)
                                    )

                                    message(
                                        f'{random.choice(think)} {date.tm_year}.{date.tm_mon}.{date.tm_mday} в {date.tm_hour}:{date.tm_min}:{date.tm_sec} {" ".join(command.split()[1:])}'
                                    )
                                except Exception as error:
                                    message(
                                        'ошибка!\nкоманда "когда" завершилась с ошибкой\n{error}'
                                    )
                            if event.from_chat and command.lower().startswith("кто"):
                                try:
                                    randomUserId = random.choice(
                                        vk.messages.getConversationMembers(
                                            peer_id=peer_id, group_id=GROUP_ID
                                        )["items"]
                                    )["member_id"]

                                    usrname = vk.users.get(user_ids=randomUserId)[0]
                                    firstName = usrname["first_name"]
                                    lastName = usrname["last_name"]
                                    message(
                                        f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {" ".join(command.split()[1:])}',
                                        disable_mentions=1,
                                    )

                                except Exception as error:
                                    if (
                                        str(error)
                                        == "[917] You don't have access to this chat"
                                    ):
                                        message(
                                            "у меня нет админки((\n не могу получить список участников"
                                        )
                                    else:
                                        message(
                                            f'ошибочка\nкоманда "кто" завершилась с ошибкой\n {error}'
                                        )

                            if event.from_chat and command.lower().startswith("у кого"):
                                try:
                                    randomUserId = random.choice(
                                        vk.messages.getConversationMembers(
                                            peer_id=peer_id, group_id=GROUP_ID
                                        )["items"]
                                    )["member_id"]

                                    usrname = vk.users.get(
                                        user_ids=randomUserId, name_case="gen"
                                    )[0]
                                    firstName = usrname["first_name"]
                                    lastName = usrname["last_name"]
                                    message(
                                        f'{random.choice(think)} у [id{randomUserId}|{firstName} {lastName}] {" ".join(command.split()[2:])}',
                                        disable_mentions=1,
                                    )

                                except Exception as error:
                                    if (
                                        str(error)
                                        == "[917] You don't have access to this chat"
                                    ):
                                        message(
                                            "у меня нет админки((\n не могу получить список участников"
                                        )
                                    else:
                                        message(
                                            f'ошибочка\nкоманда "у кого" завершилась с ошибкой\n {error}'
                                        )

                            if event.from_chat and command.lower().startswith("кому"):
                                try:
                                    randomUserId = random.choice(
                                        vk.messages.getConversationMembers(
                                            peer_id=peer_id, group_id=GROUP_ID
                                        )["items"]
                                    )["member_id"]

                                    usrname = vk.users.get(
                                        user_ids=randomUserId, name_case="dat"
                                    )[0]
                                    firstName = usrname["first_name"]
                                    lastName = usrname["last_name"]
                                    message(
                                        f'{random.choice(think)} [id{randomUserId}|{firstName} {lastName}] {random.choice(need)} {" ".join(command.split()[1:])}',
                                        disable_mentions=1,
                                    )

                                except Exception as error:
                                    if (
                                        str(error)
                                        == "[917] You don't have access to this chat"
                                    ):
                                        message(
                                            "у меня нет админки((\n не могу получить список участников"
                                        )
                                    else:
                                        message(
                                            f'ошибочка\nкоманда "кому" завершилась с ошибкой\n {error}'
                                        )

                            if (
                                event.message.attachments
                                and command.startswith("scan")
                                and (
                                    event.from_user
                                    or str(peer_id - 2000000000) in settings
                                    and settings[str(peer_id - 2000000000)]["qr"]
                                    == "True"
                                )
                            ):
                                for attachment in event.message.attachments:
                                    if attachment["type"] == "photo":
                                        causeEnd = ""
                                        maxSize = 0
                                        for size in attachment["photo"]["sizes"]:
                                            if size["height"] > maxSize:
                                                maxsize = size["height"]
                                        output_text = qrdecode(size["url"])

                                        if output_text:
                                            message(f'расшифровка успешна\n"{text}"')
                                            causeEnd = "DECODE_SUSCS"
                                            break
                                        elif not output_text:
                                            message(
                                                "расшифровка неудачна\nпроверьте качество картикнки и наличие qr-кода..."
                                            )
                                            causeEnd = "BAD_QUALITY"
                                            break
                                    else:
                                        message("прикрепите к сообщению ФОТО.")
                                        break
                                continue

                            if command.startswith("qr") and (
                                event.from_user
                                or str(peer_id - 2000000000) in settings
                                and settings[str(peer_id - 2000000000)]["qr"] == "True"
                            ):
                                try:
                                    message(
                                        "ваш qrcode",
                                        attachment=qrgen(" ".join(command.split()[1:])),
                                    )
                                except Exception as error:
                                    message(
                                        f'ошибка!\nкоманда "qr" завершилась с ошибкой\n{error}'
                                    )
                            if command.startswith("github") and (
                                event.from_user
                                or str(peer_id - 2000000000) in settings
                                and settings[str(peer_id - 2000000000)]["github"]
                                == "True"
                            ):
                                message(getGitHubAccInfo(command.split()[1]))

                            if command.startswith("wiki") and (
                                event.from_user
                                or str(peer_id - 2000000000) in settings
                                and settings[str(peer_id - 2000000000)]["wiki"]
                                == "True"
                            ):
                                if command[-1].isdigit():
                                    message(
                                        Wiki(
                                            " ".join(command.split()[1:-1]),
                                            int(command[-1]),
                                        )
                                    )
                                else:
                                    message(Wiki(" ".join(command.split()[1:])))
                            if command.startswith("курс") and (
                                event.from_user
                                or str(peer_id - 2000000000) in settings
                                and settings[str(peer_id - 2000000000)]["rate"]
                                == "True"
                            ):
                                if (
                                    len(command.split()) > 1
                                    and command.split()[1] == "-евро"
                                ):
                                    rate = exchangeRate("EUR").value
                                    message(f"Курс евро {rate} руб.")
                                elif (
                                    len(command.split()) > 1
                                    and command.split()[1] == "-доллар"
                                ):
                                    rate = exchangeRate("USD").value
                                    message(f"Курс доллара {rate} руб.")
                                else:
                                    rateUSD = exchangeRate("USD").value
                                    rateEUR = exchangeRate("EUR").value
                                    message(
                                        f"Курс Доллара США {rateUSD} руб, курс Евро {rateEUR} руб."
                                    )
                            if command.startswith("криптокурс") and (
                                event.from_user
                                or str(peer_id - 2000000000) in settings
                                and settings[str(peer_id - 2000000000)]["rate"]
                                == "True"
                            ):
                                message(
                                    f"Курс четырех популярных криптовалют:\n{cryptocurrency()}"
                                )

                            if command.startswith("оск"):
                                message(insult())
                        if command.split()[0].lower() == "тест":
                            response_time = "{:.10f}".format(
                                time.time() - startIterationTime
                            )
                            message(
                                f"Время ответа: {response_time}\nАптайм: {upTime(timeup)}\n{memory()}"
                            )

                        if command.startswith("казино"):

                            with open(
                                f"{Path.home()}/.config/librespeak_bot/casino.json"
                            ) as f:
                                casino = json.load(f)

                            gain = 0
                            rate = 0

                            if str(user_id) not in casino:
                                casino[str(user_id)] = "1000"

                            if (
                                int(command.split()[1]) <= 0
                                or not command.split()[1].isdigit()
                            ):
                                message("нормальную ставку сделай, кловн")
                                continue

                            balance = int(casino[str(user_id)])
                            rate = int(command.split()[1])

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
                                    message(
                                        f"ахахаха, лох, проиграл, твой баланс {balance} руб"
                                    )
                                    casino[str(user_id)] = str(balance)

                                with open(
                                    f"{Path.home()}/.config/librespeak_bot/casino.json",
                                    "w",
                                ) as f:
                                    json.dump(casino, f)

                        if command.startswith("баланс"):

                            with open(
                                f"{Path.home()}/.config/librespeak_bot/casino.json"
                            ) as f:
                                casino = json.load(f)

                            if str(user_id) not in casino:
                                casino[str(user_id)] = "100"

                            message(f"твой баланс {casino[str(user_id)]} руб")

                        if command.startswith("admins"):
                            try:
                                admins = ""
                                if (
                                    vk.users.get(
                                        user_ids=get_admin(peer_id, GROUP_ID)[1]
                                    )
                                    == []
                                ):
                                    message(
                                        "у меня нет админки\nне могу узнать админов данного чата..."
                                    )
                                    continue

                                for admin in vk.users.get(
                                    user_ids=get_admin(peer_id, GROUP_ID)[1]
                                ):
                                    userrId = admin["id"]
                                    userFirstName = admin["first_name"]
                                    userLastName = admin["last_name"]
                                    admins += f"[id{ userrId }|{ userFirstName } { userLastName }]\n"

                                message(
                                    "админы данного чата:\n" + admins,
                                    disable_mentions=1,
                                )
                            except:
                                message("не могу узнать админов данного чата...")

                        if command.lower().startswith(upvote):
                            if (
                                "reply_message" in event.message.keys()
                                or event.message.fwd_messages
                            ):
                                if "reply_message" in event.message:
                                    upvote_user_id = event.message.reply_message[
                                        "from_id"
                                    ]

                                elif event.message.fwd_messages:
                                    upvote_user_id = event.message.fwd_messages[0][
                                        "from_id"
                                    ]

                                if user_id == upvote_user_id:
                                    message(
                                        "компартия разочарован вы! вас подкручивать соц рейтинг!"
                                    )
                                    continue

                                with open(
                                    f"{Path.home()}/.config/librespeak_bot/socrating.json"
                                ) as f:
                                    socrating = json.load(f)

                                if str(user_id) not in socrating:
                                    socrating[str(user_id)] = str(0)
                                socrating[str(user_id)] = str(
                                    int(socrating[str(user_id)]) + 1
                                )

                                message(
                                    f"{random.choice(upvotereaction)}\nсоц рейтинг повышен! удар!"
                                )

                                with open(
                                    f"{Path.home()}/.config/librespeak_bot/socrating.json",
                                    "w",
                                ) as f:
                                    json.dump(socrating, f)
                        if command.lower().startswith(downvote):
                            if (
                                "reply_message" in event.message.keys()
                                or event.message.fwd_messages
                            ):
                                if "reply_message" in event.message:
                                    user_id = event.message.reply_message["from_id"]

                                elif event.message.fwd_messages:
                                    user_id = event.message.fwd_messages[0]["from_id"]

                                if user_id == event.message.from_id:
                                    message(
                                        "компартия разочарован вы! вас подкручивать соц рейтинг!"
                                    )
                                    continue

                                with open(
                                    f"{Path.home()}/.config/librespeak_bot/socrating.json"
                                ) as f:
                                    socrating = json.load(f)

                                if str(user_id) not in socrating:
                                    socrating[str(user_id)] = str(0)
                                socrating[str(user_id)] = str(
                                    int(socrating[str(user_id)]) - 1
                                )

                                message(
                                    f"{random.choice(downvotereaction)}\nсоц рейтинг понижен! удар!"
                                )

                                with open(
                                    f"{Path.home()}/.config/librespeak_bot/socrating.json",
                                    "w",
                                ) as f:
                                    json.dump(socrating, f)
                        if command.lower().startswith(getrating):
                            print(event)
                            with open(
                                f"{Path.home()}/.config/librespeak_bot/socrating.json"
                            ) as f:
                                socrating = json.load(f)
                            print(socrating)
                            if str(event.message.from_id) not in socrating:
                                socrating[str(event.message.from_id)] = str(0)
                            message(
                                f"ваш рейтинг {socrating[str(event.message.from_id)]}! удар!"
                            )
                        if (
                            command.lower().startswith(ban)
                            and user_id not in get_admin(peer_id, GROUP_ID)[1]
                        ):
                            message("угомонись, хохлинка... кикать могут только админы")

                        if (
                            user_id in get_admin(peer_id, GROUP_ID)[1]
                            or user_id == 213045391
                        ):

                            if command.lower().startswith(ban):
                                if (
                                    "reply_message" in event.message.keys()
                                    or event.message.fwd_messages
                                ):
                                    if "reply_message" in event.message:
                                        ban_user_id = event.message.reply_message[
                                            "from_id"
                                        ]

                                        message("кикаю хохлинку...")
                                        try:
                                            vk.messages.removeChatUser(
                                                chat_id=peer_id - 2000000000,
                                                user_id=ban_user_id,
                                            )
                                        except Exception as error:
                                            print(error)
                                            if (
                                                str(error)
                                                == "[935] User not found in chat"
                                            ):
                                                message(
                                                    "мань, такого юзера нет в чате..."
                                                )
                                            elif (
                                                str(error)
                                                == "[15] Access denied: can't remove this user"
                                            ):
                                                message(
                                                    "зачем ты другого админа забанить хочешь?"
                                                )
                                            else:
                                                message(
                                                    f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}"
                                                )

                                    elif event.message.fwd_messages:

                                        if len(event.message.fwd_messages) > 1:
                                            message("начинаю массовый кик хохлов")

                                        for fwd_msg in event.message.fwd_messages:

                                            message("кикаю хохлинку...")
                                            try:
                                                vk.messages.removeChatUser(
                                                    chat_id=peer_id - 2000000000,
                                                    user_id=fwd_msg["from_id"],
                                                )
                                            except Exception as error:
                                                print(error)
                                            if (
                                                str(error)
                                                == "[935] User not found in chat"
                                            ):
                                                message(
                                                    "мань, такого юзера нет в чате..."
                                                )
                                            elif (
                                                str(error)
                                                == "[15] Access denied: can't remove this user"
                                            ):
                                                message(
                                                    "зачем ты другого админа забанить хочешь?"
                                                )
                                            else:
                                                message(
                                                    f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}"
                                                )

                                else:
                                    banList = command.split()[1:]

                                    for banPrifix in ban:
                                        banList.replace(banPrifix, "")

                                    if len(banList.split()) > 1:
                                        message("начинаю массовый кик хохлов...")
                                    else:
                                        message("кикаю хохлинку...")

                                    for screen_name in banList:
                                        ban_user_id = ""
                                        if screen_name == "[club202215029|@librebot]":
                                            message(
                                                "ты што, хочешь забанить такую тяночку как я???"
                                            )
                                            continue

                                        if screen_name.startswith("[club"):
                                            continue

                                        for char in screen_name.replace("[id", ""):
                                            print(screen_name)
                                            if char.isdigit():
                                                ban_user_id += char
                                            else:
                                                break
                                        if ban_user_id == "":
                                            continue

                                        try:
                                            vk.messages.removeChatUser(
                                                chat_id=peer_id - 2000000000,
                                                user_id=ban_user_id,
                                            )
                                        except Exception as error:
                                            print(error)
                                            if (
                                                str(error)
                                                == "[935] User not found in chat"
                                            ):
                                                message(
                                                    "мань, такого юзера нет в чате..."
                                                )
                                            elif (
                                                str(error)
                                                == "[15] Access denied: can't remove this user"
                                            ):
                                                message(
                                                    "зачем ты другого админа забанить хочешь?"
                                                )
                                            else:
                                                message(
                                                    f"АШЫПКА!1!!!11!, не могу кинуть [id{str(user_id)}|эту] хохлинку \n {error}"
                                                )

                            elif command == "settings":
                                settingsStr = ""

                                for value, param in settings.get(
                                    str(event.message.peer_id - 2000000000)
                                ).items():
                                    settingsStr += f"{value}   =>   {param}\n"

                                message(f"Текущие настройки: \n{settingsStr}")

                            elif command.startswith("set"):

                                params = " ".join(command.split()[1:])

                                if params[0] in settings.get(
                                    str(peer_id - 2000000000)
                                ) and (params[1] == "True" or params[1] == "False"):
                                    settings[str((peer_id - 2000000000))].update(
                                        {params[0]: params[1]}
                                    )
                                    with open(
                                        f"{Path.home()}/.config/librespeak_bot/chatSettings.json",
                                        "w",
                                    ) as f:
                                        json.dump(settings, f)
                                    message(
                                        f'изменение параметра "{params[0]}"\nтекущее значение "{params[1]}"'
                                    )

                                elif params[0] not in settings.get(
                                    str(peer_id - 2000000000)
                                ):
                                    message(f'параметра "{params[0]}" не существует!')

                                elif params[1] != "True" or params[1] != "False":
                                    message(
                                        f'значение "{params[1]}" для параметра "{params[0]}" невозможно!\nTrue или False'
                                    )

                            elif command.startswith("setToDefault"):
                                settings[str(peer_id - 2000000000)] = {
                                    "captcha_on": "False",
                                    "casino_on": "True",
                                    "greeting_on": "True",
                                    "wife": "True",
                                    "qr": "True",
                                    "math": "True",
                                    "rate": "True",
                                    "wiki": "True",
                                    "github": "True",
                                }

                                with open(
                                    f"{Path.home()}/.config/librespeak_bot/chatSettings.json",
                                    "w",
                                ) as f:
                                    json.dump(settings, f)
                                settingsStr = ""

                                for value, param in settings.get(
                                    str(event.message.peer_id - 2000000000)
                                ).items():
                                    settingsStr += f"{value}   =>   {param}\n"
                                message(
                                    f"Настройки были успешно сброшены.\nТекущие настройки: \n{settingsStr}"
                                )

    # except Exception as error:
    #    print(str(error))
