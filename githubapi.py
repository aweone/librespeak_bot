from requests import get
from json import loads


def getGitHubAccInfo(username):
    account = loads(get(f"https://api.github.com/users/{username}").text.replace("'", '`'))
    if "message" in account:
        return f"Ничего не найдено по запросу {username}"
    else:
        login = account["login"]
        name = account["name"]
        company = account["company"]
        location = account["location"]
        email = account["email"]
        bio = account["bio"]
        repos = account["public_repos"]
        followers = account["followers"]
        following = account["following"]

        msg = f"Логин: {login}\nИмя: {name}\nКомпания/Организация: {company}\nМесто: {location}\nПочта: {email}\nО себе: {bio}\nКол-во репозиториев: {repos}\nКол-во подписок: {following}\nКол-во подписчиков: {followers}\nПодробнее: github.com/{username}"
        return msg.replace("None", "N/A")



