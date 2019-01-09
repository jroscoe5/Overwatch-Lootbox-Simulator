# file: overwatchdiscordbot.py
# desc: A bot for the VOIP app discord that simulates opening
#       lootboxes in the PC game Overwatch

import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import json
from pprint import pprint
import random

# File containing the bot's secret token
token_filename = "tokens\\token.dat"

# The bot will only react to command messages that are prefaced by this
command_prefix = "!"

# Description of the bot
description = "Discord bot that simulates opening lootboxes"

# File for log output
log_filename = "logs\\log_" + str(datetime.now().date())+ ".dat"

# Files for items
epic_filename = "items\\epic.json"
rare_filename = "items\\rare.json"
common_filename = "items\\common.json"
legendary_filename = "items\\legendary.json"

# Site that hosts the images for us lmao
image_host_prefix = "https://overwatchitemtracker.com/resources"

# Compounded Lootbox Probabilities in range [0,1]
prob_common = 0.5820
prob_rare = 0.8990
prob_epic = 0.9745
prob_legend = 1

# Discord emojis that represent rarity
icon_common = ":grey_exclamation:"
icon_rare = ":small_blue_diamond:"
icon_epic = ":purple_heart:"
icon_legend = ":large_orange_diamond:"

# Load the items
list_epic = json.load(open(epic_filename, "r"))["items"]
list_rare = json.load(open(rare_filename, "r"))["items"]
list_common = json.load(open(common_filename, "r"))["items"]
list_legendary = json.load(open(legendary_filename, "r"))["items"]

bot = commands.Bot(command_prefix=command_prefix, description=description)
log_file = open(log_filename, "a")

# Generate 4 random items representing a lootbox
def genItems():
    items = []
    rare_gen = False
    for _ in range(4):
        rarity = genRarity()
        if(not rare_gen and rarity != icon_common):
            rare_gen = True
        if rarity == icon_common:
            item = random.choice(list_common)
            items.append((rarity, item["id"], item["url"]))
        elif rarity == icon_rare:
            item = random.choice(list_rare)
            items.append((rarity, item["id"], item["url"]))
        elif rarity == icon_epic:
            item = random.choice(list_epic)
            items.append((rarity, item["id"], item["url"]))
        else:
            item = random.choice(list_legendary)
            items.append((rarity, item["id"], item["url"]))      
    if not rare_gen:
        item = random.choice(list_rare)
        items[random.randint(0,3)] = (icon_rare, item["id"], item["url"])
    return items

# Generate a rarity and return the emoji representing that rarity
def genRarity():
    roll = random.random()
    if roll < prob_common:
        return icon_common
    elif roll < prob_rare:
        return icon_rare
    elif roll < prob_epic:
        return icon_epic
    else:
        return icon_legend

# Logs all the bot's interactions to a stream
def log(string):
	# print(str(datetime.now()) + " : " + string)
    print(str(datetime.now()) + " : " + string, file = log_file)
    log_file.flush()

# Retrieves the bot's secret token from a file
def retrieveToken():
    handle = open(token_filename, "r")
    return handle.readline()

# Called after bot.run when bot is ready for commands
@bot.event
@asyncio.coroutine
def on_ready():
    log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    log("Bot starting . . .")
    log("Logged in as: " + bot.user.name)
    log("Client ID: " + bot.user.id)
    game = discord.Game(name=("Type " + command_prefix + "info for commands."))
    yield from bot.change_presence(game=game, status=discord.Status.online)

# Simulates opening a lootbox
@bot.command(pass_context=True)
@asyncio.coroutine
def lootbox(ctx):
    author = str(ctx.message.author)
    items = genItems()
    log(author + " is opening a lootbox.")
    embed = discord.Embed(color=0x9932cc)
    embed.add_field(name=items[0][0], value= "[" + items[0][1] + "](" +image_host_prefix + items[0][2] + ")", inline=True)
    embed.add_field(name=items[1][0], value= "[" + items[1][1] + "](" +image_host_prefix + items[1][2] + ")", inline=True)
    embed.add_field(name="You opened a lootbox!", value = "click the links to view the items you found", inline=False)
    embed.add_field(name=items[2][0], value= "[" + items[2][1] + "](" +image_host_prefix + items[2][2] + ")", inline=True)
    embed.add_field(name=items[3][0], value= "[" + items[3][1] + "](" +image_host_prefix + items[3][2] + ")", inline=True)
    yield from bot.reply("", embed=embed)

# Info about the bot
@bot.command(pass_context=True)
@asyncio.coroutine
def info(ctx):
    author = str(ctx.message.author)
    log(author + " is requesting info")
    embed = discord.Embed(title = "Info", color=0xffa500, description= 
                        "This bot lets you open imaginary Overwatch lootboxes.\n"+
                        "Currently the supported only commands are as follows:\n\n"+
                        command_prefix + "info -------- displays this message\n"+
                        command_prefix + "lootbox ----- opens a lootbox\n\n"+
                        "Planned features include mass opening, inventory tracking, and keeping a count of the boxes opened for each user\n\n"
                        "Source code located [here](https://github.com/jroscoe5/Overwatch-Lootbox-Simulator) (feel free to clean up my ugly code)"
                        )
    yield from bot.say(embed=embed)

if __name__ == "__main__":
	print("Logging to: " + log_filename)
	bot.run(retrieveToken())