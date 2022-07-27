import discord
from discord.ext import commands
import json
import random
import os
import csv
import asyncio

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

with open('C:\\Users\\user\\Documents\\GitHub\\basically_what\\token.json','r',encoding='utf-8') as jfile:
    token_file=json.load(jfile)

intents = discord.Intents.all() # enables all intents
bot = commands.Bot(command_prefix='k!',intents=intents,case_insensitive=True)

tra=[]

def do_pss(a,b):
    if a==b:
        return "0"
    elif a+b==4:
        return "b" if a==3 else "a"
    else:
        return "b" if a<b else "a"

#@bot.command()
#async def agyour18(ctx):
    #pic=random.choice(jdata['PIC18'])
    #ag=discord.File(pic)
    #await ctx.send(file=ag)


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
            return
    #if '森' in msg.content and '盤' in msg.content and ('爾' in msg.content or '噁' in msg.content) and msg.author != bot.user:
        #addd=discord.File('C:\\Users\\user\\Documents\\GitHub\\KomarouBot\\goodplate.jpg')
        #await msg.channel.send(file=addd)
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
    bot.load_extension(F'cmds.{extension}')
    await ctx.send(F"領域{extension} 出現了")

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(F'cmds.{extension}')
    await ctx.send(F"領域{extension} 消失了")

@bot.command()
async def reload(ctx,extension):
    bot.reload_extension(F'cmds.{extension}')
    await ctx.send(F"領域{extension} 洗好了")

#Bot設定區

@bot.event
async def on_ready():
    print('>>Bot Online.<<')
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name="狛克被人狂揍猛揍")
    await bot.change_presence(status= status_w, activity=activity_w)

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')
if __name__ == "__main__":
    bot.run(token_file['TOKEN'])