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
    async def say(self,ctx,arg,arg2=None):
        await ctx.message.delete()
        if arg2 in jchannel:
            channelcode=jchannel[arg2]
            channel=self.bot.get_channel(channelcode)
            await channel.send(f'{arg}')
        else:
            await ctx.send(f'{arg}')

def setup(bot):
    bot.add_cog(Say(bot))