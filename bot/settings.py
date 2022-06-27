# base modules
import os

# external modules
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
engine = create_engine('postgresql://' + os.environ['SQL_CONNECTION'] + '/postgres', echo=False, future=True)

Session = sessionmaker(engine)

