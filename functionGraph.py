from auth import vk
from sympy import symbols
from sympy.plotting import plot
from sympy.plotting import plot3d
import vk_api

def graph(expression):
    x = symbols(expression)
    plot(expression, show=False).save("graph.png")
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("graph.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment

def graph3d(expression):
    x = symbols(expression)
    plot3d(expression, show=False).save("graph.png")
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("graph.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment

#graph("2")
