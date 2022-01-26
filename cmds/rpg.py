import discord
from discord.ext import commands
from core.classes import Cog_Extension
from datetime import datetime
import json
import random
import csv

def doread(filea):
    with open(filea,'r',encoding='utf-8') as jfile:
        alines=[]
        t=jfile.readlines()
        for lines in t:
            alines.append(lines.strip('\n').strip(' ').split(','))
    return alines

def dorecord(file,text):
    with open(file,'a',encoding='utf-8') as opfile:
        opfile.writelines(f'\n{text}')

with open('csvfile\channel.json','r',encoding='utf-8') as jfile:
    gifs=json.load(jfile)

rpglist=doread('csvfile\\rpgweapon.csv')

available_channel=(935768359931371540,935471683911954512,641131990959259667)

boss_hp=0

class Rpg(Cog_Extension):
    @commands.command()
    async def hit(self,ctx):
        if ctx.channel.id in available_channel:
            #變數預設值
            global boss_hp
            textout=""
            killed=False
            critical=0
            combo=0
            intkiller=[]

            #BOSS空血時回血
            if boss_hp == 0:
                boss_hp = random.randint(500,1000)
            
            #傷害判定
            while critical <= 5 :
                #隨機武器
                WeaponResult=random.choice(rpglist)
                main1=WeaponResult[0]
                main2=WeaponResult[1]
                down=int(WeaponResult[2])
                up=int(WeaponResult[3])
                
                #隨機傷害
                if up == 0:
                    atk='?'
                else:
                    atk = random.randint(down,up)

                #輸出格式
                if atk=='?':                                      #無傷害
                    textout+=f'{main1}\n{main2}\n'
                elif atk<0:                                       #補血
                    textout+=f'{main1}{-(atk)}{main2}\n'
                    boss_hp-=atk
                elif main2 == "a":                                #不顯示傷害的武器
                    textout+=f'{main1}\n'
                    boss_hp-=atk
                else:
                    textout+=f'{main1}{atk}{main2}\n'             #所有其他武器
                    boss_hp-=atk

                #爆擊判定
                critical=random.randint(1,100)
                if critical <= 5 :
                    combo+=1
                    if combo%3==1:
                        textout+="緊接著"
                    elif combo%3==2:
                        textout+="然後"
                    else:
                        textout+="再來"

            #剩餘血量&訊息印出
            if boss_hp > 0:
                textout+=f'狛克還有{boss_hp}點血量！\n'
                await ctx.send(f'{ctx.author.mention}\n{textout}')
            else:
                killed=True
                boss_hp=0
                textout+=f'尾刀！狛克被變成了薩摩耶！\n'
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
        else:
            await ctx.send(f'本頻道不可使用此指令，或者沒有登錄此頻道。')
        

def setup(bot):
    bot.add_cog(Rpg(bot))