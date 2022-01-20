import discord
from discord.ext import commands
import json

with open{'setting.json','r',encoding='utf-8'} as jfile:
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

bot.run(jdata['TOKEN'])