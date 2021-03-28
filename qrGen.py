import qrcode
import vk_api
from auth import vk

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

