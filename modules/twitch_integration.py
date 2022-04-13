# twitch_integration.py

import requests
import os
import time

from twitchAPI.oauth import refresh_access_token
from discord.ext import tasks, commands
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
load_dotenv()


app_id = os.getenv("TWITCH_APP_TOKEN")
app_token = os.getenv("TWITCH_APP_ACCESS_TOKEN")

client_secret = os.getenv("TWITCH_CLIENT_SECRET")
client_id = os.getenv("TWITCH_CLIENT_ID")
refresh_token = os.getenv("TWITCH_REFRESH_TOKEN")

new_token, new_refresh_token = refresh_access_token(refresh_token, client_id, client_secret)
twitch = Twitch(app_id, client_secret)
twitch.authenticate_app([])


API_HEADERS = {
    'Client-ID': app_id,
    'Authorization': 'Bearer '+new_token,
}

reqSession = requests.Session()


def check_user(username):
    url = 'https://api.twitch.tv/helix/streams?user_login='+username
    try:
        req = reqSession.get(url, headers=API_HEADERS)
        jsondata = req.json()
        if len(jsondata['data']) == 1:
            return True
        else:
            return False
    except Exception as e:
        global app_token
        global refresh_token
        print("Twitch login error. Trying to refresh app token.")
        try:
            app_token, refresh_token = refresh_access_token(refresh_token, client_id, client_secret)
        finally:
            print("Done")
        return False


class Integration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bratiki_watch.start()
        print("Integration cog loaded successfully")

    @tasks.loop(seconds=300)
    async def bratiki_watch(self):
        channel = self.bot.get_channel(962758647883116605)
        if check_user("bratiki94") is True:
            await channel.send("Братики онлайн. Делайте что хотите с этой информацией.")
            time.sleep(28500)
        else:
            time.sleep(1)


def setup(bot):
    bot.add_cog(Integration(bot))
