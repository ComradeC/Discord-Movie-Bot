# base modules
import os

# external modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
KP_TOKEN = os.environ['KP_TOKEN']
engine = create_engine(os.environ['SQL_CONNECTION'], echo=True, future=True)

Session = sessionmaker(engine)

