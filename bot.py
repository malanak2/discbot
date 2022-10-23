# bot.py
# By malanak

from calendar import timegm
from datetime import datetime
from distutils.cmd import Command
from fileinput import filename
import json
import os
from os.path import exists
import platform
import random
from time import time
import shutil

from purgeBtns import Buttons
from purgeBtns import logRet

import discord
from discord import Client, app_commands, guild, Embed
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
rawJson = open('data.json')
data = json.load(rawJson)
log = []

intents = discord.Intents.all()
client = Client(intents=intents)
tree = app_commands.CommandTree(client)
guildId = os.getenv('GUILDID')
guild = discord.Object(id=guildId, type=guild)
adminRoleId = int(os.getenv('ADMINROLE'))
embNoPerms = Embed(title="Permission", description="You do not have the permissions to do this!", color=discord.Color.red())

@tree.command(name="ping", description="Returns bot latency and says pong!", guild=guild)
async def ping(ctx: discord.Interaction):
    global log
    embResp = Embed(title="🏓Pong!")
    embAdminResp = Embed(title="🏓Pong!", description=f"Bot latency is <{client.latency}> seconds")
    await ctx.response.send_message(embed=embResp)
    adminRole = ctx.guild.get_role(adminRoleId)
    if ctx.user.roles.__contains__(adminRole):
        await ctx.response.edit_message(embed=embAdminResp)

@tree.command(name="roll", description="Does something, nobody knows what!", guild=guild)
async def roll(ctx: discord.Interaction):
    global log
    num = random.randint(0, 100)
    print(f"number: {num}, user: {ctx.user.name}")
    log.append(f"number: {num}, user: {ctx.user.name}")
    try:
        match num:
            case 42:
                data["users"].append(ctx.user.name)
                with open("data.json", "w") as jsFile:
                    json.dump(data, jsFile)
                user = ctx.user
                role = ctx.guild.get_role(1030846154537177108)
                ifhasrole = ctx.user.roles.__contains__(role)
                log.append(f"<{ctx.user}> has rolled 42!")
                embRespWin = Embed(title="Roll", description=f"You have rolled 42, the answer to everything, on the 100-sided dice and won the **{role.name}** role!", color=discord.Color.red())
                embRespWinMore = Embed(title="Roll", description=f"You, **{ctx.user.name}**, have rolled 21 again! What a miracle!\n Sadly, there is no reward for that, at least not yet", color=discord.Color.yellow())
                if ifhasrole:
                    await ctx.response.send_message(embed=embRespWinMore)
                else:
                    await ctx.response.send_message(embed=embRespWin)
                    await user.add_roles(role)
            case _:
                embRespDef = Embed(title="Roll", description="Certainly did something, now on to figure out what.", color=discord.Color.yellow())
                await ctx.response.send_message(embed=embRespDef)
    except Exception as e:
        print(e)

    
@tree.command(name="addrole", description="Adds said role to mentioned guy", guild=guild)
async def addrole(ctx: discord.Interaction, user: discord.User, role: discord.Role):
    if ctx.user.roles.__contains__(ctx.guild.get_role(adminRoleId)):
        if not user.roles.__contains__(role):
            global log
            try:
                print(f"Added role <{role}> to <{user}>")
                log.append(f"Added role <{role}> to <{user}>")
                await user.add_roles(role)
                embAddRole = Embed(title="Role Manager", description=f"Added role {role.name} to {user.name}", color=discord.Color.green())
                await ctx.response.send_message(embed=embAddRole)
            except Exception as e:
                print(f"Not enough permissions to add role {role.name}")
                log.append(f"Not enough permisions to add role {role.name}")
                embNEP = Embed(title="Role Manager", description=f"I do not have the permissions to manage role {role.name}", color=discord.Color.red())
                await ctx.response.send_message(embed=embNEP)
        else:
            embUserNoRole = Embed(title="Role Manager", description=f"User {user.name} already has role {role.name}", color=discord.Color.red())
            await ctx.response.send_message(embed=embUserNoRole)
    else:
        await ctx.response.send_message(embed=embNoPerms)


@tree.command(name="removerole", description="Removes said role to mentioned guy", guild=guild)
async def addrole(ctx: discord.Interaction, user: discord.User, role: discord.Role):
    if ctx.user.roles.__contains__(ctx.guild.get_role(adminRoleId)):
        global log
        if user.roles.__contains__(role):
            try:
                print(f"Removed role <{role}> from <{user}>")
                log.append(f"Removed role <{role}> from <{user}>")
                await user.remove_roles(role)
                embRemRole = Embed(title="Role Manager", description=f"Removed role {role.name} from {user.name}", color=discord.Color.green())
                await ctx.response.send_message(embed=embRemRole)
            except Exception as e:
                if e == "'Member' object has no attribute 'remove_role'":
                    print("Internal error has occured in removerole command")
                    log.append("Internal error has occured in removerole command")
                    await ctx.response.send_message(f"Internal error, code \"001\"")
                else:
                    print(f"Not enough perms to add role {role.name}")
                    log.append(f"Not enough perms to add role {role.name}")
                    embNEP = Embed(title="Role Manager", description=f"I do not have the permissions to manage role {role.name}", color=discord.Color.red())
                    await ctx.response.send_message(embed=embNEP)
        else:
            embUserNoRole = Embed(title="Role Manager", description=f"User {user.name} doesn't have role {role.name}", color=discord.Color.red())
            await ctx.response.send_message(embed=embUserNoRole)
    else:
        await ctx.response.send_message(embed=embNoPerms)

@tree.command(name="purge", description="Removes messages from channel this command is used in!", guild=guild)
async def purge(ctx: discord.Interaction):
    global log
    if ctx.user.roles.__contains__(ctx.guild.get_role(adminRoleId)):
        embAsk = Embed(title="Purge", description="Are you sure?", color=discord.Color.red())
        await ctx.response.send_message(embed=embAsk, view=Buttons())
        print(f"<{ctx.user}> tried purging <{ctx.channel.name}>")
        log.append((f"<{ctx.user}> tried purging <{ctx.channel.name}>"))
    else:
        await ctx.response.send_message(embed=embNoPerms)

@tree.command(name="writelog", description="Writes log file", guild=guild)
async def writelog(ctx: discord.Interaction):
    global log
    adRole = ctx.guild.get_role(adminRoleId)
    if ctx.user.roles.__contains__(adRole):
        exlog = logRet()
        for x in exlog:
            log.append(x)
        if exists('./logs/latestlog.txt'):
            os.remove('./logs/latestlog.txt')
        timestamp = int(time())
        curdattime = datetime.fromtimestamp(timestamp)
        fileName = './logs/' + str(curdattime) + ".txt"
        leng = len(fileName)
        stra = []
        for x in fileName:
            stra.append(x)
        for x in range(0, leng):
            if stra[x] == ":":
                stra[x] = ";"
        finFileName = ''.join(stra)
        open('./logs/latestlog.txt', 'x')
        with open('./logs/latestlog.txt', 'w') as f:
            for line in log:
                f.write(f"{line}\n")
        with open(finFileName, 'w') as f:
            for line in log:
                f.write(f"{line}\n")
        embSucces = Embed(title="Logger", description="Succesfully logged log to file latestlog.txt")
        log = []
        await ctx.response.send_message(embed=embSucces)
    else:
        ctx.response.send_message(embed=embNoPerms)


@client.event
async def on_message(msg: discord.Message):
    global log
    timestamp = int(time())
    curdattime = datetime.fromtimestamp(timestamp)
    log.append(f"[{curdattime}] <{msg.author}> messaged <{msg.content}> in <{msg.channel}>")

@client.event
async def on_message_edit(msgB: discord.Message, msg: discord.Message):
    global log
    timestamp = int(time())
    curdattime = datetime.fromtimestamp(timestamp)
    log.append(f"[{curdattime}] <{msg.author}> edited message from <{msgB.content}> to <{msg.content}> in <{msg.channel}>")

@client.event
async def on_message_delete(msg: discord.Message):
    global log
    timestamp = int(time())
    curdattime = datetime.fromtimestamp(timestamp)
    log.append(f"[{curdattime}] <{msg.author}> deleted message <{msg.content}> in <{msg.channel}>")

@client.event
async def on_ready():
    await tree.sync(guild=guild)
    print(f"Logged in as {client.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()}, {platform.release()}, ({os.name})")
    print("-------------------")
client.run(TOKEN)
