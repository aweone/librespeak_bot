from auth import vk
from sympy import symbols
from sympy.plotting import plot
from sympy.plotting import plot3d
import matplotlib.pyplot
import vk_api


def graph(expression):
    x = symbols(expression)
    image = plot(expression, show=False)
    image.save("graph.png")
    image = matplotlib.pyplot
    image.close()
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("graph.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    del x, image, upload, photo
    return attachment


def graph3d(expression):
    x = symbols(expression)
    image = plot3d(expression, show=False)
    image.save("graph.png")
    image = matplotlib.pyplot
    image.close()
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages("graph.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    del x, image, upload, photo
    return attachment

# for i in range(1, 100):
#    graph3d("3*x**y")
#    print(i)
