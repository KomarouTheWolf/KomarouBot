import discord
from discord.ext import commands
from core.classes import Cog_Extension
from discord import Embed
import json
import random
import asyncio
from discord.ui import Button,View

ex_perc=0

def coffeepack(a,ctx):
    embedmes=  discord.Embed(description=a)
    embedmes.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    return embedmes
def new_coffeepack(info,color,ctx):
    embedmes=  discord.Embed(description=info,colour=color)
    embedmes.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    return embedmes

def intr_coffeepack(info,color,intr):
    embedmes=  discord.Embed(description=info,colour=color)
    embedmes.set_author(name=intr.user.display_name, icon_url=intr.user.display_avatar.url)
    return embedmes

#可以呼叫指令的button
class ClCmdBton(Button):
    def __init__(self, label:str, emoji:str, commandf, ctxg):
        super().__init__(style=discord.ButtonStyle.green, emoji=emoji, label=label)
        self.ctx=ctxg
        self.command=commandf

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author==interaction.user:
            await self.view.clickdead()
            await interaction.response.defer()
            await self.ctx.invoke(self.command)
        else:
            await interaction.response.defer()

#可以呼叫指令的View
class OneButtonCmdView(View):
    def __init__(self, label:str, emoji:str, commandk ,ctxf):
        super().__init__(timeout=180)
        self.add_item(ClCmdBton(label, emoji, commandk,ctxf))
        self.org_mes=None

    async def clickdead(self):
        for btns in self.children:
            btns.disabled=True
            btns.style=discord.ButtonStyle.gray
        await self.org_mes.edit(view=self) 

    async def on_timeout(self):
        for btns in self.children:
            btns.disabled=True

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

        slfcmd= self.bot.get_command("drink")
        theView=OneButtonCmdView("再一杯！","🍹",slfcmd,ctx)

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
            await outemb.edit(embed=new_coffeepack(outmes,orangered,ctx),view=theView)
        else:
            ex_perc+=1
            outmes+=f'\n狛克 :「久等了！這是給你的！」 \n狛克把調製好的飲品推到你面前。'
            await outemb.edit(embed=new_coffeepack(outmes,lightgreen,ctx),view=theView)
        theView.org_mes=outemb
            
    @commands.command()
    async def toast(self,ctx):
        global ex_perc
        rarity=0
        tsttype=""
        lightgreen=0x90EE90
        silver=0xC0C0C0
        orangered=0xFF4500
        with open('csvfile\coffee.json','r',encoding='utf-8') as jfile:
            cofeefile=json.load(jfile)

        slfcmd= self.bot.get_command("toast")
        theView=OneButtonCmdView("再一份！","🍞",slfcmd,ctx)

        #第一次(純歡迎)
        outmes=f'你向狛克要了一份神秘吐司。\n狛克 : 「{random.choice(cofeefile["toast"]["welcome"])}」\n'
        outemb= await ctx.send(f"{ctx.author.mention}",embed=new_coffeepack(outmes,silver,ctx))
        await asyncio.sleep(2)
        
        #比重隨機
        rd_toast = lambda kind : random.choices(list(cofeefile["toast"][kind].keys()),weights=[cofeefile["toast"][kind][ele][0] for ele in cofeefile["toast"][kind]])[0]

        #決定吐司種類
        toast_kind=rd_toast("toast")
        outmes+=f'狛克先放了{toast_kind}在盤子上。\n'
        rarity+=cofeefile["toast"]["toast"][toast_kind][1]
        await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
        await asyncio.sleep(2)

        #厚片吐司專用
        if toast_kind=="一片厚片吐司":
            flavor=rd_toast("thick")
            outmes+=f'接著，狛克在吐司上{flavor}。\n'
            rarity+=cofeefile["toast"]["thick"][flavor][1]
            flvrname=cofeefile["toast"]["thick"][flavor][2]
            await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
            await asyncio.sleep(2)

            #額外口味
            thckjam=random.randint(1,100)>80
            if thckjam:
                secflavor=rd_toast("jam")
                secflavor_txt=secflavor.replace("抹上","抹上更多的") if secflavor==flavor else secflavor
                outmes+=f'心血來潮的狛克，在吐司上{secflavor_txt}。\n'
                rarity+=cofeefile["toast"]["jam"][secflavor][1]
                flvrname+=cofeefile["toast"]["jam"][secflavor][2]
                await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
                await asyncio.sleep(2)

            outmes+=f'狛克將做好的厚片吐司，沿著對角線劃上兩刀。\n'
            await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
            await asyncio.sleep(2)
        #普通吐司
        else:
            #決定種類
            tsttype=random.choices(["jamed","ingr","ingrjamed","white"],weights=[10,70,19,1])[0]

            if "jamed" in tsttype:
                jamtype=random.choices(["single","doubled"],weights=[80,20])[0]
                if jamtype == "single":
                    jam=rd_toast("jam")
                    outmes+=f'接著，狛克在兩片吐司上各{jam}。\n'
                    await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
                    await asyncio.sleep(2)
                    rarity+=cofeefile["toast"]["jam"][jam][1]
                    flvrname=cofeefile["toast"]["jam"][jam][2]
                elif jamtype == "doubled":
                    jam1=rd_toast("jam")
                    jam2=jam1
                    while jam2 == jam1:
                        jam2=rd_toast("jam")
                    outmes+=f'接著，狛克在其中一片吐司上{jam1}。\n'
                    await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
                    await asyncio.sleep(2)
                    outmes+=f'然後在另外一片吐司上，{jam2.replace("抹上","抹上了")}。\n'
                    await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
                    await asyncio.sleep(2)
                    rarity+=cofeefile["toast"]["jam"][jam1][1]+cofeefile["toast"]["jam"][jam2][1]
                    flvrname=cofeefile["toast"]["jam"][jam1][2]+cofeefile["toast"]["jam"][jam2][2]
            else:
                flvrname=""
        
            if "ingr" in tsttype:
                lettucedice=random.randint(1,100)>20
                tmtdice=random.randint(1,100)>80

                if lettucedice and tmtdice:
                    rarity+=15
                    lttmtmes=f'狛克切了一些番茄與生菜，放在吐司上。'
                elif lettucedice:
                    rarity+=5
                    lttmtmes=f'狛克放了些生菜在吐司上。'

                if lettucedice:
                    outmes+=f'然後，{lttmtmes}\n' if "接著" in outmes else f'接著，{lttmtmes}\n'
                    await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
                    await asyncio.sleep(2)
                

                multin,ingrdc,numofingr=1.0,True,0
                while ingrdc:
                    ingrdc=random.choices([True,False],cum_weights=[multin,1.0])[0]
                    multin*=0.33
                    numofingr+=1

                raw_ingrlst=[]
                for _ in range(numofingr):
                    rd_ingr=rd_toast("side")
                    raw_ingrlst.append(rd_ingr)
                    rarity+=cofeefile["toast"]["side"][rd_ingr][1]
                
                eggdice=random.randint(1,100)>60
                if eggdice:
                    raw_ingrlst.append("放上一片煎蛋")
                    rarity+=10
                
                for counts in range(len(raw_ingrlst)):
                    ingredients=raw_ingrlst[counts]
                    if ingredients == "放上一整顆高麗菜":       #店長出沒
                        ingrmes=f'黑野店長突然出現，並在吐司上{ingredients}'
                    else:
                        ingrmes=f'狛克在吐司上{ingredients}'
                    ingrmes=ingrmes.replace("在吐司上","在吐司上又") if ingredients in outmes else ingrmes
                    conjunc="最後" if counts==len(raw_ingrlst)-1 and counts!=0 else random.choice(["之後","然後","不急不徐地"])
                    outmes+=f'{conjunc}，{ingrmes}。\n'
                    await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
                    await asyncio.sleep(2)

                ingr={}
                for ingredients in set(raw_ingrlst):
                    ingr[cofeefile["toast"]["side"][ingredients][2]]=raw_ingrlst.count(ingredients)
                
                
                clubbed=any(["雞" in outmes,"豬" in outmes,"牛" in outmes]) and ("培根" in ingr) and lettucedice and tmtdice
                if clubbed:
                    del ingr["培根"]

                numdict={1:"",2:"雙倍",3:"三重",4:"四倍"}
                for ingrtype in [cofeefile["toast"]["side"][ele][2] for ele in cofeefile["toast"]["side"]]:
                    if ingrtype in ingr:
                        if ingrtype=="蛋" and clubbed:
                            continue
                        flvrname+=f'{numdict.get(ingr[ingrtype],"海量")}{ingrtype}'
                
                if clubbed:
                    flvrname+="總匯"
                    rarity+=25

            if tsttype=="white":
                flvrname="烤"
            
            outmes+=f'狛克將放好配料的兩片吐司面對面闔上。\n' if tsttype!="white" else f'狛克將兩片香噴噴的烤吐司面對面闔上。\n'
            sandwiched=random.randint(1,100)>50
            if sandwiched:
                outmes+=f'再將做好的吐司沿著對角線，切成四份後立起來。\n'
                rarity+=5
            await outemb.edit(embed=new_coffeepack(outmes,silver,ctx))
            await asyncio.sleep(2)
            
        if rarity<=15:
            rarname="UR"
        elif rarity<=40:
            rarname="N"
        elif rarity<=80:
            rarname="R"
        elif rarity<=120:
            rarname="SR"
        elif rarity<=180:
            rarname="**SSR**"
        elif rarity<=220:
            rarname="**SSSR**"
        else:
            rarname="**SSSSR**"

        toast_shape = "三明治" if toast_kind!="一片厚片吐司" and sandwiched else "吐司"

        ex_perc=149 if ex_perc==150 else ex_perc
        secretdice=random.randint(1,150-ex_perc)
        robbedbywolf=random.randint(1,25)==1
        if secretdice == 1:
            ex_perc=0
            outmes+=f'\n狛克 :「久等了！這是給......」\n結果狛克不小心記錯，把{toast_shape}拿給別人了。'
            await outemb.edit(embed=new_coffeepack(outmes,orangered,ctx),view=theView)
        elif robbedbywolf and "巧克" in flvrname:
            outmes+=f'\n狛克 :「久等了！這是給......嗚哇啊啊啊！」\n巧克布從吧檯裡冒出來，把你的{toast_shape}咬走了。'
            await outemb.edit(embed=new_coffeepack(outmes,orangered,ctx),view=theView)
        elif robbedbywolf and "鮪魚" in flvrname:
            outmes+=f'\n狛克 :「久等了！這是給......啊啊啊！」\n一隻柴碗蒸出來把你的{toast_shape}頂走了。'
            await outemb.edit(embed=new_coffeepack(outmes,orangered,ctx),view=theView)
        elif "蛋" in flvrname and toast_shape == "三明治" and robbedbywolf:
            outmes+=f'\n狛克 :「久等了！這是給......欸欸欸！」\n希澈突然衝出來，把你的{toast_shape}叼走了。'
            await outemb.edit(embed=new_coffeepack(outmes,orangered,ctx),view=theView)
        elif robbedbywolf and "熱狗" in flvrname:
            outmes+=f'\n狛克 :「久等了！這是給......回來啊喂！」\n{toast_shape}裡的熱狗跟著熱狗跑掉了。'
            await outemb.edit(embed=new_coffeepack(outmes,orangered,ctx),view=theView)
        else:
            ex_perc+=1
            outmes+=f'\n狛克 :「久等了！這是給你的！」 \n狛克把做好的{toast_shape}推到你面前。\n'
            outmes+=f'你得到了[{rarname}]{flvrname}{cofeefile["toast"]["toast"][toast_kind][2]}{toast_shape}！'
            await outemb.edit(embed=new_coffeepack(outmes,lightgreen,ctx),view=theView)
        theView.org_mes=outemb
    

async def setup(bot):
    await bot.add_cog(Coffee(bot))