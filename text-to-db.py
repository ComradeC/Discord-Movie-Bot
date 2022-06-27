from bot.cogs.tools.settings import Session
from bot.cogs.tools import DowQuoteModel

with open("dow_quotes.txt", "r", encoding="utf-8") as file:
    modded_list = [entry[3:].rstrip("\n").lstrip() for entry in file.readlines()]


if __name__ == '__main__':
    with Session() as session:
        for element in modded_list:
            quote = DowQuoteModel(text=element)
            session.add(quote)
        session.commit()
