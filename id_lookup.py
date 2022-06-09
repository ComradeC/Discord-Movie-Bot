import requests
from bs4 import BeautifulSoup as bs


def title_to_query(title):
    query = title.replace(" ", "+").replace(",", "%2C")
    return query


def kp_id_lookup(title):
    data = requests.get(f"https://www.kinopoisk.ru/index.php?kp_query={title_to_query(title)}")
    soup = bs(data.content, "html.parser")
    kp_id = soup.find("div", {"class": "element most_wanted"}).a["data-id"]
    return str(kp_id)


def imdb_id_lookup(title):
    data = requests.get(f"https://www.imdb.com/find?q={title_to_query(title)}")
    soup = bs(data.content, "html.parser")
    imdb_id = (soup.find("table", {"class": "findList"}).a["href"]).strip("/title/")
    return "tt" + str(imdb_id)
