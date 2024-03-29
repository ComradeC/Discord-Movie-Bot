# db_commands.py

# external modules
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func

# local modules
from .models import MovieModel, QuoteModel, DowQuoteModel, MessageModel
from .settings import Session

def db_change_toxicity(message_id, amount, author, text):
    try:
        with Session() as session:
            if session.execute(select(MessageModel).where(MessageModel.id == message_id)).first():
                stmt = update(MessageModel).where(MessageModel.id == message_id) \
                    .values(toxicity=MessageModel.toxicity + amount) \
                    .returning(MessageModel.toxicity)
                result = session.execute(stmt)
                if result == 0:
                    db_delete("messages", message_id)
                else:
                    session.commit()
            else:
                message = MessageModel(id=message_id, author=author, text=text, toxicity=amount)
                session.add(message)
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
        elif db_name == "quotes":
            stmt = select(QuoteModel.text, QuoteModel.title, QuoteModel.timestamp)
            return session.execute(stmt)
        elif db_name == "messages":
            stmt = select(MessageModel.id, MessageModel.text, MessageModel.author, MessageModel.toxicity)
            return session.execute(stmt)


def db_delete(db_name=str, entity=str):
    try:
        with Session() as session:
            if db_name == "movies":
                stmt = delete(MovieModel).where(MovieModel.title == entity)
            elif db_name == "quotes":
                stmt = delete(QuoteModel).where(QuoteModel.text == entity)
            elif db_name == "messages":
                stmt = delete(MessageModel).where(MessageModel.id == entity)

            session.execute(stmt)
            session.commit()
    except SQLAlchemyError:
        return "Error"


def db_random_dow_quote():
    with Session() as session:
        random_quote = session.execute(select(DowQuoteModel.text).order_by(func.random())).fetchone()
    return random_quote[0]
