import discord
from discord.ext import commands
import json
import random
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

def numnum(a):
    try:
        int(a)
    except:
        return False
    else:
        return True

kills=0

class Zombie(Cog_Extension):
    @commands.command()
    async def dmg(self,ctx,arg1,arg2):
        try:
            zombie=int(arg1)
            player=int(arg2)
            damage=[]
            retmes=f'{zombie}b{player}='
            for count in range(1,zombie+1):
                damage.append(random.randint(1,player))
            for ppl in range(0,zombie):
                retmes+=f'{damage[ppl]}'
                if ppl != zombie-1:
                    retmes+=f','
            retmes+=f'\n統計結果:'
            for k in range(1,player+1):
                retmes+=f'\n{k}:{damage.count(k)}'
            await ctx.send(f'```{retmes}```')
        except:
            await ctx.send(f'```我不知道問題出在哪裡 但是這個指令無法正確執行```')

    @commands.command()
    async def dth(self,ctx,arg):
        global kills
        if numnum(arg):
            kills+=int(arg)
            emoji = '<:windwow:640946675078266911>'
            await ctx.message.add_reaction(emoji)
        if arg == "zero":
            kills=0
            await ctx.send(f'```擊殺數歸零```')
        if arg == "show":
            await ctx.send(f'```擊殺數為{kills}```')

    @commands.command()
    async def ban(self,ctx):
        aa=jdata["JOB"]
        oao=''
        bb=random.sample(aa,5)
        for a in bb:
            oao+=(a+" ")
        await ctx.message.channel.send(f'```{oao}```')

def setup(bot):
    bot.add_cog(Zombie(bot))