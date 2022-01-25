import discord
from discord.ext import commands
from core.classes import Cog_Extension
from datetime import datetime
import json
import random
import csv

def docsv(filea):
    alines=[]
    t=filea.readlines()
    for lines in t:
        alines.append(lines.strip('\n').strip(' ').split(','))
    return alines

with open('csvfile\channel.json','r',encoding='utf-8') as jfile:
    gifs=json.load(jfile)

with open('csvfile\\rpgweapon.csv','r',encoding='utf-8') as jfile:
    rpglist=docsv(jfile)


boss_hp=0

class Rpg(Cog_Extension):
    @commands.command()
    async def hit(self,ctx):
        global boss_hp
        textout=""
        killed=False
        if boss_hp == 0:
            boss_hp = random.randint(500,1000)

        critical=0
        while critical <= 5 :
            WeaponResult=random.choice(rpglist)
            main1=WeaponResult[0]
            main2=WeaponResult[1]
            down=int(WeaponResult[2])
            up=int(WeaponResult[3])
            if up == 0:
                atk='?'
            else:
                atk = random.randint(down,up)

                if atk=='?':
                    textout+=f'{main1}\n{main2}\n'
                elif atk<0:
                    textout+=f'{main1}{-(atk)}{main2}\n'
                    boss_hp-=atk
                elif main2 == "a":
                    textout+=f'{main1}\n'
                    boss_hp-=atk
                else:
                    textout+=f'{main1}{atk}{main2}\n'
                    boss_hp-=atk
                critical=random.randint(1,100)
                if critical <= 5 :
                    textout+="緊接著"

        if boss_hp > 0:
            textout+=f'狛克還有{boss_hp}點血量！\n'
            await ctx.send(f'{ctx.author.mention}\n{textout}')
        else:
            boss_hp=0
            textout+=f'尾刀！狛克被變成了薩摩耶！\n'
            killed=True
            hahahalol=discord.File(random.choice(gifs["samoyed"]))
            await ctx.send(f'{ctx.author.mention}\n{textout}',file=hahahalol)
        

def setup(bot):
    bot.add_cog(Rpg(bot))