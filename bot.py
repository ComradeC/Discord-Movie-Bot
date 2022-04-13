# bot.py
# version 0.2beta

import requests
import os
import nextcord
from cogs import movies_commands, quotes_commands, twitch_integration
from nextcord.ext import commands
from dotenv import load_dotenv
load_dotenv()

reqSession = requests.Session()

MovieBot = commands.Bot(command_prefix="!", intends=nextcord.Intents.default())

MovieBot.add_cog(twitch_integration.Integration(MovieBot))
MovieBot.add_cog(movies_commands.Movies(MovieBot))
MovieBot.add_cog(quotes_commands.Quotes(MovieBot))


@MovieBot.event
async def on_ready():
    print(f"{MovieBot.user} к бою готов!")


@MovieBot.command(name="hello", help="Поздоровайся, будь человеком")
async def hello(ctx):
    await ctx.send("Драсти")

MovieBot.run(os.getenv("DISCORD_TOKEN"))
