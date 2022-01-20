import discord
from discord.ext import commands
import json
import random

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

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


bot.run(jdata['TOKEN'])