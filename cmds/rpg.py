import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random
import csv

def numnum(a):
    try:
        int(a)
    except:
        return False
    else:
        return True

def doread(filea):
    with open(filea,'r',encoding='utf-8') as jfile:
        alines=[]
        t=jfile.readlines()
        for lines in t:
            alines.append(lines.strip('\n').strip(' ').split(','))
    return alines

def readitem(list):
    res=[]
    res.append(list[2].strip('\n').strip(' ').split(';'))
    return res

def dorecord(file,text):
    with open(file,'a',encoding='utf-8') as opfile:
        opfile.writelines(f'\n{text}')

def removeend(file):
    with open(file,'r',encoding='utf-8') as opfile:
        a=opfile.read()
    b=a.split("\n")
    t="\n".join(b[:-1])
    with open(file,'w+',encoding='utf-8') as opfile:
        for i in range(len(t)):
            opfile.write(t[i])

def doblank(file):
    with open(file,'w',encoding='utf-8') as opfile:
        opfile.writelines('0,0')

damagerec="csvfile\\damagerec.csv"
item="csvfile\\item.csv"

with open('csvfile\channel.json','r',encoding='utf-8') as jfile:
    gifs=json.load(jfile)

rpglist=doread('csvfile\\rpgweapon.csv')

available_channel=(935768359931371540,935471683911954512,641131990959259667)

boss_hp=0
hpfirst=0

class Rpg(Cog_Extension):
    @commands.command()
    async def hit(self,ctx,arg1=''):
        if ctx.channel.id in available_channel:
            #變數預設值
            global boss_hp
            global hpfirst
            textout=""
            killed=False
            critical=0
            combo=0
            intkiller=[]
            hpwas=0
            overkill=False

            #BOSS空血時回血
            if boss_hp == 0:
                boss_hp = random.randint(500,1000)
                doblank(damagerec)
                hpfirst=boss_hp

            #紀錄原本的血量
            hpwas=boss_hp
            
            #傷害判定
            while critical <= 5 :
                #隨機武器
                WeaponResult=random.choice(rpglist)
                main1=WeaponResult[0]
                main2=WeaponResult[1]
                down=int(WeaponResult[2])
                up=int(WeaponResult[3])
                lastshot=0
                
                if boss_hp<=0:
                    overkill=True
                    lastshot+=atk

                #隨機傷害
                if up == 0:
                    atk='?'
                else:
                    atk = random.randint(down,up)

                #輸出格式
                if atk=='?':                                      #無傷害
                    textout+=f'{main1}\n{main2}\n'
                    atk=0
                elif atk<0:                                       #補血
                    textout+=f'{main1}{-(atk)}{main2}\n'
                    boss_hp-=atk
                    hpwas-=atk
                elif main2 == "a":                                #不顯示傷害的武器
                    textout+=f'{main1}\n'
                    boss_hp-=atk
                else:
                    textout+=f'{main1}{atk}{main2}\n'             #所有其他武器
                    boss_hp-=atk

                #紀錄輸出
                damagelist=doread(damagerec)
                damagename=[]
                damagenumber=[]
                for a in damagelist:
                    damagename.append(int(a[0]))
                    damagenumber.append(int(a[1]))
                if ctx.author.id in damagename:
                    v=damagename.index(ctx.author.id)
                    damagenumber[v]+=atk
                    doblank(damagerec)
                    for b in range(1,len(damagename)):
                        dorecord(damagerec,f"{damagename[b]},{damagenumber[b]}")
                else:
                    dorecord(damagerec,f"{ctx.author.id},{atk}")

                #爆擊判定
                critical=random.randint(1,100)
                if critical <= 5 :
                    combo+=1
                    if overkill:
                        textout+="鞭屍！"
                    else:
                        if combo%3==1:
                            textout+="緊接著"
                        elif combo%3==2:
                            textout+="然後"
                        else:
                            textout+="再來"

            #剩餘血量&訊息印出
            if boss_hp > 0:
                #textout+=f'狛克還有{boss_hp}點血量！\n'
                if hpwas >= 500 and boss_hp < 500:
                    textout+=f'狛克看起來有點虛弱！\n'
                if hpwas >= 300 and boss_hp < 300:
                    textout+=f'狛克看起來非常的虛弱！\n'
                if hpwas >= 100 and boss_hp < 100:
                    textout+=f'狛克看起來已經沒有力氣掙扎了！\n'
                if hpwas <= 100 and boss_hp > 100:
                    textout+=f'狛克他重新站起來了！\n'
                if hpwas <= 1000 and boss_hp > 1000:
                    textout+=f'狛克感到了前所未有的亢奮！\n'
                await ctx.send(f'{ctx.author.mention}\n{textout}')
            else:
                killed=True
                boss_hp=0
                textout+=f'尾刀！狛克被變成了薩摩耶！\n'
                mvp=damagename[damagenumber.index(max(damagenumber))]
                partofhp=round((max(damagenumber)-lastshot-atk+hpwas)/hpfirst*100,1)
                #if partofhp >100:
                    #partofhp=100
                textout+=f'本次BOSS輸出之MVP為<@{mvp}>，輸出率為{partofhp}%\n'
                hahahalol=discord.File(random.choice(gifs["samoyed"]))
                await ctx.send(f'{ctx.author.mention}\n{textout}',file=hahahalol)

            if killed:
                dorecord("csvfile\\killed.csv",ctx.author.id)
                history=doread("csvfile\\killed.csv")
                for a in history:
                    intkiller.append(int(a[0]))
                userkills=intkiller.count(ctx.author.id)
                if userkills %5 == 0 and userkills != 0:
                    await ctx.send(f'{ctx.author.mention}\n恭喜！您已經把狛克變成薩摩耶{userkills}次！')
                if len(intkiller) %10 == 1:
                    await ctx.send(f'{ctx.author.mention}\n恭喜！您是第{len(intkiller)-1}個把狛克變成薩摩耶的玩家！')
            #掉落寶物
            users=[]
            itemrawdata=doread(item)
            for rawdata in itemrawdata:
                users.append(int(rawdata[0]))
            id=ctx.author.id
            roll_dice=random.randint(1,100)
            while combo != 0:
                roll_dice+=random.randint(1,20)
                combo-=1
            they_get_it=False
            how_many=0
            mvp_get_it=False
            if killed:
                if int(roll_dice/80)>0:
                    they_get_it=True
                    how_many=int(roll_dice/80)
                    mvp_dice=random.randint(1,100)
                    if mvp_dice>90:
                        mvp_get_it=True
            else:
                if int(roll_dice/95)>0 :
                    they_get_it=True
                    how_many=int(roll_dice/95)
            if they_get_it:
                await ctx.send(f'{ctx.author.mention}\n您獲得了{how_many}顆雪狼牙！')
                if id in users:
                    available_tooth=int(itemrawdata[users.index(id)][1])
                    available_tooth+=how_many
                    itemrawdata[users.index(id)][1]=available_tooth
                    with open(item,'w',encoding='utf-8') as opfile:
                        for a in itemrawdata:
                            opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
                    removeend(item)
                else:
                    dorecord(item,f'{id},{how_many},0')
            if mvp_get_it:
                await ctx.send(f'<@{mvp}>\n您獲得了1顆雪狼牙！')
                if mvp in users:
                    available_tooth=int(itemrawdata[users.index(mvp)][1])
                    available_tooth+=1
                    itemrawdata[users.index(mvp)][1]=available_tooth
                    with open(item,'w',encoding='utf-8') as opfile:
                        for a in itemrawdata:
                            opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
                    removeend(item)
                else:
                    dorecord(item,f'{mvp},1,0')
        else:
            await ctx.send(f'本頻道不可使用此指令，或者沒有登錄此頻道。')

    @commands.command()
    async def bosskill(self,ctx):
        intkiller=[]
        history=doread("csvfile\\killed.csv")
        for a in history:
                    intkiller.append(int(a[0]))
        await ctx.send(f'{ctx.author.mention}\n狛克已經變成薩摩耶{len(intkiller)-1}次了！')

    @commands.command()
    async def mykill(self,ctx):
        intkiller=[]
        history=doread("csvfile\\killed.csv")
        for a in history:
                    intkiller.append(int(a[0]))
        userkills=intkiller.count(ctx.author.id)
        await ctx.send(f'{ctx.author.mention}\n您目前已經把狛克變成薩摩耶{userkills}次了！')

    @commands.command()
    async def showhp(self,ctx):
        global boss_hp
        if boss_hp == 0:
            boss_hp = random.randint(500,1000)
            doblank(damagerec)
        await ctx.send(f'{ctx.author.mention}\n你拿起偵測儀對著狛克一陣亂拍。\n偵測儀顯示狛克現在還有{boss_hp}點血量！')

    @commands.command()
    async def gatcha(self,ctx,arg='1'):
        users=[]
        outmes=""
        itemrawdata=doread(item)
        for rawdata in itemrawdata:
            users.append(int(rawdata[0]))
        id=ctx.author.id
        if id in users:
            available_tooth=int(itemrawdata[users.index(id)][1])
            if arg.isdecimal:
                if available_tooth >= int(arg):
                    available_tooth-=int(arg)
                    itemrawdata[users.index(id)][1]=available_tooth
                    turns=int(arg)
                    outmes+=f"抽取{turns}次！\n"
                    while turns != 0:
                        itemrawdata[users.index(id)][2]+=f';(獎品)'
                        turns-=1
                        outmes+="你抽到了(獎品)！\n"
                    with open(item,'w',encoding='utf-8') as opfile:
                        for a in itemrawdata:
                            opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
                    removeend(item)
                    await ctx.send(f'{ctx.author.mention}\n{outmes}')
                else:
                    await ctx.send(f'{ctx.author.mention}\n您似乎沒有足夠的雪狼牙呢-w-...')
            else:
                await ctx.send(f'{ctx.author.mention}\n轉蛋次數請輸入整數-w-...')
        else:
            await ctx.send(f'{ctx.author.mention}\n您似乎一顆雪狼牙都還沒取得呢-w-...')


def setup(bot):
    bot.add_cog(Rpg(bot))