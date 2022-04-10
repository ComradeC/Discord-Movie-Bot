# main.py
# version 0.2beta

import requests
import os
from libs import twitch_integration
from libs import quotes_commands
from libs import movies_commands
from discord.ext import commands
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch

load_dotenv()

app_id = os.getenv("TWITCH_APP_TOKEN")
app_token = os.getenv("TWITCH_APP_ACCESS_TOKEN")

client_secret = os.getenv("TWITCH_CLIENT_SECRET")
client_id = os.getenv("TWITCH_CLIENT_ID")

twitch = Twitch(app_id, client_secret)
twitch.authenticate_app([])


API_HEADERS = {
    'Client-ID': app_id,
    'Authorization': 'Bearer '+app_token,
}

reqSession = requests.Session()

bot = commands.Bot(command_prefix="!")
bot.add_cog(twitch_integration.Integration(bot))
bot.add_cog(movies_commands.Movies(bot))
bot.add_cog(quotes_commands.Quotes(bot))


@bot.event
async def on_ready():
    print(f"{bot.user} к бою готов!")


@bot.command(name="hello", help="Поздоровайся, будь человеком")
async def hello(ctx):
    await ctx.send("Драсти")


bot.run(os.getenv("DISCORD_TOKEN"))
