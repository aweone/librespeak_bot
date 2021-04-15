from PIL import Image, ImageDraw, ImageFont, ImageColor
import random
import os
import string
from color_list import colors
from auth import vk
import vk_api


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
    wText, hText = draw_text.textsize(captcha, font)
    wIm, hIm = im.size

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
