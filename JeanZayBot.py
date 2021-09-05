import discord
from discord.ext import commands
from discord.utils import get
import time

def cooldown():0

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name="RSA | https://github.com/Askehraz/JeanZayBot"))

@client.event #Autorole
async def on_member_join(member):
    print(f'{member} has joined the server.')
    role = get(member.guild.roles, id=ADDTHEIDOFTHEROLE)
    await member.add_roles(role)

@client.event #QuoiFeur
async def on_message(message):
    stripped_message = message.content.lower().strip(" .:?!*\)")

    if stripped_message.endswith("quoi"):
        await message.channel.send("feur")

client.run('ADDTHEBOTTOKEN')
