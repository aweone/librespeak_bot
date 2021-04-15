from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from auth import vk
import random
import vk_api
import os
import string
from color_list import colors
from warnings import warn


username = str(Path.home())

char_list = []

for i in range(65, 91):
    char_list.append(chr(i))
for i in range(97, 123):
    char_list.append(chr(i))
for i in range(48, 58):
    char_list.append(chr(i))

font = ImageFont.truetype('font/Cantarell-Bold.otf', 110)


def __get_captcha():
    warn("Используется устаревший модуль")
    warn
    captcha = ""
    for _ in range(6):
        captcha += random.choice(char_list)

    print(captcha)

    im = Image.open("images/captcha.jpg")
    im1 = Image.open("images/captcha4.jpg")
    im2 = Image.open("images/captcha5.jpg")
    im3 = Image.open("images/captcha6.jpg")
    im4 = Image.open("images/captcha2.jpg")
    im5 = Image.open("images/captcha7.jpg")
    draw_text = ImageDraw.Draw(im)
    wText, _hText = draw_text.textsize(captcha, font)
    wIm, _hIm = im.size
    # print(wIm, hIm, _wText, _hText)
    draw_text.text(
        ((wIm-wText)/2, 160),
        str(captcha),
        font=font,
        fill=(0, 0, 0, 128)
    )
    Image.blend(
        Image.blend(
            Image.blend(
                Image.blend(
                    Image.blend(
                        im, im1, 50),
                    im2, 50),
                im3, 50),
            im4, 50),
        im5, 50).save('images/captcha3.jpg')

    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("images/captcha3.jpg")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    print(attachment)
    return attachment, captcha


chars = string.ascii_lowercase + string.digits


def get_captcha():
    n = 0
    font = ImageFont.truetype('font/Cantarell-Bold.otf', 70)
    captcha = ""
    for i in range(6):
        captcha += random.choice(chars)

    print(captcha)

    im = Image.new('RGBA', size=(400, 200), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    draw_text = ImageDraw.Draw(im)
    wText, _hText = draw_text.textsize(captcha, font)
    wIm, _hIm = im.size

    for i in captcha:
        fontName = 'font/' + random.choice(os.listdir(path="./font"))
        color = random.choice(colors)
        font = ImageFont.truetype(fontName, random.randint(65, 85))

        draw_text.text(
            ((wIm-wText)/2 - 10 + n, random.randint(60, 80)),
            str(i),
            font=font,
            fill=color
        )
        n += draw_text.textsize(i, font)[0]

    for i in range(0, random.randint(64, 128)):
        draw.line((
            random.randint(1, 600), random.randint(1, 400),
            random.randint(1, 600), random.randint(1, 400)),
            fill=random.choice(colors)

        )

    for i in range(0, random.randint(700, 1500)):
        x, y = random.randint(10, 800), random.randint(10, 400)
        eX, eY = 2, 2  # Size of Bounding Box for ellipse

        bbox = (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
        draw.ellipse((bbox), fill=random.choice(
            colors), outline=random.choice(colors))

    im.save("captcha.png", "PNG")
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("captcha.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    print(attachment)
    return attachment, captcha
