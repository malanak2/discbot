import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
guildid = os.getenv('GUILDID')
guild = discord.Object(id=guildid, type=discord.guild) # type: discord.guild
intents =discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    tree.remove_command("ping")
    tree.remove_command("work")
    tree.remove_command("purge")
    tree.remove_command("addrole")
    tree.remove_command("removerole")
    print("Done")

client.run(token)