import discord
from discord.ext import commands
from core.classes import Cog_Extension
import plotly.graph_objects as go
import json
import numpy as np

with open('C:\\Users\\user\\Desktop\\收納夾\\KomarouLetsPython\\SHProject\\csvfiles\\lahh.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

class Lah(Cog_Extension):
    @commands.command()
    async def calc(self,ctx,arg=""):

        if arg=="":
            outmes=f"輸入[k!calc (角色日文全名)]以取得LAH角色60級能力四維圖！"
            await ctx.send(f'{ctx.author.mention}\n{outmes}')
            return
    
        sixty_data=[]
        samestar_data=[]
        search_hero=arg
        search_success=False
        fixed_data=None

        for linesd in jdata:
            if linesd[5]=="1":
                lines=jdata[linesd]
                first_rank=lines["rarity"]
                last_num=7-first_rank
                linesk=jdata[linesd[:5]+str(last_num)]
                result=linesk["growths"][4]
                their_ability=[result["hp"],result["attack"],result["agility"],result["addView"]]
                sixty_data.append(their_ability)
                if linesk["cardName"]==search_hero:
                    search_success=True
                    fixed_data=their_ability
                    stars=first_rank
                    imagenamee=linesk["stockId"]
        if not search_success:
            await ctx.send(f'{ctx.author.mention}\n我們找不到{arg}這隻英雄，請檢查看看輸入的是不是正確的角色日文全名-w-...')
            return
        for linesd in jdata:
            if linesd[5]=="1":
                if jdata[linesd]["rarity"] == stars:
                    last_num=7-stars
                    result=jdata[linesd[:5]+str(last_num)]["growths"][4]
                    samestar_data.append([result["hp"],result["attack"],result["agility"],result["addView"]])

        maxi=[]
        smal=[]
        meaan=[]

        for v in range(4):
            b=[]
            for a in sixty_data:
                b.append(a[v])
            maxi.append(max(b))
            smal.append(min(b))

        for v in range(4):
            b=[]
            for a in samestar_data:
                b.append(a[v])
            meaan.append(round(sum(b)/len(b),4))

        if fixed_data:
            the_printin_data=fixed_data
            asss=np.array(the_printin_data)
            bsss=np.array(maxi)
            csss=np.array(smal)
            dsss=np.array(meaan)
            percentage=(asss-csss)/(bsss-csss)*100
            mean_star=(dsss-csss)/(bsss-csss)*100
            perc=list(np.around(percentage,2))

            categories = [f"HP({perc[0]})",f"ATK({perc[1]})",f"SPD({perc[2]})",f"View({perc[3]})"]
            categories = [*categories, categories[0]]

            restaurant_1 = percentage
            restaurant_2 = [100,100,100,100]
            restaurant_3 = mean_star
            restaurant_1 = [*restaurant_1, restaurant_1[0]]
            restaurant_2 = [*restaurant_2, restaurant_2[0]]
            restaurant_3 = [*restaurant_3, restaurant_3[0]]


            fig = go.Figure(
                data=[
                    go.Scatterpolar(r=restaurant_1, theta=categories, fill='toself', name=f'{search_hero}'),
                    go.Scatterpolar(r=restaurant_2, theta=categories, line_color = 'lightslategrey' ,name='極值'),
                    go.Scatterpolar(r=restaurant_3, theta=categories, line_color = 'orange' ,name='同星均值'),
                ],
                layout=go.Layout(
                    title=go.layout.Title(text=f'{search_hero}的60級四圍表'),
                    polar={'radialaxis': {'visible': True}},
                    showlegend=True
                )
            )

            fig.write_image(f"temporary//fig{imagenamee}.png")
            outfile=discord.File(f"temporary//fig{imagenamee}.png")
            await ctx.send(f'{ctx.author.mention}\n',file=outfile)

#Bot設定區

def setup(bot):
    bot.add_cog(Lah(bot))