from requests import get
from json import loads

def ipsearch(ip):
    response = loads(get(f"http://ip-api.com/json/{ip}").text.replace("'",'"'))
    if response["status"] == "success":
        return f'IP: {response["query"]} Страна: {response["country"]}\nСубъект: {response["regionName"]}\nГород: {response["city"]}\nШирота: {response["lat"]}\nДолгота: {response["lon"]}'
    elif response["status"] == "fail":
        return "Ошибка. Невернаый запрос."
