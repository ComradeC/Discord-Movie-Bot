# bot.py
# version 0.2beta

# standard modules
from nextcord import abc

import requests
import os
import nextcord
from dbcon import *

# external modules
from nextcord.ext import commands
from dotenv import load_dotenv

# cogs
from cogs import movies_commands, quotes_commands#, twitch_integration

load_dotenv()
reqSession = requests.Session()


#intends.members=True
#intends.reactions=True
MovieBot = commands.Bot(command_prefix="!", intends=nextcord.Intents.all())

#MovieBot.add_cog(twitch_integration.Integration(MovieBot))
MovieBot.add_cog(movies_commands.Movies(MovieBot))
MovieBot.add_cog(quotes_commands.Quotes(MovieBot))


@MovieBot.event
async def on_ready():
    print(f"{MovieBot.user} к бою готов!")

@MovieBot.event
async def on_reaction_add(reaction, user):
    #print(reaction)
    #print(reaction.message.content)
    if (user != MovieBot.user) and (reaction.emoji=='☑'):
        await reaction.message.channel.send(f'@Gulfik, подрубай {reaction.message.content}. Приятного просмотра.')
        cur = conn.cursor()
        cur.execute("update movies set watched=true where title=%s", [reaction.message.content])
        conn.commit()
        cur.close()

@MovieBot.event
async def on_reaction_remove(reaction, user):
    print('So, you have chosen oblivion.')
    await reaction.message.channel.send(f'So, you have chosen oblivion.')
    if (user != MovieBot.user):
        await reaction.message.channel.send(f'Увиденное не забудешь. Но я попробую.')
        cur = conn.cursor()
        cur.execute("update movies set watched=false where title=%s", [reaction.message.content])
        conn.commit()
        cur.close()

@MovieBot.event
async def on_raw_reaction_remove(payload):
    print(payload)
    channel = MovieBot.get_channel(payload.channel_id)
    if (MovieBot.get_user(payload.user_id) != MovieBot.user):
        await channel.send(f'Увиденное не забудешь. Но я попробую.')
        cur = conn.cursor()
        txt = await channel.fetch_message(payload.message_id)
        cur.execute("update movies set watched=false where title=%s", [str(txt.content)])
        conn.commit()
        cur.close()

@MovieBot.command(name="hello", help="Поздоровайся, будь человеком")
async def hello(ctx):
    await ctx.send("Драсти")

MovieBot.run(os.getenv("DISCORD_TOKEN"))
