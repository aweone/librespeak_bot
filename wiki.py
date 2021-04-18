import wikipedia
from requests import get


def wiki(requestName, sentences=4):
    try:
        wikipedia.set_lang("ru")
        page = wikipedia.page(requestName)
        text = wikipedia.summary(requestName, sentences)
        title = page.title
        similar = "\n".join(wikipedia.search(requestName))
        url = get("https://clck.ru/--?url=" + page.url).text
    except Exception:
        return "По вашему запросу ничего не найдено!"

    return f"{title}\n{text}\nПодробнее: {url}\n\nПохожие запросы:\n{similar}"
