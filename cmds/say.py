import discord
from discord.ext import commands
from core.classes import Cog_Extension
from datetime import datetime
import json
import asyncio

with open('csvfile\channel.json','r',encoding='utf-8') as jfile:
    jchannel=json.load(jfile)

class Say(Cog_Extension):
    @commands.command()
    async def say(self,ctx):
        await ctx.message.delete()
        arg=ctx.message.clean_content[5:]
        await ctx.send(f'{arg}')

def setup(bot):
    bot.add_cog(Say(bot))