import discord
from discord.ext import commands
import json
import random

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

tra=[]

bot = commands.Bot(command_prefix='kmrzb')

@bot.event
async def on_ready():
    print('>>Bot Online.<<')

@bot.event
async def on_member_join(member):
    channel=bot.get.channel(681125167866707978)
    await channel.send(f'{member} join!')


@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000,1)}ms')

@bot.command()
async def agyou(ctx):
    pic=random.choice(jdata['PIC'])
    ag=discord.File(pic)
    await ctx.send(file=ag)

@bot.command()
async def agyour18(ctx):
    pic=random.choice(jdata['PIC18'])
    ag=discord.File(pic)
    await ctx.send(file=ag)

@bot.command()
async def dmg(ctx):
    a=ctx.content
    await ctx.send(f'{a}')

@bot.event
async def on_message(msg):
    if msg.content.endswith('殭屍計算bot出來玩') and msg.author != bot.user:
        a=msg.content
        b=a.strip('')
        c=b.split(',')
        ouo=''
        del c[-1]
        global tra
        tra=[]
        for itemsss in c:
            tra.append(int(itemsss))
        tra=sorted(tra)
        y=max(tra)
        tra.append(y+1)
        for a in range(1,y+1):
            ouo+=(str(a)+':'+str(tra.index(a+1)-tra.index(a))+'\n')
        await msg.channel.send(f'```{ouo}```')


bot.run(jdata['TOKEN'])