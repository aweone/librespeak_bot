import requests


_link = "https://evilinsult.com/generate_insult.php?lang=ru&type=json"


def insult():
    response = requests.get(_link)
    return response.json()["insult"]
