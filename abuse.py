from requests import get
from json import loads

def insult():
    response = loads(get("https://evilinsult.com/generate_insult.php?lang=ru&type=json").text.replace("'",'"'))
    return response["insult"]

