# id_lookup.py

# standard modules
import requests

# external modules
from sqlalchemy import select, update

# local modules
from .models import MovieModel
from .settings import Session, KP_TOKEN


def kp_id_lookup(title):
    headers = {
        'X-API-KEY': KP_TOKEN,
        'Content-Type': 'application/json',
    }
    data = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={title}",
                        headers=headers).json()
    try:
        return data['films'][0]['filmId']
    except IndexError:
        return None


def imdb_id_lookup(kp_id):
    headers = {
        'X-API-KEY': KP_TOKEN,
        'Content-Type': 'application/json',
    }
    data = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{kp_id}", headers=headers).json()
    return data['imdbId']


def id_gather(title):
    kp_id = kp_id_lookup(title)
    if kp_id:
        imdb_id = imdb_id_lookup(kp_id)
    else:
        imdb_id = None
    return kp_id, imdb_id


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
