from sqlalchemy import create_engine, Column, Integer, String, Time, Boolean, select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies_db"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    watched_status = Column(Boolean)

    kp_id = Column(Integer)
    imdb_id  = Column(Integer)

    def __repr__(self):
        return f"Movie(id={self.id!r}, title={self.title!r})"


class Quote(Base):
    __tablename__ = "quotes_db"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    timestamp = Column(Time)
    title = Column(String)

    def __repr__(self):
        return f"Quote(id={self.id!r}, text={self.text!r}, title={self.title!r}, timestamp={self.timestamp!r})"


engine = create_engine('postgresql://Commi:1537@localhost:5432/postgres', echo=True, future=True)
Base.metadata.create_all(engine)  # For db creation


# adding movie to DBs
def db_add_movie(title):
    with Session(engine) as session:
        try:
            movie = Movie(title=title, watched_status=False)
            session.add(movie)
            session.commit()
        except SQLAlchemyError:
            return "Error"


def db_add_quote(text, title, timestamp):
    with Session(engine) as session:
        try:
            quote = Quote(text=text, title=title, timestamp=timestamp)
            session.add(quote)
            session.commit()
        except SQLAlchemyError:
            return "Error"


def db_select(db_name, *args):
    with Session(engine) as session:
        if db_name == "movies":
            if args:
                if args[0].lower() == "all":
                    stmt = select(Movie.title)
            else:
                stmt = select(Movie.title).where(Movie.watched_status == "False")
            return session.execute(stmt).scalars()
        elif db_name == "quotes":
            return session.query(Quote).with_entities(Quote.text, Quote.title, Quote.timestamp)


def db_delete(db_name, entity):
    with Session(engine) as session:
        try:
            if db_name == "movies":
                stmt = delete(Movie).where(Movie.title == entity).returning(Movie.title)
            elif db_name == "quotes":
                stmt = delete(Quote).where(Quote.text == entity).returning(Quote.text)

            result = session.execute(stmt)
            print(result.rowcount)
            if result.rowcount == 0:
                print(result.rowcount)
                return "Error"
            session.commit()
        except SQLAlchemyError:
            return "Error"


def db_movie_set_watched(entity):
    with Session(engine) as session:
        try:
            stmt = update(Movie).where(Movie.title == entity).values(watched_status=True).returning(Movie.title)
            result = session.execute(stmt)
            if result.rowcount == 0:
                return "Error"
            session.commit()
        except SQLAlchemyError:
            return "Error"

