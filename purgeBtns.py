# prugeBtns.py

import os
import discord
from dotenv import load_dotenv
load_dotenv()

log = []

class Buttons(discord.ui.View):
    global view
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Yes",style=discord.ButtonStyle.red)
    async def red_button(self, ctx: discord.Interaction, button: discord.ui.Button):
        global log
        adRoleId = int(os.getenv('ADMINROLE'))
        adRole = ctx.guild.get_role(adRoleId)
        if ctx.user.roles.__contains__(adRole):
            embPurged = discord.Embed(title="Purge", description=f"Succesfully purged {ctx.channel.name}", color=discord.Color.red())
            channel = ctx.channel
            view = Buttons()
            view.clear_items()
            async for message in channel.history():
                if not message == ctx.message:
                    await message.delete(delay=1)
            print(f"<{ctx.user}> purged <{ctx.channel}>")
            log.append(f"<{ctx.user}> purged <{ctx.channel}>")
            await ctx.response.edit_message(embed=embPurged, view=view)

    @discord.ui.button(label="No",style=discord.ButtonStyle.green)
    async def green_button(self, ctx: discord.Interaction, button: discord.ui.Button):
        global log
        adRoleId = int(os.getenv('ADMINROLE'))
        adRole = ctx.guild.get_role(adRoleId)
        if ctx.user.roles.__contains__(adRole):
            view = Buttons()
            view.clear_items()
            print(f"<{ctx.user}> didnt purge <{ctx.channel}>")
            log.append(f"<{ctx.user}> didnt purge <{ctx.channel}>")
            embNotPurged = discord.Embed(title="Purge", description="Purge aborted", color=discord.Color.green())
            await ctx.response.edit_message(embed=embNotPurged, view=view)


def logRet():
    global log
    return log