import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

#正式指令區

class Main(Cog_Extension):
    @commands.command()
    async def ping(self,ctx):
        embedmes = discord.Embed(title="ping!", description=f'機器人目前ping值為{round(self.bot.latency*1000,1)}ms 高得跟鬼一樣',colour=0xff9999) 
        embedmes.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embedmes)
    
    @commands.command()
    async def helping(self,ctx):
        bsd=jdata["DES"]
        await ctx.message.channel.send(f'```{bsd}```')

    '''@commands.command()
    async def agyou(self,ctx):
        pic=random.choice(jdata['PIC'])
        ag=discord.File(pic)
        await ctx.send(file=ag)'''

#Bot設定區

async def setup(bot):
    await bot.add_cog(Main(bot))