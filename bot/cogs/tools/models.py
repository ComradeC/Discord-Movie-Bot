from sqlalchemy import Column, Integer, String, Boolean, Time, BigInteger
from sqlalchemy.orm import declarative_base
from .settings import engine

Base = declarative_base()


class MovieModel(Base):
    __tablename__ = "movies_db"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    watched_status = Column(Boolean)

    kp_id = Column(String)
    imdb_id = Column(String)

    def __repr__(self):
        return f"Movie(id={self.id!r}, title={self.title!r})"


class QuoteModel(Base):
    __tablename__ = "quotes_db"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    timestamp = Column(Time)
    title = Column(String)

    def __repr__(self):
        return f"Quote(id={self.id!r}, text={self.text!r}, title={self.title!r}, timestamp={self.timestamp!r})"


class UserModel(Base):
    __tablename__ = "user_db"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r})"


class DowQuoteModel(Base):
    __tablename__ = "dow_quote_db"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)

    def __repr__(self):
        return f"DowQuote(id={self.id!r}, text={self.title!r})"


class MessageModel(Base):
    __tablename__ = "message_db"

    id = Column(BigInteger, primary_key=True)
    text = Column(String, nullable=False)
    author = Column(String, nullable=False)
    toxicity = Column(Integer)

    def __repr__(self):
        return f"Message(id={self.id!r}, text={self.text!r}, author={self.author!r}, toxicity={self.toxicity!r})"


if __name__ == '__main__':
    Base.metadata.create_all(engine)  # For db creation
