# bot.py
# version 0.2beta

import json
import requests
import os
from cogs import twitch_integration
from cogs import quotes_commands
from cogs import movies_commands
from discord.ext import commands

from dotenv import load_dotenv



load_dotenv()

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


