import qrcode
import vk_api
from auth import vk
from PIL import Image
from pyzbar.pyzbar import decode
import requests


def qrgen(data):
    img = qrcode.make(data)
    img.save("qrcode.png")

    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("qrcode.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    print(attachment)
    return attachment


def qrdecode(link):
    r = requests.get(link)
    with open('decodeqr.png', 'wb') as f:
        f.write(r.content)
    data = decode(Image.open('decodeqr.png'))
    if data:
        return data[0].data.decode("utf-8")
    elif data == []:
        return ""
