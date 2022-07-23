import discord
from discord.ext import commands
from core.classes import Cog_Extension
from discord import Embed
import json
import random
import asyncio

ex_perc=0

def coffeepack(a,ctx):
    embedmes=  discord.Embed(description=a)
    embedmes.set_author(name=ctx.author.nick or ctx.author.name, icon_url=ctx.author.avatar_url)
    return embedmes
def new_coffeepack(info,color,ctx):
    embedmes=  discord.Embed(description=info,colour=color)
    embedmes.set_author(name=ctx.author.nick or ctx.author.name, icon_url=ctx.author.avatar_url)
    return embedmes

class Coffee(Cog_Extension):
    @commands.command()
    async def old_menu(self,ctx):
        a='''狛克 : 嗯?找本狼呀?先說好晚上沒有空唷?
說吧,今天的你想要什麼? 

====餐單====
k!Greentea ☞ 綠茶
k!Oolong ☞ 烏龍茶
k!Blacktea ☞ 紅茶
k!Espresso ☞ 黑咖啡
k!Americano ☞ 美式咖啡
k!Latte ☞ 拿鐵
k!Cappuccino ☞ 卡布其諾
k!Mocha ☞ 摩卡
k!Macchiatto ☞ 焦糖瑪奇朵
k!Vienna ☞ 維也納
k!Starburst ☞ 星爆
k!Druid ☞ 德魯伊
k!Kamui ☞ 卡姆伊(結凍的咖啡)
k!Fuusuke ☞ 風助(底部有隻黑糖狼的咖啡)'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def americano(self,ctx):
        a='''狛克 : 代表「清純」的美式，你也有面子點呀 :）
總而言之，做好了，給你吧(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def blacktea(self,ctx):
        a='''狛克 : 帶有香醇果香的紅茶，有如成熟可靠的大叔般，微苦之下，藏著柔甜的滋味…
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def cappuccino(self,ctx):
        a='''狛克 : 等等，代表「我愛你」的卡布其諾，你是要送人的嗎OAO
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def druid(self,ctx):
        a='''狛克 : 魔力不夠了嗎？
其實…也可以不用靠咖啡補魔力的…>w0
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def espresso(self,ctx):
        a='''狛克 : 「本色」的黑咖啡嗎？是我最喜歡的咖啡呢～
總而言之，做好了，給你吧(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def greentea(self,ctx):
        a='''狛克 : 清香飄逸的綠茶，就像獸太的單純天真，我可是非常喜歡綠茶的呢！
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def kamui(self,ctx):
        a='''狛克 : 那個，要找真的卡姆伊，去隔壁就好了唷？
很好奇你要結凍的咖啡幹嘛…
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def latte(self,ctx):
        a='''狛克 : 代表「隨心」的拿鐵呀，我很喜歡喝加了檸檬的拿鐵呢～
總而言之，做好了，給你吧(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def macchiatto(self,ctx):
        a='''狛克 : 代表「溫柔」的焦糖瑪奇朵，挺適合你的性格呢～
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def mocha(self,ctx):
        a='''狛克 : 代表「甜蜜」的摩卡，就像現在的我們兩個一樣吧+w+？
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def oolong(self,ctx):
        a='''狛克 : 稚氣未脫卻又帶點成熟的韻味，烏龍茶就像這裡許多精力旺盛的獸獸一樣呢～
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def starburst(self,ctx):
        a='''狛克 : 等等，你還好吧？昨天熬夜了嗎？
給我十秒就好！我立刻拿第二把刀！

總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def vienna(self,ctx):
        a='''狛克 : 雖然很甜很好喝，但是維也納代表著「獨自等待」呢。
你也……在等著某個誰嗎？
總而言之，做好了，給你吧～(遞'''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def fuusuke(self,ctx):
        a='''狛克 : 等…等等，你說你想要我嗎OAO?
那個…都說我晚上沒空了……
……沒事沒事，我，我是說，我也喜歡黑糖…
總而言之，做好了，趕快拿去喝啦//// '''
        embedmes=coffeepack(a,ctx)
        await ctx.send(f'{ctx.author.mention}',embed=embedmes)

    @commands.command()
    async def drink(self,ctx):
        global ex_perc
        lightgreen=0x90EE90
        silver=0xC0C0C0
        orangered=0xFF4500
        with open('csvfile\coffee.json','r',encoding='utf-8') as jfile:
            cofeefile=json.load(jfile)
        main=random.choice(cofeefile["drink"]["main"])
        side=random.choice(cofeefile["drink"]["side"])
        if side==main:
            side="更多的"+side
        else:
            side="少許"+side
        outmes=f'你向狛克要了一杯飲品。\n狛克 : 「{random.choice(cofeefile["drink"]["welcome"])}」\n'
        outemb= await ctx.send(f"{ctx.author.mention}",embed=new_coffeepack(outmes,silver,ctx))
        await asyncio.sleep(2)
        outmes+="\n"
        outmes+=f'狛克拿出了一個玻璃杯，倒了七分滿的{main}。\n'
        await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
        await asyncio.sleep(2)
        outmes+=f'接著狛克在杯中，緩緩的加入{side}，溫柔的攪拌均勻。\n'
        await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
        await asyncio.sleep(2)
        rd_plc=random.randint(1,100)
        def ssn():
            first_plc=random.choices(["cup","upper","inner"],weights=(len(cofeefile["drink"]["seasoning"]["cup"]),len(cofeefile["drink"]["seasoning"]["upper"]),len(cofeefile["drink"]["seasoning"]["inner"])))[0]
            seasoning=random.choice(cofeefile["drink"]["seasoning"][first_plc])
            if first_plc=="cup":
                mes=f'最後，狛克在杯緣放上了{seasoning}。\n'
            elif first_plc=="upper":
                mes=f'最後，狛克輕輕在飲品的上方{seasoning}。\n'
            elif first_plc=="inner":
                mes=f'最後，狛克在飲品裡放入{seasoning}。\n'
            return mes
        if rd_plc>10:
            frst=ssn()
            outmes+=frst
            await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
            await asyncio.sleep(2)
        if rd_plc>90:
            scnd=frst
            while scnd == frst:
                scnd=ssn()
            scnd=scnd.replace("最後","作為特殊招待")
            outmes+=scnd
            await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
            await asyncio.sleep(2)
        ex_perc=149 if ex_perc==150 else ex_perc
        secretdice=random.randint(1,150-ex_perc)
        if secretdice == 1:
            ex_perc=0
            outmes+=f'\n狛克 :「久等了！這是給你......啊啊啊啊！」 \n狛克把調製好的飲品打翻了。'
            await outemb.edit(embed=new_coffeepack(outmes,orangered,ctx))
        else:
            ex_perc+=1
            outmes+=f'\n狛克 :「久等了！這是給你的！」 \n狛克把調製好的飲品推到你面前。'
            await outemb.edit(embed=new_coffeepack(outmes,lightgreen,ctx))

def setup(bot):
    bot.add_cog(Coffee(bot))