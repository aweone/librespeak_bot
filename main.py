import vk_api, random, time, json, getpass
from PIL import Image, ImageDraw, ImageFont
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from auth import vk, longpoll, vkAdmin, GROUP_ID

username = getpass.getuser()


captcha_on = True

font = ImageFont.truetype('/usr/share/fonts/opentype/cantarell/Cantarell-Bold.otf', 110)
timeup=time.asctime()
ids_captcha={}
char_list=[]

for i in range(65, 91):
    char_list.append(chr(i))
for i in range(97, 123):
    char_list.append(chr(i))
for i in range(48, 58):
    char_list.append(chr(i))


def get_admin(peerid, groupid):
    admins = []
    admins_str = ""
    members = vk.messages.getConversationMembers(peer_id=peerid, group_id=groupid)["items"]
    for member in members:
        if "is_admin" in member:
            admins.append(member["member_id"])
            if member["member_id"] > 0:
                admins_str+=("\n @id"+str(member["member_id"]))
            #print(member["member_id"])
    #print(members)
    return admins_str, admins


def get_captcha():
    captcha=""
    for i in range(6):
        captcha+=random.choice(char_list)

    print(captcha)

    im = Image.open("/home/{}/Pictures/captcha.jpg".format(username))
    im1 = Image.open("/home/{}/Pictures/captcha4.jpg".format(username))
    im2 = Image.open("/home/{}/Pictures/captcha5.jpg".format(username))
    im3 = Image.open("/home/{}/Pictures/captcha6.jpg".format(username))
    im4 = Image.open("/home/{}/Pictures/captcha2.jpg".format(username))
    im5 = Image.open("/home/{}/Pictures/captcha7.jpg".format(username))
    draw_text = ImageDraw.Draw(im)
    wText, hText = draw_text.textsize(captcha, font)
    wIm, hIm = im.size
    #print(wIm, hIm, wText, hText)
    draw_text.text(
        ((wIm-wText)/2, 160),
        str(captcha),
        font=font,
        fill=(0,0,0,128)
        )
    Image.blend(Image.blend(Image.blend(Image.blend(Image.blend(im, im1, 50), im2, 50), im3 , 50), im4, 50),im5 , 50).save('/home/{}/Pictures/captcha3.jpg'.format(username))

    im.save('/home/{}/Pictures/captcha1.jpg'.format(username))


    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("/home/{}/Pictures/captcha3.jpg".format(username))
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    #vk.messages.send(peer_id=event.peer_id, random_id=0, attachment=attachment)
    print(attachment)
    return attachment, captcha



while 1:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print((event.t))
                #print(event.object)         
                    #print
                    #vk.messages.send(peer_id=event.peer_id, message = captcha_value[1], random_id=random.randint(1,999999), attachment=captcha_value[0])
                    
                    #if event.raw[6].get("source_act") == "chat_invite_user_by_link":
                if (
                    captcha_on and
                    "action" in event.object["message"] and 
                    event.object["message"]["action"]["type"] == "chat_invite_user_by_link"
                ):

                    vk.messages.send(
                        peer_id=event.object["message"]["peer_id"], 
                        message=("новый [id"+str(event.object["message"]["from_id"])+"|пользователь] присоединился по ссылке"), 
                        random_id=random.randint(1,999999)
                    )
                    print("новый юзер")
                        #   if event.object["message"]["text"] == "1234":
                    captcha_value = get_captcha()
                    vk.messages.send(
                        peer_id=event.object["message"]["peer_id"], 
                        message="пройдите капчу или кик", 
                        random_id=random.randint(1,999999), 
                        attachment=captcha_value[0]
                    )
                    ids_captcha[str(event.object["message"]["from_id"])]=captcha_value[1]

                    #print(ids_captcha)

                        
                elif (
                    str(event.object["message"]["from_id"]) in ids_captcha and
                    event.object["message"]["text"] == ids_captcha[str(event.object["message"]["from_id"])]
                ):

                    ids_captcha.pop(str(event.object["message"]["from_id"]))
                    vk.messages.send(
                        peer_id=event.object["message"]["peer_id"], 
                        message = "проверка пройдена", 
                        random_id=random.randint(1,999999)
                    )


                    #print( ids_captcha[str(event.user_id)] )
                elif (
                    str(event.object["message"]["from_id"]) in ids_captcha and
                    event.object["message"]["text"] != ids_captcha[str(event.object["message"]["from_id"])]
                ):

                    ids_captcha.pop(str(event.object["message"]["from_id"]))

                    vk.messages.send(
                        peer_id=event.object["message"]["peer_id"], 
                        message = "пошел нахуй фурриеб", 
                        random_id=random.randint(1,999999)
                    )

                    vk.messages.removeChatUser(
                        chat_id=event.object["message"]["peer_id"]-2000000000, 
                        user_id=event.object["message"]["from_id"]
                    )

                    if event["message"]["peer_id"] == 2000000001:
                        vkAdmin.groups.ban(
                            group_id=GROUP_ID,
                            owner_id=event.object["message"]["from_id"]
                        )


                
                elif (
                    event.object["message"]["text"] == "/ban"
                ):
                    if (
                        event.object["message"]["from_id"] in get_admin(event.object["message"]["peer_id"], GROUP_ID)[1]
                    ):
                        if (
                            "reply_message" in event.object["message"]
                        ):
                            vk.messages.removeChatUser(
                                chat_id=event.object["message"]["peer_id"]-2000000000, 
                                user_id=event.object["message"]["reply_message"]["from_id"]
                            )
                        elif (
                            "fwd_messages" in event.object["message"]
                        ): 
                            vk.messages.removeChatUser(
                                chat_id=event.object["message"]["peer_id"]-2000000000, 
                                user_id=event.object["message"]["fwd_messages"][0]["from_id"]
                            )

                        vk.messages.send(
                            peer_id=event.object["message"]["peer_id"],
                            message="кикаю хохлинку...",
                            random_id=random.randint(1, 999999)
                        )
                    elif (
                        event.object["message"]["from_id"] not in get_admin(event.object["message"]["peer_id"], GROUP_ID)[1]
                    ):
                        vk.messages.send(
                            peer_id=event.object["message"]["peer_id"],
                            message="угомонись, хохлинка... кикать могут только админы",
                            random_id=random.randint(1, 999999)
                        )

                elif (
                    event.object["message"]["text"] == "/admins" and
                    event.object["message"]["from_id"] == 213045391
                ):

                    vk.messages.send(
                        peer_id=event.object["message"]["peer_id"],
                        message="админы данного чата: "+get_admin(event.object["message"]["peer_id"], GROUP_ID)[0],
                        random_id=random.randint(1,999999),
                        disable_mentions = 1
                    )

                
                elif (
                    event.object["message"]["attachments"] and
                    event.object["message"]["attachments"][0]["type"] == "audio_message" and
                    random.choices([True, False], weights = (25, 75), k=2)[0]
                    ):

                    vk.messages.send(
                        peer_id=event.object["message"]["peer_id"],
                        message = "хрю-хрю",
                        random_id=0
                    )

                elif (
                    "навальный" in event.object["message"]["text"].lower() and
                    random.choices([True, False], weights = (25, 75), k=2)[0]
                    ):
                    vk.messages.send(
                        peer_id=event.object["message"]["peer_id"],
                        random_id=0,
                        attachment="photo-202215029_457239052"
                    )
                
                elif (
                    "action" in event.object["message"]
                ):
                    if (
                        event.object["message"]["action"]["type"] == "chat_kick_user"
                    ):
                        vk.messages.send(
                            peer_id=event.object["message"]["peer_id"], 
                            message = "еще один [id"+str(event.object["message"]["action"]["member_id"])+"|хохол] покидает нас, ура!", 
                            random_id=random.randint(1,999999)
                        )

                    elif (
                        event.object["message"]["action"]["type"] == "chat_invite_user"
                    ):
                        vk.messages.send(
                            peer_id=event.object["message"]["peer_id"], 
                            message = "еще один [id"+str(event.object["message"]["action"]["member_id"])+"|хохол] присоединился...", 
                            random_id=random.randint(1,999999)
                        )

                elif (
                    event.object["message"]["from_id"] == 213045391
                ):


                    if (
                        event.object["message"]["text"] == "/инф"
                    ):

                        vk.messages.send(
                            peer_id=event.object["message"]["peer_id"], 
                            message="бот работает, аптайм c "+timeup, 
                            random_id=random.randint(1,999999)
                        )


                    elif (
                        event.object["message"]["text"] == "/капча"
                    ):
                        
                        captcha_value = get_captcha()
                        vk.messages.send(
                            peer_id=event.object["message"]["peer_id"], 
                            message=captcha_value[1], 
                            random_id=random.randint(1,999999), 
                            attachment=captcha_value[0]
                        )
                    elif (
                        event.object["message"]["from_id"] == 213045391 and
                        event.object["message"]["text"].split()[0] == "/exec"
                    ):

                        command = event.object["message"]["text"].replace("/exec ", "")
                        exec(str(command))
                        print(command)


    except Exception as error:
        print(error)
