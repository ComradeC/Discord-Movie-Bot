# db_commands.py

# external modules
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func

# local modules
from .models import MovieModel, QuoteModel, DowQuoteModel
from .settings import Session


def db_add_movie(title, kp_id, imdb_id):
    try:
        with Session() as session:
            movie = MovieModel(title=title, watched_status=False, kp_id=kp_id, imdb_id=imdb_id)
            session.add(movie)
            session.commit()
    except SQLAlchemyError:
        return "Error"


def db_add_quote(text, title, timestamp):
    try:
        with Session() as session:
            quote = QuoteModel(text=text, title=title, timestamp=timestamp)
            session.add(quote)
            session.commit()

    except SQLAlchemyError:
        return "Error"


def db_select(db_name):
    with Session() as session:
        if db_name == "movies":
            stmt = select(MovieModel.title).where(MovieModel.watched_status == "False")
            return session.scalars(stmt)
        else:
            stmt = select(QuoteModel.text, QuoteModel.title, QuoteModel.timestamp)
            return session.execute(stmt)


def db_select_all():
    with Session() as session:
        result = session.execute(select(MovieModel.title, MovieModel.watched_status))
        return result


def db_delete(db_name, entity):
    try:
        with Session() as session:
            if db_name == "movies":
                stmt = delete(MovieModel).where(MovieModel.title == entity).returning(MovieModel.title)
            else:
                stmt = delete(QuoteModel).where(QuoteModel.text == entity).returning(QuoteModel.text)

            result = session.execute(stmt)
            if result.rowcount == 0:
                return "Error"
            session.commit()
    except SQLAlchemyError:
        return "Error"


def db_movie_set_watched(entity):
    try:
        with Session() as session:
            stmt = update(MovieModel).where(MovieModel.title == entity).values(watched_status=True).returning(MovieModel.title)
            result = session.execute(stmt)
            if result.rowcount == 0:
                return "Error"
            session.commit()
    except SQLAlchemyError:
        return "Error"


def db_movie_set_not_watched(entity):
    try:
        with Session() as session:
            stmt = update(MovieModel).where(MovieModel.title == entity).values(watched_status=False).returning(MovieModel.title)
            result = session.execute(stmt)
            if result.rowcount == 0:
                return "Error"
            session.commit()
    except SQLAlchemyError:
        return "Error"


def db_random_dow_quote():
    with Session() as session:
        random_quote = session.execute(select(DowQuoteModel.text).order_by(func.random())).fetchone()
    return random_quote[0]