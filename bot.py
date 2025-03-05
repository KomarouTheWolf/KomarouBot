import discord
from discord.ext import commands, tasks
import datetime
from datetime import timedelta, timezone
import json
import random
import os
import csv
import asyncio
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

with open('C:\\Users\\user\\Documents\\GitHub\\basically_what\\token.json','r',encoding='utf-8') as jfile:
    token_file=json.load(jfile)

intents = discord.Intents.all() # enables all intents
bot = commands.Bot(command_prefix='k!',intents=intents,case_insensitive=True)

# 設定台灣時區
tz = timezone(timedelta(hours=8))

# 活動日期
events = {
    "統測": datetime.datetime(2025, 4, 26, tzinfo=tz),
    "分科": datetime.datetime(2025, 7, 11, tzinfo=tz),
}

# 目標頻道 ID
TARGET_CHANNEL_ID = 1319625155395321938

def do_pss(a,b):
    if a==b:
        return "0"
    elif a+b==4:
        return "b" if a==3 else "a"
    else:
        return "b" if a<b else "a"

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if msg.content.endswith('誰被咬') and msg.author != bot.user:
        try:
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
                    if a in tra:
                        ouo+=(str(a)+':'+str(tra.count(a))+'\n')
                    else:
                        ouo+=(str(a)+':0\n')
                await msg.channel.send(f'```{ouo}```')
        except:
                await msg.channel.send(f'```我不知道問題出在哪裡 但是這個指令無法正確執行```')
    if msg.content == '殭屍ban職業' and msg.author != bot.user:
        aa=jdata["JOB"]
        bb=random.sample(aa,5)
        oao=""
        for a in bb:
            oao+=(a+" ")
        await msg.channel.send(f'```{oao}```')
        if (msg.content.endswith('= 1') or  msg.content.endswith('1/1(最大/合計)')) and msg.author.id == 544462904037081138 and not '1d2' in msg.content:
            emoji='\U0001f972'
            await msg.add_reaction(emoji)
    await bot.process_commands(msg)

@bot.command()
async def load(ctx,extension):
    await bot.load_extension(F'cmds.{extension}')
    await ctx.send(F"領域{extension} 出現了")

@bot.command()
async def unload(ctx,extension):
    await bot.unload_extension(F'cmds.{extension}')
    await ctx.send(F"領域{extension} 消失了")

@bot.command()
async def reload(ctx,extension):
    await bot.reload_extension(F'cmds.{extension}')
    await ctx.send(F"領域{extension} 洗好了")

nowtime=datetime.time(hour = 8, minute = 0, tzinfo=tz)
# 每天早上 8 點發送活動倒數
@tasks.loop(time=nowtime)
async def daily_countdown():
    now = datetime.datetime.now(tz)
    message_lines = []

    for event_name, event_date in events.items():
        if now > event_date:
            message_lines.append(f"{event_name}：已經一天不剩了！")
        else:
            days_left = (event_date - now).days
            message_lines.append(f"{event_name}：還有 {days_left} 天！")

    message = "\n".join(message_lines)

    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        await channel.send(f"📅 今日倒數提醒：\n{message}")

@bot.command()
async def asd(ctx):
    now = datetime.datetime.now(tz)
    message_lines = []

    for event_name, event_date in events.items():
        if now > event_date:
            message_lines.append(f"{event_name}：已經一天不剩了！")
        else:
            days_left = (event_date - now).days
            message_lines.append(f"{event_name}：還有 {days_left} 天！")

    message = "\n".join(message_lines)
    await ctx.send(f"📅 今日倒數提醒：\n{message}")

@bot.event
async def on_ready():
    print('>>Bot Online.<<')
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name="狛克被人狂揍猛揍")
    await bot.change_presence(status= status_w, activity=activity_w)
    daily_countdown.start()

async def load_extensions():
    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cmds.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token_file['TOKEN'])

if __name__ == "__main__":
    asyncio.run(main())
