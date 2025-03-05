import discord
from discord.ext import commands
import json
import random
from core.classes import Cog_Extension
import asyncio

with open('setting.json','r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)

def numnum(a):
    try:
        int(a)
    except:
        return False
    else:
        return True

def testresult(job_id):
    k=["戰士","聖騎士","牧師","傀儡師","街頭藝人","狂戰士","膽小鬼","狼人","賭徒","主教","賢者","靈術使者","毒幽靈","槍械塔技師","催眠師","衛兵","入殮師","學徒","精靈師","召喚師","忍者","煉金術師","元素使","店員","浪人","音樂家","小傑","奇犽","魔槍手","燈火使"]
    outmes=f"適合你的職業為{job_id}.**{k[job_id-1]}**！\n"
    outmes+="在<#670646498618376232>看看這個職業的能力吧！\n"
    return outmes

kills=0

class Zombie(Cog_Extension):
    @commands.command()
    async def dmg(self,ctx,arg1,arg2):
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

    @commands.command()
    async def dth(self,ctx,arg):
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

    @commands.command()
    async def ban(self,ctx):
        aa=jdata["JOB"]
        oao=''
        bb=random.sample(aa,5)
        for a in bb:
            oao+=(a+" ")
        await ctx.message.channel.send(f'```{oao}```')

    @commands.command()
    async def classtest(self,ctx):
        emoji1="1️⃣"
        emoji2="2️⃣"
        emoji3="3️⃣"
        def check2(reaction, user):
            return user == ctx.author and str(reaction.emoji) in (emoji1,emoji2)
        def check3(reaction, user):
            return user == ctx.author and str(reaction.emoji) in (emoji1,emoji2,emoji3)
        
        
        original_message=await ctx.send(f'{ctx.author.mention}\n歡迎使用狛克自製測試殭屍大逃殺職業適性1.0ver.\n可以測出相對適合你的職業，不準不要打我，要注意的是放置超過2分鐘bot會自動刪除。\n1:知道了啦趕快開始\n2:我突然不想做了笑死')
        await original_message.clear_reactions()
        await original_message.add_reaction(emoji1)
        await original_message.add_reaction(emoji2)


        #你各位請看沒學好coroutine與task的下場
        #這段我是懶得改了 反正都能動

        try:
            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
            if str(reaction.emoji) ==emoji2:
                await original_message.clear_reactions()
                await original_message.edit(content=f"好喔，888 -w-")
                await asyncio.sleep(3)
                await original_message.delete()
                await ctx.message.delete()
                return
            elif str(reaction.emoji) ==emoji1:
                await original_message.clear_reactions()
                await original_message.add_reaction(emoji1)
                await original_message.add_reaction(emoji2)
                #第一問
                await original_message.edit(content=f"{ctx.author.mention}\n對於冒險的各種事件，你的偏好是？\n1:排除一切可能危險\n2:享受冒險途中的未知")
                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                if str(reaction.emoji) ==emoji1:
                    await original_message.clear_reactions()
                    await original_message.add_reaction(emoji1)
                    await original_message.add_reaction(emoji2)
                    await original_message.add_reaction(emoji3)
                    #A問
                    await original_message.edit(content=f"{ctx.author.mention}\n你期望的角色定位是？\n1:承擔團隊希望的主力輸出\n2:作為隊友後盾的強力輔助\n3:兩種都弱一點也沒關係，輸出輔助我全都要")
                    reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check3)
                    if str(reaction.emoji) ==emoji1:
                        await original_message.clear_reactions()
                        #A1問
                        await original_message.edit(content=f"{ctx.author.mention}\n你喜歡讓角色爆炸嗎？\n1:不用了我安定一點\n2:哪次不耍帥的啦")
                        await original_message.add_reaction(emoji1)
                        await original_message.add_reaction(emoji2)
                        reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                        if str(reaction.emoji) ==emoji1:
                            await original_message.clear_reactions()
                            #A1K問
                            await original_message.edit(content=f"{ctx.author.mention}\n你希望角色擁有哪種發展曲線？\n1:穩一點，不要有明顯弱勢期\n2:為了巔峰，可以接受過渡期的存在")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                #A1KV問
                                await original_message.edit(content=f"{ctx.author.mention}\n考卷上有兩題你不會的填充題，但你知道其中一個是甲，一個是乙。\n你會怎麼填答案？\n1:兩個都填一樣的，至少要賺到一題\n2:一個填甲一個填乙，我是天選之人可以的啦")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(1)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(14)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                #A1K反V問
                                await original_message.edit(content=f"{ctx.author.mention}\n你喜歡被打嗎？\n1:快，打我！\n2:我才不要！")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(13)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(18)}")
                        elif str(reaction.emoji) ==emoji2:
                            await original_message.clear_reactions()
                            #A1K反K問
                            await original_message.edit(content=f"{ctx.author.mention}\n你相信自己的運氣嗎？\n1:我都靠運氣吃飯的啦！\n2:有沒有...比較不靠運氣的...職業...")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(15)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                #A1K反K正方形問
                                await original_message.edit(content=f"{ctx.author.mention}\n生死之交的戰友在交涉時被其他倖存者陷害而葬身於喪屍堆中，你的身邊只剩下青梅竹馬的戀人，你會怎麼行動？\n1:安置好愛人後，尋找兇手的下落並報仇\n2:全力守護好唯一的愛人，不讓悲劇再次發生")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(6)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(8)}")
                    elif str(reaction.emoji) ==emoji2:
                        await original_message.clear_reactions()
                        #A2問
                        await original_message.edit(content=f"{ctx.author.mention}\n你想成為在團隊陷入劣勢時獨自力挽狂瀾，絕境翻盤的英雄嗎？\n1:我想要有搶救局勢的能力！\n2:不陷入絕境就不用翻盤了吧？")
                        await original_message.add_reaction(emoji1)
                        await original_message.add_reaction(emoji2)
                        reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                        if str(reaction.emoji) ==emoji1:
                            await original_message.clear_reactions()
                            #A2上問
                            await original_message.edit(content=f"{ctx.author.mention}\n你相信自己的運氣嗎？\n1:我都靠運氣吃飯的啦！\n2:有沒有...比較不靠運氣的...職業...")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                #A2上:D問
                                await original_message.edit(content=f"{ctx.author.mention}\n你認為一個優秀的槍兵，哪個性質最重要？\n1:高命中率\n2:身體素質\n3:優質武器")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                await original_message.add_reaction(emoji3)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check3)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(9)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(2)}")
                                elif str(reaction.emoji) ==emoji3:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(11)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                #A2上反:D問
                                await original_message.edit(content=f"{ctx.author.mention}\n兩種守城方案，你會選擇哪一套？\n1:城外重兵防禦\n2:城內陷阱佈陣")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(3)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(16)}")
                        elif str(reaction.emoji) ==emoji2:
                            await original_message.clear_reactions()
                            #A2上反:D問
                            await original_message.edit(content=f"{ctx.author.mention}\n希望角色的操作複雜度如何？\n1:簡單一點，可以理解比較重要\n2:複雜一點也可以，重點是好用")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(17)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(12)}")
                    elif str(reaction.emoji) ==emoji3:
                        await original_message.clear_reactions()
                        #A3問
                        await original_message.edit(content=f"{ctx.author.mention}\n輸出輔助都要的原因是？\n1:普通的...選擇...困難...\n2:想要在不同情況下擁有做出不同決定的能力")
                        await original_message.add_reaction(emoji1)
                        await original_message.add_reaction(emoji2)
                        reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                        if str(reaction.emoji) ==emoji1:
                            await original_message.clear_reactions()
                            #A3勾問
                            await original_message.edit(content=f"{ctx.author.mention}\n希望角色的操作複雜度如何？\n1:簡單一點，可以理解比較重要\n2:複雜一點也可以，重點是好用")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                #A3勾+問
                                await original_message.edit(content=f"{ctx.author.mention}\n隊友跟自己同時遇到危機時，會優先搶救哪邊的危機？\n1:自己重要\n2:隊友重要")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(4)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(10)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                #A3勾-問
                                await original_message.edit(content=f"{ctx.author.mention}\n你喜歡讓角色爆炸嗎？\n1:不用了我安定一點\n2:哪次不耍帥的啦")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(4)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(29)}")
                        elif str(reaction.emoji) ==emoji2:
                            await original_message.clear_reactions()
                            #A3叉問
                            await original_message.edit(content=f"{ctx.author.mention}\n你相信你隊友的運氣嗎？\n1:我的隊友都很強的啦\n2:我們之間沒有信任")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(7)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(30)}")
                elif str(reaction.emoji) ==emoji2:
                    await original_message.clear_reactions()
                    #B問
                    await original_message.edit(content=f"{ctx.author.mention}\n你期望的角色定位是？\n1:承擔團隊希望的主力輸出\n2:作為隊友後盾的強力輔助\n3:兩種都弱一點也沒關係，輸出輔助我全都要")
                    await original_message.add_reaction(emoji1)
                    await original_message.add_reaction(emoji2)
                    await original_message.add_reaction(emoji3)
                    reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check3)
                    if str(reaction.emoji) ==emoji1:
                        await original_message.clear_reactions()
                        #B1問
                        await original_message.edit(content=f"{ctx.author.mention}\n敢使用很看隊友選角的角色嗎？\n1:我都可以啊沒差的\n2:能不被隊友束縛比較好")
                        await original_message.add_reaction(emoji1)
                        await original_message.add_reaction(emoji2)
                        reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                        if str(reaction.emoji) ==emoji1:
                            await original_message.clear_reactions()
                            await original_message.edit(content=f"{ctx.author.mention}\n{testresult(28)}")
                        elif str(reaction.emoji) ==emoji2:
                            await original_message.clear_reactions()
                            #B1N問
                            await original_message.edit(content=f"{ctx.author.mention}\n考卷上有兩題你不會的填充題，但你知道其中一個是甲，一個是乙。\n你會怎麼填答案？\n1:兩個都填一樣的，至少要賺到一題\n2:一個填甲一個填乙，我是天選之人可以的啦")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(25)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(21)}")
                    elif str(reaction.emoji) ==emoji2:
                        await original_message.clear_reactions()
                        #B3問
                        await original_message.edit(content=f"{ctx.author.mention}\n你相信自己的運氣嗎？\n1:我都靠運氣吃飯的啦！\n2:有沒有...比較不靠運氣的...職業...")
                        await original_message.add_reaction(emoji1)
                        await original_message.add_reaction(emoji2)
                        reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                        if str(reaction.emoji) ==emoji1:
                            await original_message.clear_reactions()
                            await original_message.edit(content=f"{ctx.author.mention}\n{testresult(11)}")
                        elif str(reaction.emoji) ==emoji2:
                            await original_message.clear_reactions()
                            await original_message.edit(content=f"{ctx.author.mention}\n{testresult(24)}")
                    elif str(reaction.emoji) ==emoji3:
                        await original_message.clear_reactions()
                        #B2問
                        await original_message.edit(content=f"{ctx.author.mention}\n你希望角色擁有哪種發展曲線？\n1:穩一點，不要有明顯弱勢期\n2:為了巔峰，可以接受過渡期的存在")
                        await original_message.add_reaction(emoji1)
                        await original_message.add_reaction(emoji2)
                        reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                        if str(reaction.emoji) ==emoji1:
                            await original_message.clear_reactions()
                            #B2閃電問
                            await original_message.edit(content=f"{ctx.author.mention}\n輸出輔助都要的原因是？\n1:普通的...選擇...困難...\n2:想要在不同情況下擁有做出不同決定的能力")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(5)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                #B2閃電X問
                                await original_message.edit(content=f"{ctx.author.mention}\n你希望角色在哪方面能稍微更強一點？\n1:輔助層面\n2:輸出層面")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    #B2閃電X輔助問
                                    await original_message.edit(content=f"{ctx.author.mention}\n喜歡動物還是魔法？\n1:我喜歡毛毛的\n2:我喜歡爆炸")
                                    await original_message.add_reaction(emoji1)
                                    await original_message.add_reaction(emoji2)
                                    reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                    if str(reaction.emoji) ==emoji1:
                                        await original_message.clear_reactions()
                                        await original_message.edit(content=f"{ctx.author.mention}\n{testresult(20)}")
                                    elif str(reaction.emoji) ==emoji2:
                                        await original_message.clear_reactions()
                                        await original_message.edit(content=f"{ctx.author.mention}\n{testresult(19)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(23)}")
                        elif str(reaction.emoji) ==emoji2:
                            await original_message.clear_reactions()
                            #B2反閃電問
                            await original_message.edit(content=f"{ctx.author.mention}\n敢使用很看隊友選角的角色嗎？\n1:我都可以啊沒差的\n2:能不被隊友束縛比較好")
                            await original_message.add_reaction(emoji1)
                            await original_message.add_reaction(emoji2)
                            reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                            if str(reaction.emoji) ==emoji1:
                                await original_message.clear_reactions()
                                await original_message.edit(content=f"{ctx.author.mention}\n{testresult(27)}")
                            elif str(reaction.emoji) ==emoji2:
                                await original_message.clear_reactions()
                                #B2反閃電N問
                                await original_message.edit(content=f"{ctx.author.mention}\n你喜歡讓角色爆炸嗎？\n1:不用了我安定一點\n2:哪次不耍帥的啦")
                                await original_message.add_reaction(emoji1)
                                await original_message.add_reaction(emoji2)
                                reaction,user=await self.bot.wait_for("reaction_add", timeout=120, check=check2)
                                if str(reaction.emoji) ==emoji1:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(26)}")
                                elif str(reaction.emoji) ==emoji2:
                                    await original_message.clear_reactions()
                                    await original_message.edit(content=f"{ctx.author.mention}\n{testresult(22)}")
        except asyncio.TimeoutError:
            await original_message.clear_reactions()
            await original_message.edit(content=f"放置超過2分鐘，自動刪除！")
            await asyncio.sleep(3)
            await original_message.delete()
            await ctx.message.delete()


    @commands.command()
    async def animal(self,ctx):
        original_message=await ctx.send(f'告訴我，小林，你有什麼興趣？你喜歡動物嗎？\n1:什麼？動物？哪一種？\n2:奶油龍蝦腳♪加水餃♫放在一起烤♪')
        emoji1="1️⃣"
        emoji2="2️⃣"
        await original_message.add_reaction(emoji1)
        await original_message.add_reaction(emoji2)
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in (emoji2,emoji1)
        try:
            reaction,user= await self.bot.wait_for("reaction_add", timeout=15.0, check=check)
            if str(reaction.emoji) ==emoji1:
                await original_message.clear_reactions()
                await original_message.edit(content=f"一般的、狗、貓、馬、天竺鼠......\n勞贖？")
            if str(reaction.emoji) ==emoji2:
                await original_message.clear_reactions()
                await original_message.edit(content=f"(氣到中離)")
        except asyncio.TimeoutError:
            await original_message.clear_reactions()
            await original_message.edit(content=f"太久了啦不理你了-w-")

async def setup(bot):
    await bot.add_cog(Zombie(bot))