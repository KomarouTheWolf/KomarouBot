import discord
from discord.ext import commands
import json
import random

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

tra=[]
kills=0

bot = commands.Bot(command_prefix='kmrzb')

def numnum(a):
    try:
        int(a)
    except:
        return False
    else:
        return True


@bot.event
async def on_ready():
    print('>>Bot Online.<<')

@bot.command()
async def ping(ctx):
    await ctx.send(f'機器人目前ping值為{round(bot.latency*1000,1)}ms 高得跟鬼一樣')

@bot.command()
async def agyou(ctx):
    pic=random.choice(jdata['PIC'])
    ag=discord.File(pic)
    await ctx.send(file=ag)

#@bot.command()
#async def agyour18(ctx):
    #pic=random.choice(jdata['PIC18'])
    #ag=discord.File(pic)
    #await ctx.send(file=ag)

@bot.command()
async def dmg(ctx,arg1,arg2):
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

@bot.command()
async def dth(ctx,arg):
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

@bot.command()
async def ban(ctx):
    aa=jdata["JOB"]
    oao=''
    bb=random.sample(aa,5)
    for a in bb:
        oao+=(a+" ")
    await ctx.message.channel.send(f'```{oao}```')



@bot.event
async def on_message(msg):
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
        oao=''
        bb=random.sample(aa,5)
        for a in bb:
            oao+=(a+" ")
        await msg.channel.send(f'```{oao}```')
    if '森' in msg.content and '盤' in msg.content and ('爾' in msg.content or '噁' in msg.content) and msg.author != bot.user:
        addd=discord.File('C:\\Users\\user\\Documents\\GitHub\\KomarouBot\\goodplate.jpg')
        await msg.channel.send(file=addd)
    if msg.content.endswith('= 1') and msg.author.id == 544462904037081138 and not '1d2' in msg.content:
        emoji='\U0001f972'
        await msg.add_reaction(emoji)

    await bot.process_commands(msg)

bot.run(jdata['TOKEN'])