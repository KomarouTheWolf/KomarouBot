import discord
from discord.ext import commands
from core.classes import Cog_Extension
from datetime import datetime
import json
import asyncio
import random
from discord.ui import Button,View

def do_pss(a,b):
    if a==b:
        return "0"
    elif a+b==4:
        return "b" if a==3 else "a"
    else:
        return "b" if a<b else "a"
    
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

with open('csvfile\channel.json','r',encoding='utf-8') as jfile:
    jchannel=json.load(jfile)
with open("csvfile\\ocgatcha.txt",'r',encoding='utf-8') as jfile:
    rawocgatcha=jfile.readlines()
    ocgatcha=[]
    for lines in rawocgatcha:
        ocgatcha.append(lines.strip('\n'))

def randgatcha(nam:str):
    outmes=""
    for _ in range(10):
        dice=random.randint(1,100)
        if dice >97:
            outmes+=f'**{random.choice([ele for ele in ocgatcha if ele.startswith("UR")])}{nam}**\n'
        elif dice >75:
            outmes+=f'{random.choice([ele for ele in ocgatcha if ele.startswith("SSR")])}{nam}\n'
        elif dice >40:
            outmes+=f'{random.choice([ele for ele in ocgatcha if ele.startswith("SR")])}{nam}\n'
        else:
            outmes+=f'{random.choice([ele for ele in ocgatcha if ele.startswith("R")])}{nam}\n'
    return outmes

class Say(Cog_Extension):
    @commands.command()
    async def say(self,ctx):
        await ctx.message.delete()
        arg=ctx.message.clean_content[5:]
        await ctx.send(f'{arg}')

    @commands.command()
    async def whatif(self,ctx):
        authr = ctx.author.display_name
        slfcmd= self.bot.get_command("whatif")
        theView=OneButtonCmdView("再十抽！","🪄",slfcmd,ctx)
        embedmes = discord.Embed(title="抽卡✨！", description=f'汪汪汪！正在幫你十連抽！',colour=0x800000)
        embedmes.set_author(name=authr, icon_url=ctx.author.display_avatar.url)
        orgmes = await ctx.send(content=f'{ctx.author.mention}',embed=embedmes)
        await asyncio.sleep(2)
        restxt=randgatcha(authr)
        resclr=0xFFE153 if "UR" in restxt else 0xff9999
        embedmes = discord.Embed(title="抽卡✨！", description=f'汪汪汪！這是你的十連抽結果！\n{restxt}',colour=resclr) 
        embedmes.set_footer(text="心動了嗎？該委託或畫出來了！")
        embedmes.set_author(name=authr, icon_url=ctx.author.display_avatar.url)
        await orgmes.edit(embed=embedmes,view=theView)
        theView.org_mes=orgmes

    @commands.Cog.listener()
    async def on_message(self, message):
        if ("烤吐司" in message.content or "烤土司" in message.content) and message.author.name!= "烤吐司機#0000":
            webhooks = await message.channel.webhooks()
            if webhooks:
                for webhook in webhooks:
                    await webhook.send("\*發射吐司\*", username="烤吐司機", avatar_url="https://images.plurk.com/67L8aTFP2WiiKypJ6wSqoj.png")
            else:
                webhook = await message.channel.create_webhook(name="烤吐司機")
                await webhook.send("\*發射吐司\*", username="烤吐司機", avatar_url="https://images.plurk.com/67L8aTFP2WiiKypJ6wSqoj.png")

        if message.content == '剪刀石頭布' and message.author != self.bot.user:
            authr = message.author.name if message.author.nick is None else message.author.nick
            embedmes = discord.Embed(title="剪刀石頭布！", description=f'{authr}，你要玩剪刀石頭布嗎？')
            org_message=await message.channel.send(embed=embedmes)
            emoji_y="⭕"
            emoji_n="❌"
            await org_message.add_reaction(emoji_y)
            await org_message.add_reaction(emoji_n)
            try:
                def checkv(reaction,user):
                    return user == message.author and str(reaction.emoji) in (emoji_y,emoji_n)
                reaction,user=await self.bot.wait_for("reaction_add", timeout=20, check=checkv)
                if str(reaction.emoji) ==emoji_n:
                    await org_message.delete()
                if str(reaction.emoji) ==emoji_y:
                    await org_message.delete()
                    try:
                        embedmes2 = discord.Embed(title="出拳！", description=f'玩家{authr}，請在60秒內於下方以文字留言你要出的拳。(剪刀、石頭、布)')
                        embedmes2.set_author(name=authr, icon_url=message.author.display_avatar.url)
                        org2_message=await message.channel.send(embed=embedmes2)
                        def checkb(incmessage):
                            return incmessage.author == message.author and incmessage.channel==message.channel
                        messagegg=await self.bot.wait_for("message", timeout=60, check=checkb)
                        they_do=messagegg.clean_content
                        with open('csvfile\\pss.json','r',encoding='utf-8') as jfile:
                            pss_file=json.load(jfile)
                        pss_file.setdefault(they_do,random.choice([1,2,3]))
                        with open('csvfile\\pss.json','w',encoding='utf-8') as jfile:
                            json.dump(pss_file,jfile,ensure_ascii=False,indent=4)
                        cpu_do=random.choice(("剪刀","石頭","布"))
                        resultin=do_pss(pss_file[they_do],pss_file[cpu_do])
                        if resultin=="0":
                            r1="平手！"
                            r2="沒想到結果會是這樣呢，再來一次？"
                        elif resultin=="a":
                            r1="你贏了！"
                            r2="哎呀哎呀，可惡，下次可不會輸給你的！"
                        elif resultin=="b":
                            r1="你輸了！"
                            r2="哼哼，我很厲害吧！"
                        embedmes3 = discord.Embed(title=r1, description=r2)
                        embedmes3.set_author(name=authr, icon_url=message.author.display_avatar.url)
                        embedmes3.add_field(name="你出了", value=they_do, inline=True)
                        embedmes3.add_field(name="Bot出了", value=cpu_do, inline=True)
                        embedmes3.set_footer(text="打「剪刀石頭布」來進行猜拳對決")
                        await message.channel.send(embed=embedmes3)
                    except asyncio.TimeoutError:
                        await org2_message.delete()
            except asyncio.TimeoutError:
                await org_message.delete()

        if message.content.startswith("剪刀石頭布對戰") and message.author != self.bot.user:
            if not message.mentions:
                await message.channel.send(f"{message.author.mention}\n請@任何一位非BOT成員以邀請對戰。")
                return

            if len(message.mentions)!=1:
                await message.channel.send(f"{message.author.mention}\n一次只能跟一個人BATTLE啦-w-...。")
                return

            req_member=message.mentions[0]
            if req_member.bot:
                await message.channel.send(f"{message.author.mention}\n對戰目前只支援跟非bot對戰喔-w-...。")
                return

            if req_member==message.author:
                await message.channel.send(f"{message.author.mention}\n你不能跟自己對戰-w-...。")
                return

            chlngr = req_member.name if req_member.nick is None else req_member.nick
            invtr = message.author.name if message.author.nick is None else message.author.nick
            embedmes = discord.Embed(title="⚔️BATTLE！", description=f'{chlngr}，{invtr}向你發起剪刀石頭布的對戰！\n你要接受邀請嗎？')
            embedmes.set_author(name=chlngr, icon_url=req_member.avatar_url)
            org_message=await message.channel.send(embed=embedmes)
            emoji_y="⭕"
            emoji_n="❌"
            await org_message.add_reaction(emoji_y)
            await org_message.add_reaction(emoji_n)

            try:
                def checkv(reaction,user):
                    return user == req_member and str(reaction.emoji) in (emoji_y,emoji_n)
                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=checkv)
                if str(reaction.emoji) ==emoji_n:
                    embedmes = discord.Embed(title="💣被拒...", description=f'{chlngr}拒絕了你發起的剪刀石頭布對戰...')
                    embedmes.set_author(name=invtr, icon_url=message.author.display_avatar.url)
                    org_message.clear_reactions()
                    await org_message.edit(embed=embedmes)
                if str(reaction.emoji) ==emoji_y:
                    embedmes = discord.Embed(title="⚔️BATTLE！", description=f'{chlngr}與{invtr}，請至雪狛的私訊出拳！')
                    embedmes.set_author(name="裁判", icon_url=self.bot.user.default_avatar_url)
                    await org_message.clear_reactions()
                    await org_message.edit(embed=embedmes)

                try:
                    pss_mes=discord.Embed(title="⚔️猜拳！", description=f'請在60秒內於下方以文字留言你要出的拳。')
                    invtr_mes=await message.author.send(f"{message.author.mention}",embed=pss_mes)
                    chlngr_mes=await req_member.send(f"{req_member.mention}",embed=pss_mes)

                    def checkinvtr(incmessage):
                        return incmessage.author == message.author and isinstance(incmessage.channel, discord.DMChannel) #必須是DM且使用者正確
                    def checkchlngr(incmessage):
                        return incmessage.author == req_member and isinstance(incmessage.channel, discord.DMChannel) #必須是DM且使用者正確

                    invtrdo, chlngrdo = await asyncio.gather(self.bot.wait_for("message", timeout=60, check=checkinvtr),self.bot.wait_for("message", timeout=60, check=checkchlngr))

                    pss_mes=discord.Embed(title="⚔️猜拳！", description=f'雙方猜拳完成，請回原頻道查看結果。')
                    await invtr_mes.edit(embed=pss_mes)
                    await chlngr_mes.edit(embed=pss_mes)

                    invtrdo=invtrdo.clean_content
                    chlngrdo=chlngrdo.clean_content

                    with open('csvfile\\pss.json','r',encoding='utf-8') as jfile:
                        pss_file=json.load(jfile)
                    invtr123=pss_file.setdefault(invtrdo,random.choice([1,2,3]))
                    chlngr123=pss_file.setdefault(chlngrdo,random.choice([1,2,3]))
                    with open('csvfile\\pss.json','w',encoding='utf-8') as jfile:
                        json.dump(pss_file,jfile,ensure_ascii=False,indent=4)

                    resultin=do_pss(invtr123,chlngr123)
                    if resultin=="0":
                        r1="平手！"
                    elif resultin=="a":
                        r1=f"{invtr}贏了！"
                    elif resultin=="b":
                        r1=f"{chlngr}贏了！"

                    embedmes3 = discord.Embed(title=r1,colour=0x90EE90)
                    embedmes3.set_author(name="裁判", icon_url=self.bot.user.default_avatar_url)
                    embedmes3.add_field(name=f"{invtr}出了", value=invtrdo, inline=True)
                    embedmes3.add_field(name=f"{chlngr}出了", value=chlngrdo, inline=True)
                    embedmes3.set_footer(text="打「剪刀石頭布對戰」來進行玩家間的猜拳對決")
                    await message.channel.send(embed=embedmes3)

                except asyncio.TimeoutError:
                    embedmes = discord.Embed(title="💣超時...", description=f'其中一方沒有出拳-w-...')
                    embedmes.set_author(name="裁判", icon_url=self.bot.user.default_avatar_url)
                    await org_message.edit(embed=embedmes)
                    await org_message.clear_reactions()
            except asyncio.TimeoutError:
                embedmes = discord.Embed(title="💣超時...", description=f'{chlngr}沒有接受你發起的剪刀石頭布對戰-w-...')
                embedmes.set_author(name=invtr, icon_url=message.author.display_avatar.url)
                await org_message.edit(embed=embedmes)
                await org_message.clear_reactions()
        if message.content == '午餐吃什麼' and message.author != self.bot.user:
            authr = message.author.name if message.author.nick is None else message.author.nick
            with open('csvfile\coffee.json','r',encoding='utf-8') as jfile:
                cofeefile=json.load(jfile)
            e_or_d = random.choices(["吃","喝"],weights=(len(cofeefile["dinner"]["吃"]),len(cofeefile["dinner"]["喝"])))[0]
            resultin = random.choice(cofeefile["dinner"][e_or_d])
            embedmes = discord.Embed(title="午餐！", description=f'{authr}，午餐你可以{e_or_d}{resultin}。')
            embedmes.set_author(name=authr, icon_url=message.author.display_avatar.url)
            await message.channel.send(embed=embedmes)

        if message.content == '晚餐吃什麼' and message.author != self.bot.user:
            authr = message.author.name if message.author.nick is None else message.author.nick
            with open('csvfile\coffee.json','r',encoding='utf-8') as jfile:
                cofeefile=json.load(jfile)
            e_or_d = random.choices(["吃","喝"],weights=(len(cofeefile["dinner"]["吃"]),len(cofeefile["dinner"]["喝"])))[0]
            resultin = random.choice(cofeefile["dinner"][e_or_d])
            embedmes = discord.Embed(title="晚餐！", description=f'{authr}，晚餐你可以{e_or_d}{resultin}。')
            embedmes.set_author(name=authr, icon_url=message.author.display_avatar.url)
            await message.channel.send(embed=embedmes)


async def setup(bot):
    await bot.add_cog(Say(bot))