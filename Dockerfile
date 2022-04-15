FROM python:3.10-slim
WORKDIR /app
RUN pip install discord.py
RUN pip install python-dotenv
RUN pip install requests
RUN pip install twitchAPI

COPY . .

CMD ["python3", "bot.py"]
