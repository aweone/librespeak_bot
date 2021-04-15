from PIL import Image
from pyzbar.pyzbar import decode
import requests


def qrdecode(link):
    r = requests.get(link)
    with open('decodeqr.png', 'wb') as f:
        f.write(r.content)
    data = decode(Image.open('decodeqr.png'))
    if data:
        return data[0].data.decode("utf-8")
    elif data == []:
        return ""
