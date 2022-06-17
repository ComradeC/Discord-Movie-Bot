# id_lookup.py

# standard modules
import requests

# external modules
from bs4 import BeautifulSoup as Soupify
from fake_useragent import UserAgent
from sqlalchemy import select, update

# local modules
from website.models import MovieModel
from website.settings import Session


def title_to_query(title):
    query = title.replace(" ", "+").replace(",", "%2C")
    return query


def kp_id_lookup(title):
    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    response = requests.get(f"https://www.kinopoisk.ru/index.php?kp_query={title_to_query(title)}", headers=headers)
    if response.history:
        print(response.url)
        if response.url.strip("https://www.kinopoisk.ru/film/").isnumeric():
            kp_id = response.url.strip("https://www.kinopoisk.ru/film/")
        else:
            kp_id = None
    else:
        soup = Soupify(response.content, "html.parser")
        try:
            kp_id = soup.find("div", {"class": "element most_wanted"}).a["data-id"]
            kp_id = str(kp_id)
        except AttributeError:
            kp_id = None
    return kp_id


def imdb_id_lookup(title):
    data = requests.get(f"https://www.imdb.com/find?q={title_to_query(title)}")
    soup = Soupify(data.content, "html.parser")
    try:
        imdb_id = (soup.find("table", {"class": "findList"}).a["href"]).strip("/title/")
        return "tt" + str(imdb_id)
    except AttributeError:
        return None


# manual id lookup
if __name__ == '__main__':
    with Session() as session:
        stmt = select(MovieModel.title).where((MovieModel.kp_id == None) | (MovieModel.imdb_id == None))
        db_data = session.execute(stmt).scalars()
        for entry in db_data:
            print(entry)
            kp_id_real = kp_id_lookup(entry)
            imdb_id_real = imdb_id_lookup(entry)
            print(kp_id_real, imdb_id_real)
            session.execute(update(MovieModel).where(MovieModel.title == entry).values(kp_id=kp_id_real, imdb_id=imdb_id_real))
        session.commit()
