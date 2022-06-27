# db_commands.py

# external modules
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

# local modules
from .models import MovieModel, QuoteModel
from bot.settings import Session


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


def db_select(db_name, *args):
    with Session() as session:
        stmt = None
        if db_name == "movies":
            if args:
                if args[0].lower() == "all":
                    stmt = select(MovieModel.title)
            else:
                stmt = select(MovieModel.title).where(MovieModel.watched_status == "False")
        else:
            stmt = select(QuoteModel.text, QuoteModel.title, QuoteModel.timestamp)
        return session.scalars(stmt)


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
