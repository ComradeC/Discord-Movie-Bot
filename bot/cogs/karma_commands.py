# karma_commands.py

# default modules
import json

# external modules
from nextcord.ext import commands
import nextcord


class Karma(commands.Cog, nextcord.ClientCog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Karma cog loaded successfully")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.emoji.name == "toxic" or reaction.emoji.name == "non_toxic":
            channel = self.bot.get_channel(reaction.channel_id)
            msg_author = (await channel.fetch_message(reaction.message_id)).author
            if msg_author.id == reaction.user_id:
                pass
            else:
                # calculating karma
                try:
                    with open("storage/karma.json", "r") as j:
                        karma_dict = json.loads(j.read())
                except FileNotFoundError:
                    karma_dict = {}

                if msg_author.name not in karma_dict.keys():
                    karma_dict[msg_author.name] = 0
                if reaction.emoji.name == "toxic":
                    karma_dict[msg_author.name] += 1
                elif reaction.emoji.name == "non_toxic":
                    karma_dict[msg_author.name] -= 1

                with open("storage/karma.json", "w") as j:
                    j.write(json.dumps(karma_dict, indent=4))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        if reaction.emoji.name == "toxic" or reaction.emoji.name == "non_toxic":
            channel = self.bot.get_channel(reaction.channel_id)
            msg_author = (await channel.fetch_message(reaction.message_id)).author
            if msg_author.id == reaction.user_id:
                pass
            else:
                # calculating karma
                try:
                    with open("storage/karma.json", "r") as j:
                        karma_dict = json.loads(j.read())
                except FileNotFoundError:
                    karma_dict = {}

                if msg_author.name not in karma_dict.keys():
                    karma_dict[msg_author.name] = 0
                if reaction.emoji.name == "toxic":
                    karma_dict[msg_author.name] -= 1
                elif reaction.emoji.name == "non_toxic":
                    karma_dict[msg_author.name] += 1

                with open("storage/karma.json", "w") as j:
                    j.write(json.dumps(karma_dict, indent=4))

    @nextcord.slash_command(name="karma",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def karma(self, interaction: nextcord.Interaction):
        pass

    @karma.subcommand(description="Shows current toxicity levels")
    async def show(self, interaction: nextcord.Interaction):
        try:
            with open("storage/karma.json", "r") as j:
                karma_dict = json.loads(j.read())
        except FileNotFoundError:
            karma_dict = {}
        if karma_dict == {}:
            await interaction.response.send_message("Toxicity level is zero. What's going on?")
        else:
            # sorting, descending order
            karma_dict = dict(sorted(karma_dict.items(), key=lambda item: item[1], reverse=True))
            # getting the dict into printable format
            msg = "```The toxic top:\n" + "\n".join([f"  {k} = {v}" for k, v in karma_dict.items()]) + "```"
            await interaction.response.send_message(msg)


def setup(bot):
    bot.add_cog(Karma(bot))
