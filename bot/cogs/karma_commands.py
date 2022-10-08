# karma_commands.py

# default modules
import json
from datetime import datetime, timedelta

# external modules
from nextcord.ext import commands
import nextcord

overuse_dict = {}


def open_json():
    try:
        with open("storage/karma.json", "r") as j:
            karma_dict = json.loads(j.read())
    except FileNotFoundError:
        karma_dict = {"karma": {}, "bananas": {}}
    return karma_dict


def write_json(karma_dict):
    with open("storage/karma.json", "w") as j:
        j.write(json.dumps(karma_dict, indent=4))


def overuse_change(username, change_value):
    if username in overuse_dict.keys():
        overuse_dict[username] += change_value
    else:
        overuse_dict[username] = change_value


def karma_change(karma_dict, user, change_value):
    if user.name not in karma_dict["karma"].keys():
        karma_dict["karma"][user.name] = 0
    karma_dict["karma"][user.name] += change_value


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
            # we don't dis our bots here
            elif msg_author.bot is True:
                if reaction.emoji.name == "toxic":
                    await reaction.member.send("Yeah, F you too!")
                else:
                    pass
            else:
                # karma abuse protection
                karma_dict = open_json()
                if reaction.emoji.name == "toxic":
                    overuse_change(reaction.member.name, 1)
                else:
                    overuse_change(reaction.member.name, -1)

                # check if user is bananed
                if reaction.member.name in karma_dict["bananas"].keys():
                    # unbanana timeout check
                    if datetime.now() - datetime.strptime(karma_dict["bananas"][reaction.member.name],
                                                          "%Y-%m-%d %H:%M:%S") > timedelta(24 * 3600):
                        karma_dict["bananas"].pop(reaction.member.name)
                        await channel.send(f"{reaction.member.name} no longer bananed")
                        if reaction.emoji.name == "toxic":
                            karma_change(karma_dict, msg_author, 1)
                        else:
                            karma_change(karma_dict, msg_author, -1)
                # check if the user *should* be banned
                elif overuse_dict[reaction.member.name] >= 10:
                    karma_dict["bananas"][reaction.member.name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    karma_change(karma_dict, reaction.member, 10)
                    await channel.send(f"{reaction.member.name} gets a banana and 10 toxic points!")

                # finally calc karma change
                else:
                    if reaction.emoji.name == "toxic":
                        karma_change(karma_dict, msg_author, 1)
                    else:
                        karma_change(karma_dict, msg_author, -1)

                write_json(karma_dict)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        if reaction.emoji.name == "toxic" or reaction.emoji.name == "non_toxic":
            channel = self.bot.get_channel(reaction.channel_id)
            msg_author = (await channel.fetch_message(reaction.message_id)).author
            if msg_author.id == reaction.user_id:
                pass
            else:
                # calculating karma
                karma_dict = open_json()

                if reaction.emoji.name == "toxic":
                    overuse_change(reaction.member.name, -1)
                else:
                    overuse_change(reaction.member.name, 1)

                if msg_author.name not in karma_dict["karma"].keys():
                    karma_dict["karma"][msg_author.name] = 0
                if reaction.emoji.name == "toxic":
                    karma_dict["karma"][msg_author.name] -= 1
                elif reaction.emoji.name == "non_toxic":
                    karma_dict["karma"][msg_author.name] += 1

                write_json(karma_dict)

    @nextcord.slash_command(name="karma",
                            guild_ids=[962235918150955008, 757218832111763557])
    async def karma(self, interaction: nextcord.Interaction):
        pass

    @karma.subcommand(description="Shows current toxicity levels")
    async def show(self, interaction: nextcord.Interaction):
        karma_dict = open_json()
        if karma_dict["karma"] == {}:
            await interaction.response.send_message("Toxicity level is zero. What's going on?")
        else:
            # sorting, descending order
            karma = dict(sorted(karma_dict["karma"].items(), key=lambda item: item[1], reverse=True))
            # getting the dict into printable format
            msg = "```The toxic top:\n" + "\n".join([f"  {k} = {v}" for k, v in karma.items()]) + "```"
            await interaction.response.send_message(msg)


def setup(bot):
    bot.add_cog(Karma(bot))
