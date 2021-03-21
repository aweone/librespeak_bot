from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from auth import vk
import random, vk_api

username = str(Path.home())

char_list=[]

for i in range(65, 91):
    char_list.append(chr(i))
for i in range(97, 123):
    char_list.append(chr(i))
for i in range(48, 58):
    char_list.append(chr(i))

font = ImageFont.truetype('font/Cantarell-Bold.otf', 110)


def get_captcha():
    captcha=""
    for i in range(6):
        captcha+=random.choice(char_list)

    print(captcha)

    im = Image.open("images/captcha.jpg")
    im1 = Image.open("images/captcha4.jpg")
    im2 = Image.open("images/captcha5.jpg")
    im3 = Image.open("images/captcha6.jpg")
    im4 = Image.open("images/captcha2.jpg")
    im5 = Image.open("images/captcha7.jpg")
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
    Image.blend(
            Image.blend(
                Image.blend(
                    Image.blend(
                        Image.blend(
                            im, im1, 50),
                        im2, 50),
                    im3 , 50),
                im4, 50),
            im5 , 50).save('images/captcha3.jpg'.format(username))

    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("images/captcha3.jpg")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    print(attachment)
    return attachment, captcha