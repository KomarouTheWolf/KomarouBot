import discord
from discord.ext import commands
from core.classes import Cog_Extension
from discord import Embed
import json
import random
import asyncio
from discord.ui import Button,View

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
        await self.org_mes.edit(view=self)

class CardDeck:
    def __init__(self):
        newcard = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4
        random.shuffle(newcard)
        self.cards = newcard
        self.card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}

    def deal_card(self):
        if len(self.cards) == 0:
            self.__init__()  #初始化牌堆
        return self.cards.pop()
    
    def calculate_score(self,cards):
        score = sum(self.card_values[card] for card in cards)
        num_aces = sum(1 for card in cards if card == "A")
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score

class CardView(View):
    def __init__(self,ctx,deck:CardDeck,plrcrd:list,cmpcrd:list):
        super().__init__(timeout=180)
        self.org_mes=None
        self.org_content=None
        self.deck=deck
        self.player_cards = plrcrd
        self.computer_cards = cmpcrd
        self.slfcmd = None
        self.ctx = ctx

    def resemb(self):
        embedmes= discord.Embed(title="21點！",description=self.org_content,colour=0x00DB00)  #綠色
        embedmes.set_author(name=self.ctx.author.display_name, icon_url=self.ctx.author.display_avatar.url)
        embedmes.add_field(name=f'你的牌',value=f'{",".join(self.player_cards)}({self.deck.calculate_score(self.player_cards)}點)')
        embedmes.add_field(name=f'莊家的牌',value=f'??,{self.computer_cards[1]}(??點)')
        return embedmes

    async def ending(self,interaction):
        def rvlemb(self,color,title):

            if title=="你贏了！":
                if self.deck.calculate_score(self.computer_cards) >21:
                    greets=["無奈地看著自己的雙手。","嘆了一口氣但依舊笑著看向你。","眼神有些失落。","發自內心的為你的勝利笑著。","承認你是個可敬的對手。"]
                elif self.deck.calculate_score(self.player_cards) ==21:
                    greets=["震驚著看著你的牌！","兩手一攤，無奈的大笑著。","發自內心的為你的勝利笑著。","承認你是個可敬的對手。"]
                else:
                    greets=["眼神有些失落。","發自內心的為你的勝利笑著。","承認你是個可敬的對手。"]
            elif title=="你輸了......":
                if self.deck.calculate_score(self.computer_cards) ==21 and len(self.computer_cards)==2:
                    greets=["囂張著拿著自己的牌在你眼前晃！","終於不需要忍耐，癲狂的大笑著！","驕傲著揚起了頭！","露出了燦爛的笑容！","興奮的嚎叫著！"]
                elif self.deck.calculate_score(self.computer_cards) ==21:
                    greets=["囂張著拿著自己的牌在你眼前晃！","驕傲著揚起了頭！","露出了燦爛的笑容！","興奮的嚎叫著！"]
                else:
                    greets=["驕傲著揚起了頭！","用看菜鳥的悲憫眼神看著你。","露出了燦爛的笑容！","幾不可聞的「呵」了一聲。"]
            elif title=="平手！":
                greets=["伸出手向你握手致意。","用認可的眼神看著你。","看著這個結局開心的微笑著。","承認你是個可敬的對手。"]
            
            if title!="開牌時間！":
                greentres=random.choice(greets)
                self.org_content+=f'狛克{greentres}'

            embedmes= discord.Embed(title=title,description=self.org_content,colour=color)
            embedmes.set_author(name=self.ctx.author.display_name, icon_url=self.ctx.author.display_avatar.url)
            embedmes.add_field(name=f'你的牌',value=f'{",".join(self.player_cards)}({self.deck.calculate_score(self.player_cards)}點)')
            embedmes.add_field(name=f'莊家的牌',value=f'{",".join(self.computer_cards)}({self.deck.calculate_score(self.computer_cards)}點)')
            return embedmes
        
        green=0x00DB00
        red=0xF75000
        golden=0xFFD306
        brown=0x5B4B00
        self.org_content+="\n"

        rview=OneButtonCmdView("再來一局？","🎮",self.slfcmd,self.ctx)
        rview.org_mes=self.org_mes
        await interaction.response.defer()
        
        if self.deck.calculate_score(self.player_cards) == 21:
            self.org_content+=f'**你贏了！**你直接湊齊了21點！\n'
            await self.org_mes.edit(content=f"{self.ctx.author.mention}", embed=rvlemb(self,golden,"你贏了！"),view=rview)
        elif self.deck.calculate_score(self.player_cards) > 21:
            self.org_content+=f'**你輸了！**你的點數超過了21點！\n'
            await self.org_mes.edit(content=f"{self.ctx.author.mention}", embed=rvlemb(self,red,"你輸了......"),view=rview)
        else:
            self.org_content+=f'狛克翻開了自己覆蓋的牌，是{self.computer_cards[0]}！\n'
            while self.deck.calculate_score(self.computer_cards) <17:
                await self.org_mes.edit(content=f"{self.ctx.author.mention}", embed=rvlemb(self,green,"開牌時間！"),view=None)
                await asyncio.sleep(3)
                self.computer_cards.append(self.deck.deal_card())
                self.org_content+=f'狛克發給自己了一張{self.computer_cards[-1]}。\n'

            self.org_content+=f'\n'
            if self.deck.calculate_score(self.computer_cards) >21:
                self.org_content+=f'**你贏了！**狛克的點數爆掉了！\n'
                await self.org_mes.edit(content=f"{self.ctx.author.mention}", embed=rvlemb(self,golden,"你贏了！"),view=rview)
            elif self.deck.calculate_score(self.player_cards)>self.deck.calculate_score(self.computer_cards):
                self.org_content+=f'**你贏了！**你的點數比狛克大！\n'
                await self.org_mes.edit(content=f"{self.ctx.author.mention}", embed=rvlemb(self,golden,"你贏了！"),view=rview)
            elif self.deck.calculate_score(self.player_cards)<self.deck.calculate_score(self.computer_cards):
                self.org_content+=f'**你輸了！**狛克的點數比你大！\n'
                await self.org_mes.edit(content=f"{self.ctx.author.mention}", embed=rvlemb(self,red,"你輸了......"),view=rview)
            else:
                self.org_content+=f'**平手！**你跟狛克的點數一樣大！\n'
                await self.org_mes.edit(content=f"{self.ctx.author.mention}", embed=rvlemb(self,brown,"平手！"),view=rview)


    @discord.ui.button(label="再要一張牌",emoji="🗡️",style=discord.ButtonStyle.green,custom_id="drw")
    async def drw_callback(self, interaction: discord.Interaction ,button):
        if self.ctx.author==interaction.user:
            self.player_cards.append(self.deck.deal_card())
            self.org_content+=f'你選擇再要一張牌，狛克發給你一張{self.player_cards[-1]}！\n'
            if self.deck.calculate_score(self.player_cards)>=21:
                await self.ending(interaction)
            else:
                outemb=self.resemb()
                await interaction.response.edit_message(content=f"{self.ctx.author.mention}", embed=outemb,view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="就這樣吧，開牌！",emoji="⚔️",style=discord.ButtonStyle.danger,custom_id="stp")
    async def stp_callback(self, interaction: discord.Interaction ,button):
        if self.ctx.author==interaction.user:
            self.org_content+=f'你選擇開牌！\n'
            await self.ending(interaction)
        else:
            await interaction.response.defer()

    async def on_timeout(self):
        for btns in self.children:
            btns.disabled=True
            btns.style=discord.ButtonStyle.gray
        await self.org_mes.edit(view=self)

class Adventure(Cog_Extension):
    @commands.command()
    async def card(self,ctx):
        deck = CardDeck()
        player_cards, computer_cards = [], []
        for _ in range(2):
            player_cards.append(deck.deal_card())
            computer_cards.append(deck.deal_card())

        outmes='狛克發出了牌，並將自己的一張牌覆蓋！\n'

        smirkval=25 if deck.calculate_score(computer_cards) >= 19 else 3
        frownval=25 if deck.calculate_score(computer_cards) == 16 else 3

        face_expression_dice=random.randint(1,100)
        if face_expression_dice <= smirkval:
            face_expression = random.choice(["露出了狡黠的笑容！","眼中閃過一絲興奮！","尾巴不受控制的晃了起來。"])
        elif face_expression_dice <= frownval:
            face_expression = random.choice(["臉色一片蒼白！","眉頭深鎖。","雙耳不自制的下垂。"])
        else:
            face_expression = random.choice(["淡定著闔上牌。","一片平靜。","看起來很期待你的選擇。","一語不發。"])

        outmes+=f'狛克偷看了一眼自己的牌，{face_expression}\n\n'

        embedmes= discord.Embed(title="21點！",description=outmes,colour=0x00DB00)  #綠色
        embedmes.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embedmes.add_field(name=f'你的牌',value=f'{",".join(player_cards)}({deck.calculate_score(player_cards)}點)')
        embedmes.add_field(name=f'莊家的牌',value=f'??,{computer_cards[1]}(??點)')

        theview = CardView(ctx,deck,player_cards,computer_cards)
        slfcmd= self.bot.get_command("card")
        theview.slfcmd = slfcmd

        orgmes = await ctx.send(f"{ctx.author.mention}",embed=embedmes,view=theview)
        theview.org_mes=orgmes
        theview.org_content=outmes

async def setup(bot):
    await bot.add_cog(Adventure(bot))