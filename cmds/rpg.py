import discord
from discord.ext import commands
from discord import Embed
import numpy as np
from tenacity import AttemptManager
from core.classes import Cog_Extension
import json
import random
import time
import asyncio
import pandas as pd
import math

item="csvfile\\item.csv"
furfile="csvfile\\furcount.csv"
damagerec="csvfile\\damagerec.csv"
timenote="csvfile\\timelimit.csv"
boss_killer="csvfile\\killed.csv"
rpgweapon="csvfile\\rpgweapon.csv"
available_channel=(935768359931371540,935471683911954512,641131990959259667,938827700968231022,990563126397247548)

with open('csvfile\channel.json','r',encoding='utf-8') as jfile:
    gifs=json.load(jfile)
with open('csvfile\\furryshop.json','r',encoding='utf-8') as jfile:
    furryshop=json.load(jfile)
with open('csvfile\\itemdata.json','r',encoding='utf-8') as jfile:
    item_fulldata=json.load(jfile)
with open("csvfile\\tips.csv",'r',encoding='utf-8') as jfile:
    tips=jfile.readlines()

#把道具中文名字對照成ID的字典
itemdict={}
for items in item_fulldata:
    itemdict[item_fulldata[items]["name"]]=items

find_id = lambda items : itemdict[items] #str
inf = lambda item_id : item_fulldata[item_id] #dict
ch = lambda item_id : item_fulldata[item_id]['name'] #str

#把csv讀成df
def doread(csv_file,col_names=None):
    df=pd.read_csv(csv_file,sep=",",header=None,names=col_names)
    return df

#把df寫入csv
def csv_write(df,csv_file,mode):
    df.to_csv(csv_file,encoding="utf-8",index=False,header=False,mode=mode)

#清空
def doblank(file):
    blanky=pd.DataFrame([[0,0]])
    csv_write(blanky,file,"w")

def doblank_dmgrec(file):
    blanky=pd.DataFrame([[]])
    csv_write(blanky,file,"w")

#讀取道具與牙齒表
def read_item():
    df=doread(item,["playerID","tooths","items"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    df.loc[:,"tooths"]=df["tooths"].astype("int64")
    return df

#讀取時間限制列表
def read_time():
    df=doread(timenote,["playerID","time"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    df.loc[:,"time"]=df["time"].astype("float64")
    return df

def read_bosskiller():
    df=doread(boss_killer,["playerID"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    return df

#讀取狼毛表
def read_fur():
    df=doread(furfile,["playerID","furs"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    df.loc[:,"furs"]=df["furs"].astype("int64")
    return df

#讀取武器表 #串列注意
def read_weapons():
    with open(rpgweapon,'r',encoding='utf-8') as jfile:
        alllines=[]
        raw_data=jfile.readlines()
        for lines in raw_data:
            alllines.append(lines.strip('\n').strip(' ').split(','))
    return alllines

def read_damagerec():
    df=doread(damagerec,["playerID","dmg"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    df.loc[:,"dmg"]=df["dmg"].astype("int64")
    return df

#把玩家的道具轉換成df
def read_scrolls(id):
    raw_df=read_item()
    if id not in raw_df["playerID"].values:
        return "Not found"
    raw_item = raw_df.loc[raw_df["playerID"]==id,"items"].copy().values[0].split(';')
    for everyitem in range(len(raw_item)):
        raw_item[everyitem]=raw_item[everyitem].split('%')
    df=pd.DataFrame(raw_item,columns=["name","counts"])
    df.loc[:,"counts"]=df["counts"].astype("int64")
    df.set_index("name",inplace=True)
    return df

#把改完的道具df寫回道具表
def save_scrolls(id,df):
    df=df.to_dict()
    result=""
    for item_name in df["counts"]:
        result+=f'{item_name}%{int(df["counts"][item_name])};'
    result=result[:-1]
    item_df=read_item()
    item_df.loc[item_df["playerID"]==id,"items"]=result
    csv_write(item_df,item,"w")
    return "okay"

#給牙齒
def givetooth(id,how_many):
    itemrawdata=read_item()
    if id in itemrawdata["playerID"].values:
        itemrawdata.loc[itemrawdata["playerID"]==id,"tooths"]=int(itemrawdata.loc[itemrawdata["playerID"]==id,"tooths"]+how_many)
        csv_write(itemrawdata,item,"w")
    else:
        blanky=pd.DataFrame([[id,how_many,'0%0']])
        csv_write(blanky,item,"a")

#消耗牙齒
def removetooth(id,how_many):
    itemrawdata=read_item()
    if id in itemrawdata["playerID"].values:
        available_tooth=int(itemrawdata.loc[itemrawdata["playerID"]==id,"tooths"])
        if available_tooth < how_many:
            return available_tooth
        else:
            itemrawdata.loc[itemrawdata["playerID"]==id,"tooths"]=int(itemrawdata.loc[itemrawdata["playerID"]==id,"tooths"]-how_many)
            csv_write(itemrawdata,item,"w")
            return True
    else:
        return 0

def givefur(id,how_many):
    itemrawdata=read_fur()
    if id in itemrawdata["playerID"].values:
        itemrawdata.loc[itemrawdata["playerID"]==id,"furs"]=int(itemrawdata.loc[itemrawdata["playerID"]==id,"furs"]+how_many)
        csv_write(itemrawdata,furfile,"w")
    else:
        blanky=pd.DataFrame([[id,how_many]])
        csv_write(blanky,furfile,"a")

def removefur(id,how_many):
    itemrawdata=read_fur()
    if id in itemrawdata["playerID"].values:
        available_fur=int(itemrawdata.loc[itemrawdata["playerID"]==id,"furs"])
        if available_fur < how_many:
            return available_fur
        else:
            itemrawdata.loc[itemrawdata["playerID"]==id,"furs"]=int(itemrawdata.loc[itemrawdata["playerID"]==id,"furs"]-how_many)
            csv_write(itemrawdata,furfile,"w")
            return True
    else:
        return 0

def giveitem(reciever,arg1,arg2=1):       #receiver是int,arg1是物品名稱 #沒有辨識arg2是否為int的功能
    if arg1 == "":
        return '您似乎沒有說明要使用什麼呢-w-...'
    if arg1 not in itemdict:
        return '這個東西似乎名稱不對呢-w-...\n請確定您輸入的是不含稀有度的道具全名-w-...'
    df=read_scrolls(reciever)
    if type(df)==str:
        blanky=pd.DataFrame([[reciever,0,f"0%0;{arg1}%{arg2}"]])
        csv_write(blanky,item,"a")
        return True
    df.loc[arg1,["counts"]]= arg2 if arg1 not in df.index else int(df.loc[arg1,["counts"]]+arg2)
    save_scrolls(reciever,df)
    return True

def checkitem(reciever,arg1,arg2=1): #回覆持有數
    df=read_scrolls(reciever)
    if type(df)==str:
        return 0
    if arg1 not in df.index:
        return 0
    if df.loc[arg1,:].values<arg2:
        return df.loc[arg1,:].values[0]
    return "OK"

def removeitem(reciever,arg1,arg2=1):
    df=read_scrolls(reciever)
    df.loc[arg1,:]-=arg2
    save_scrolls(reciever,df)

def token_redeem(redeem_ID):
    if redeem_ID == "O101":
        a=random.randint(1,100)
    elif redeem_ID == "O201":
        a=random.randint(1,40)+60
    elif redeem_ID == "O301":
        a=100
    if 0<a<=60:
        b=random.choice(["D101","D102"])
    elif 60<a<=95:
        b=random.choice(["D201","D202"])
    elif 95<a<=100:
        b="D301"
    return ch(b)

def createtxt(mes):
    k=round(time.time()*100)
    with open(f'temporary\{k}.txt','a',encoding='utf-8') as txtfile:
        txtfile.writelines(mes)
    return f'temporary\{k}.txt'
    
def gatcha(user_id,adjust_luck=0):    #結果是名字,數字
    onestar = [ele for ele in item_fulldata if item_fulldata[ele]["rarity"]==1 and not ele.startswith("D")]
    twostar = [ele for ele in item_fulldata if item_fulldata[ele]["rarity"]==2 and not ele.startswith("D")]
    threestar = [ele for ele in item_fulldata if item_fulldata[ele]["rarity"]==3 and not ele.startswith("D")]
    dice = adjust_luck + random.randint(1, 100 - adjust_luck)
    if 0<dice<=75:
        gatcharesult=random.choice(onestar)
    elif 75<dice<=95:
        gatcharesult=random.choice(twostar)
    elif 95<dice<=100:
        gatcharesult=random.choice(threestar)
    it_d=item_fulldata[gatcharesult]
    if not it_d["availnum"].isdecimal():
        des=it_d["availnum"].split("t")
        num=random.randint(int(des[0]),int(des[1]))
    else:
        num=int(it_d["availnum"])
    giveitem(user_id,ch(gatcharesult),num)
    return ch(gatcharesult),num

def in_colddown(id):
    time_df=read_time()
    if id not in time_df["playerID"].values:
        blanky=pd.DataFrame([[id,time.time()]])
        csv_write(blanky,timenote,"a")
        return 0
    awaittime = time_df.loc[time_df["playerID"]==id,"time"].values[0]
    if time.time()-awaittime<10:
        a=10-round(time.time()-awaittime)
        return 1 if a==0 else a
    else:
        time_df.loc[time_df["playerID"]==id,"time"]=time.time()
        csv_write(time_df,timenote,"w")
        return 0

embname = lambda embed_message, ctx : embed_message.set_author(name=ctx.author.nick or ctx.author.name, icon_url=ctx.author.avatar_url)
toolong = lambda x: len(x)>1600

class Boss:
    def __init__(self,minhp,maxhp,defaultname):
        self.hp=random.randint(minhp,maxhp)
        self.maxhp=maxhp
        self.minhp=minhp
        self.bosstype=defaultname
        self.name=defaultname
        self.overkilling=False
    def hp_reset(self):
        self.hp=random.randint(self.minhp,self.maxhp)
    def killed(self):
        return self.hp <= 0

boss=Boss(500,1000,"狛克")
boss.hp=0
timelimited=True

###########################################################################################################################
#正式指令開始
class Rpg(Cog_Extension):
    @commands.command()
    async def hit(self,ctx,*args):
        global boss
        global timelimited
        id=ctx.author.id
        args=list(args)
        mult_args=[]
        error_outmes=""
        revived=False
        totaldmg=0
        alloutmes=""

        #非登錄頻道不可使用
        if ctx.channel.id  not in available_channel:
            await ctx.send(f'本頻道不可使用此指令，或者沒有登錄此頻道。')
            return
        
        #把有數量的道具讀進mult_args
        for used_scroll in args:
            if "*" in used_scroll and used_scroll[used_scroll.index("*")+1:].isdecimal() :
                mult_args+=[used_scroll[:used_scroll.index("*")]]*int(used_scroll[used_scroll.index("*")+1:])
            else:
                mult_args+=[used_scroll]
        
        #把arg變成只有道具種類的list
        args=list(set(mult_args))

        #是否有道具名稱錯誤
        for used_scroll in args:
            if used_scroll not in itemdict:
                wrong_list=[ele for ele in args if ele not in itemdict]
                for wrong_scroll in wrong_list:
                    error_outmes+=f"使用**{wrong_scroll}**時發生錯誤！\n找不到此道具，請檢查是否輸入正確。\n"
                break
        
        #args變成ID
        args=[find_id(ele) for ele in args if ele in itemdict]

        #錯誤:不可用兌換道具
        for used_scroll in args:
            if used_scroll.startswith("O"):
                error_outmes+=f"使用**{ch(used_scroll)}**時發生錯誤！\n本道具為兌換用道具，請以以下格式輸入：k!redeem {ch(used_scroll)}\n"
                continue

        #錯誤:B>1種
        b_args=[ele for ele in args if ele.startswith("B")]
        if len(b_args)>1:
            for used_scroll in b_args:
                error_outmes+=f"使用**{ch(used_scroll)}**時發生錯誤！\n傷害保障型卷軸一次只能使用一個！\n"
            args = [ele for ele in args if not ele.startswith("B")]
            b_args=[]

        #錯誤:C>1種
        c_args=[ele for ele in args if ele.startswith("C")]
        if len(c_args)>1:
            for used_scroll in c_args:
                error_outmes+=f"使用**{ch(used_scroll)}**時發生錯誤！\n武器變化型卷軸一次只能使用一個！\n"
            args = [ele for ele in args if not ele.startswith("C")]
            c_args=[]

        d_args=[ele for ele in args if ele.startswith("D") and inf(ele)["move_type"]!="c"]

        #讀出上下限與傷害制限種類
        b_type,c_type,d_type="","",""
        if b_args: #if len(b_args)==1
            b_type=inf(b_args[0])["move_type"]  #a必攻,b必奶
            limitation=inf(b_args[0])["limit"] if inf(b_args[0])["can_combo"]=="N" else 1
        if c_args:
            c_type=inf(c_args[0])["move_type"] #a必攻,b必奶,c都有
            c_moves=inf(c_args[0])["weapons"]
            high_limitation=max([int(ele[3]) for ele in c_moves])
            low_limitation=min([int(ele[2]) for ele in c_moves])
        if d_args:
            d_type="a"
            d_limitation=0
            for d_items in d_args:
                d_limitation=max(inf(d_items)["limit"],d_limitation)

        #錯誤:必攻+必回
        typedic={"a":"必定攻擊","b":"必定回復"}
        final_type=set([ele for ele in [b_type,c_type,d_type] if ele and ele!="c"])
        if len(final_type)>1:
            final_type=set()
            if b_args:
                error_outmes+=f"使用**{ch(b_args[0])}**時發生錯誤！\n不得同時使用必定攻擊型的卷軸與必定回復型的卷軸！(此卷軸為{typedic[b_type]}型卷軸)\n"
                b_args=[]
                args = [ele for ele in args if not ele.startswith("B")]
            if c_args and c_type!="c":
                error_outmes+=f"使用**{ch(c_args[0])}**時發生錯誤！\n不得同時使用必定攻擊型的卷軸與必定回復型的卷軸！(此卷軸為{typedic[c_type]}型卷軸)\n"
                c_args=[]
                args = [ele for ele in args if not ele.startswith("C")]
            if d_args:
                for d_items in d_args:
                    error_outmes+=f"使用**{ch(d_items)}**時發生錯誤！\n不得同時使用必定攻擊型的卷軸與必定回復型的卷軸！(此卷軸為{typedic[d_type]}型卷軸)\n"
                d_args=[]
                args = [ele for ele in args if not ele in d_args]
        
        #錯誤:C的極限達不到滿足B的條件
        if b_type=="a" and d_type=="a":
            limitation=max(limitation,d_limitation)
        if d_type and not b_type:
            limitation=d_limitation
        if c_args and (b_args or d_args):
            if final_type=={"a"} and high_limitation<limitation:
                for ags in b_args+c_args+d_args:
                    error_outmes+=f"使用**{ch(ags)}**時發生錯誤！\n所使用之武器變化型卷軸的傷害上限({high_limitation})小於傷害保障型卷軸或連擊型卷軸的傷害上限({limitation})！\n"
                    args = [ele for ele in args if not ele in b_args+c_args+d_args]
            if final_type=={"b"} and low_limitation>-limitation:
                for ags in b_args+c_args+d_args:
                    error_outmes+=f"使用**{ch(ags)}**時發生錯誤！\n所使用之武器變化型卷軸的補血上限({-low_limitation})小於傷害保障型卷軸或連擊型卷軸的補血上限({limitation})！\n"
                    args = [ele for ele in args if not ele in b_args+c_args+d_args]
        
        #錯誤:抽牌但必定攻擊
        if c_args and c_type=="a" and "D201" in args:
            error_outmes+=f"使用**{ch(c_args[0])}**時發生錯誤！\n不得同時使用必定攻擊型的卷軸與抽牌！(此卷軸為{typedic[c_type]}型卷軸)\n"
            error_outmes+=f"使用**{ch('D201')}**時發生錯誤！\n不得同時使用必定攻擊型的卷軸與抽牌！\n"

        #錯誤訊息印出
        if error_outmes:
            error_mes=discord.Embed(title="❌行動失敗",description=error_outmes)
            embname(error_mes,ctx)
            await ctx.send(embed=error_mes)
            return
        
        #道具數量檢定
        notenoughlist=[ele for ele in set(mult_args) if type(checkitem(id,ele,mult_args.count(ele)))!=str]
        if notenoughlist != []:
            for notenoughitem in notenoughlist:
                error_outmes+=f"使用**{notenoughitem}**時發生錯誤！\n所使用之道具不足！(持有:{checkitem(id,notenoughitem,mult_args.count(notenoughitem))}，使用:{mult_args.count(notenoughitem)})\n"
            error_mes=discord.Embed(title="⚠️道具不足",description=error_outmes)
            embname(error_mes,ctx)
            await ctx.send(embed=error_mes)
            return

        #未冷卻完畢之訊息
        if timelimited and in_colddown(id):
            notcoldmes = await ctx.send(f'{ctx.author.mention}\n本指令有10秒冷卻！您還有{in_colddown(id)}秒！')
            await asyncio.sleep(3)
            await notcoldmes.delete()
            return

        ######此行以下沒有除了變形術以外的return######

        #道具數量字典
        scrolls_dict={}
        for scrolls in set(mult_args):
            scrolls_dict[itemdict[scrolls]]=mult_args.count(scrolls)
        
        #血量重置
        if boss.killed():
            boss=Boss(500,1000,"狛克")
            doblank_dmgrec(damagerec)
            revived=True

        #竹節蟲化
        if "A201" in scrolls_dict:
            boss.name="威爾森"

        #變形術專屬輸入名稱欄位
        try:
            if "A301" in scrolls_dict:
                pen_mes=discord.Embed(title="🖍️變形術！",description="請在此頻道留言你要幫這隻BOSS取的名字。")
                embname(pen_mes,ctx)
                pen_message=await ctx.send(embed=pen_mes)
                def checkb(incmsg):
                    return incmsg.author == ctx.author and incmsg.channel==ctx.channel
                pen_bossname=await self.bot.wait_for("message", timeout=60, check=checkb)
                boss.name=pen_bossname.clean_content
        except asyncio.TimeoutError:
            error_mes=discord.Embed(title="❌超時",description="過久未回覆，已取消行動。")
            embname(error_mes,ctx)
            await pen_message.edit(embed=error_mes)
            return

        ######沒有return了######

        #消耗道具
        for scrolls in scrolls_dict:
            removeitem(id,ch(scrolls),scrolls_dict[scrolls])

        if "X101" in scrolls_dict:
            boss=Boss(3000,5000,"天堂狛克")
            doblank_dmgrec(damagerec)
            heavengrass_mes=discord.Embed(title="⚖️「說吧，讓我聆聽你的願望。」",description=f"你餵食了BOSS天國草，BOSS產生了劇烈的變化！\n天堂{boss.name}降臨！\n").set_footer(text="特殊技能：血量超級厚，掉落道具。")
            embname(heavengrass_mes,ctx)
            await ctx.send(embed=heavengrass_mes)
            revived=True

        if revived:
            if len(read_bosskiller().index)%1000 == 0:
                boss.name=boss.name.replace(boss.name,f"千年{boss.name}")
                transform_mes=discord.Embed(title="🌊特殊事件！",description=f"{boss.name}從湖底甦醒了！\n").set_footer(text="特殊技能：被回血時回復5倍。")
                embname(transform_mes,ctx)
                await ctx.send(embed=transform_mes)
            elif len(read_bosskiller().index)%100 == 0:
                boss.name=boss.name.replace(boss.name,f"百年{boss.name}")
                transform_mes=discord.Embed(title="🏔️特殊事件！",description=f"{boss.name}從山頂躍下！\n").set_footer(text="特殊技能：每次被攻擊固定回復20點血量。")
                embname(transform_mes,ctx)
                await ctx.send(embed=transform_mes)

        if "J101" in scrolls_dict:
            boss.hp_reset()
            revived=True
            
        if "J201" in scrolls_dict:
            for _ in range(scrolls_dict["J201"]):
                boss.hp=round(boss.hp/2)
                boss.hp=1 if boss.hp==0 else boss.hp

        #事先設定保底combo數(D區讀取)
        can_use_combo,critical,lockcount,verticount=0,0,0,0
        while critical<=5:
            critical=random.randint(1,100)
            can_use_combo+=1
        for Ds in [ele for ele in scrolls_dict if ele.startswith("D")]:
            can_use_combo+=inf(Ds)["combos"]*scrolls_dict[Ds]
            lockcount+=1+scrolls_dict[Ds] if Ds=="D101" else 0
            verticount+=1+3*scrolls_dict[Ds] if Ds=="D202" else 0
        if "C303" in scrolls_dict:
            can_use_combo+=random.randint(8,12)

        allcombos=can_use_combo
        uncomboed=0
        first_move=True

        #原本血量紀錄
        old_hp=boss.hp

        #傷害判定=============================================================================
        if "J301" in scrolls_dict:
            boss.hp=random.randint(200,300)
            alloutmes+="你不顧一切的拖著狛克一起跳下懸崖！\n"
            atk=0
            E_allatk=0
            allcombos=0
            uncomboed=0
        while can_use_combo>0 and "J301" not in scrolls_dict:
            textout=""
            WeaponResult=random.choice(c_moves) if c_args else random.choice(read_weapons())
            mvmain1,mvmain2,mvdown,mvup=WeaponResult[0],WeaponResult[1],int(WeaponResult[2]),int(WeaponResult[3])
            atk = 0 if mvup==0 else random.randint(mvdown,mvup)

            #傷害制限
            if b_type or lockcount or verticount:
                if final_type=={"a"} and atk<limitation:
                    continue
                else:
                    lockcount-=(1 if lockcount else 0)
                    verticount-=(1 if verticount else 0)
                if final_type=={"b"} and atk>-limitation:
                    continue
            
            #F區使用
            def F_calc(atk,scrolls_dict,do_Fmult):
                if atk!=0:
                    for F_adds in [ele for ele in scrolls_dict if ele.startswith("F") and inf(ele)["add_or_mult"]=="a"]:
                        o_a=inf(F_adds)["only_attack"]=="a"
                        attckin=atk>0
                        if (o_a and attckin) or not o_a:
                            F_totaldmg=inf(F_adds)["limit"]*scrolls_dict[F_adds]
                            atk+=F_totaldmg if atk>0 else -F_totaldmg
                    if do_Fmult:
                        for F_mults in [ele for ele in scrolls_dict if ele.startswith("F") and inf(ele)["add_or_mult"]=="m"]:
                            o_a=inf(F_mults)["only_attack"]=="a"
                            attckin=atk>0
                            if (o_a and attckin) or not o_a:
                                atk*=inf(F_mults)["limit"]**scrolls_dict[F_mults]
                return atk
            atk = round(F_calc(atk,scrolls_dict,True))

            #千年百年
            if len(read_bosskiller().index)%1000 == 0 and atk<0:
                atk*=5
            if len(read_bosskiller().index)%1000 != 0 and len(read_bosskiller().index)%100 == 0 and not boss.killed():
                boss.hp+=20

            #傷害訊息印出
            if atk==0:
                weapontextout=f'{mvmain1}\n{mvmain2}\n'
            elif mvmain2 == "a":
                weapontextout=f'{mvmain1}\n'
            else:
                weapontextout=f'{mvmain1}{abs(atk)}{mvmain2}\n'
            textout=weapontextout

            #追擊類道具
            E_allatk=0
            for Es in [ele for ele in scrolls_dict if ele.startswith("E")]:
                cond1=Es=="E101" and atk>0 and ("真實" not in weapontextout)
                cond2=Es=="E102" and atk<0
                cond3=Es=="E103" and atk>0 and ("真實" in weapontextout)
                cond4=Es!=("E101" or "E102" or "E103")
                raw_turns=inf(Es)["turns"]
                E_repeat=0
                for _ in range(scrolls_dict[Es]):
                    E_repeat+=int(raw_turns) if raw_turns.isdecimal() else random.randint(int(raw_turns.split("n")[0]),int(raw_turns.split("n")[1]))
                    if cond1 or cond2 or cond3 or cond4:
                        allcombos+=E_repeat
                for _ in range(E_repeat):
                    if Es=="E201":
                        E_atk=mvup if atk<0 else mvdown
                        E_atk = round(F_calc(E_atk,scrolls_dict,False))
                        textout+=f"影子模仿了你的行動！{weapontextout.replace('你','影子').replace(str(atk),str(E_atk))}"
                    elif Es=="E301":
                        E_atk=mvdown if atk<0 else mvup
                        E_atk = round(F_calc(E_atk,scrolls_dict,False))
                        textout+=f"靈獸模仿了你的行動！{weapontextout.replace('你','靈獸').replace(str(atk),str(E_atk))}"
                    elif cond1 or cond2 or cond3 or cond4:
                        E_atk=random.randint(int(inf(Es)["move"][2]),int(inf(Es)["move"][3]))
                        E_atk = round(F_calc(E_atk,scrolls_dict,False))
                        textout+=f'{inf(Es)["move"][0]}{abs(E_atk)}{inf(Es)["move"][1]}\n'
                    else:
                        E_atk=0
                    E_allatk+=E_atk

            #鞭屍判定
            if boss.killed():
                boss.overkilling=True

            #傷害小結算
            boss.hp-=(atk+E_allatk)
            totaldmg+=(atk+E_allatk)
                
            if boss.overkilling:
                alloutmes+="**鞭屍！**"
            elif boss.killed():
                alloutmes+="**尾刀！**"
            elif first_move:
                first_move=False
            else:
                alloutmes+=random.choice(["緊接著","然後","再來","隨即"])
            
            alloutmes+=f"{textout}\n"

            #其他再動判定(不扣can_use)
            uncombo_cond1="D201" in scrolls_dict and atk>0
            uncombo_cond2=b_args and inf(b_args[0])["can_combo"]== "Y" and abs(totaldmg)<inf(b_args[0])["limit"]
            if uncombo_cond1 or uncombo_cond2:
                uncomboed+=1
                continue
            
            #B卷軸效果銷毀
            if b_args:
                if inf(b_args[0])["can_combo"]== "N" or (inf(b_args[0])["can_combo"]== "Y" and abs(totaldmg)>inf(b_args[0])["limit"]):
                    b_args,b_type=[],""

            #行動結束
            can_use_combo-=1

        #寫入傷害表============================================================================
        damage_df=read_damagerec()
        if id not in damage_df["playerID"].values:
            blanky=pd.DataFrame([[id,(atk+E_allatk)]])
            csv_write(blanky,damagerec,"a")
        else:
            damage_df.loc[damage_df["playerID"]==id,"dmg"]+=(atk+E_allatk)
            csv_write(damage_df,damagerec,"w")

        #血量上限
        if boss.hp>1500 and not boss.bosstype=="天堂狛克":
            boss.hp=1500

        #combo回歸
        allcombos+=uncomboed

        fiel1=""
        fiel2=""
        #剩餘血量
        if not boss.killed():
            status_=""
            downhpchange=lambda x:old_hp>=x and boss.hp<x
            uphpchange=lambda x:old_hp<x and boss.hp>=x
            if boss.bosstype=="天堂狛克":
                if downhpchange(200):
                    status_=f'狛克跪地不起！\n'
                elif downhpchange(500):
                    status_=f'狛克面色蒼白！\n'
                elif downhpchange(1500):
                    status_=f'狛克略顯疲態！\n'
                elif uphpchange(200):
                    status_=f'狛克重新站了起來！\n'
            else:
                if downhpchange(100):
                    status_=f'狛克看起來已經沒有力氣掙扎了！\n'
                elif downhpchange(300):
                    status_=f'狛克看起來非常的虛弱！\n'
                elif uphpchange(1500):
                    status_=f'狛克全身散發著神聖的光芒！\n'
                elif uphpchange(1000):
                    status_=f'狛克感到前所未有的亢奮！\n'
                elif uphpchange(100):
                    status_=f'狛克他重新站起來了！\n'
            alloutmes+=f'狛克還有{boss.hp}點血量！\n{status_}'
        else:
            boss.hp=0
            alloutmes+=f'狛克被變成了薩摩耶！\n'
            if "威爾森" in boss.name:
                alloutmes=alloutmes.replace("薩摩耶","竹節蟲")

            #MVP計算
            damage_df=read_damagerec()
            damage_df.sort_values(["dmg"],ascending=False,inplace=True)
            mvp=int(damage_df["playerID"].iloc[0])
            #防止鞭屍後剛好的總輸出=0的尷尬瞬間
            if int(damage_df["dmg"].sum())==0:
                damage_df["playerID"].iloc[0]["dmg"]+=1
            mvp_atkperc=round(int(damage_df["dmg"].max())/int(damage_df["dmg"].sum())*100,1)
            if ctx.guild.get_member(mvp):
                mvp_member=ctx.guild.get_member(mvp)
                mvp_name=mvp_member.nick or mvp_member.name
            else:
                mvp_name=await self.bot.fetch_user(int(mvp))
            alloutmes+=f'本次BOSS輸出之MVP為{str(mvp_name)}，輸出率為{mvp_atkperc}%\n'

            #令牌計算
            if len(read_bosskiller().index)%1000 == 0:
                giveitem(id,"銀令牌")
                giveitem(mvp,"鐵令牌")
                fiel1+="銀令牌×1\n"
                fiel2+="鐵令牌×1\n"
            elif len(read_bosskiller().index)%100 == 0:
                giveitem(id,"鐵令牌")
                giveitem(mvp,"木令牌")
                fiel1+="鐵令牌×1\n"
                fiel2+="木令牌×1\n"
            elif len(read_bosskiller().index)%10 == 0:
                giveitem(id,"木令牌")
                fiel1+="木令牌×1\n"
            
            #紀錄擊殺者
            blanky=pd.DataFrame([[id]])
            csv_write(blanky,boss_killer,"a")
        
        #攻擊者的牙齒/毛計算
        tooth_dice=random.randint(1,100)
        if abs(totaldmg) > 19200: #128combo以上時
            dmgcombo=int(math.log(abs(totaldmg)/150,2)/7*128)
        else:
            dmgcombo=int(abs(totaldmg/150))
        additional_percentage=max(allcombos,dmgcombo)
        for _ in range(additional_percentage):
            tooth_dice+=random.randint(1,10)
        if totaldmg>0:
            tooth_get=int(tooth_dice/105)
        else:
            tooth_get=int(tooth_dice/100)
        if boss.killed():
            tooth_get+=int(random.randint(1,100)/80)

        #防止齒爆
        if tooth_get>30:
            tooth_get=30
        
        #給牙給毛
        if boss.bosstype=="天堂狛克":
            #讓人崩潰的擊殺計算
            if boss.killed():
                tooth_get+=4
                damage_df=read_damagerec()
                damage_df.sort_values(["dmg"],ascending=False,inplace=True)
                #篩出有資格拿的人(每10%1個)
                damage_df["can_have_items"]=damage_df["dmg"]/damage_df["dmg"].sum()*20
                damage_df.loc[:,"can_have_items"]=damage_df["can_have_items"].astype("int64")
                canhave_df=damage_df[damage_df["can_have_items"]>0]
                hv_resultdict={}
                #卡進字典裡(攻擊者的會在攻擊者自己的裡面)
                for n in range(canhave_df.shape[0]):
                    award_str=''
                    for _ in range(canhave_df.iloc[n]["can_have_items"]):
                        resitem,resnum=gatcha(id,(70 if n==0 else 50))
                        award_str+=f"{resnum}個{resitem}\n"
                    if int(canhave_df.iloc[n]["playerID"]) == id:
                        fiel1+=award_str
                    else:
                        hv_resultdict[int(canhave_df.iloc[n]["playerID"])]=award_str
            #攻擊者計算
            for _ in range(tooth_get):
                resitem,resnum=gatcha(id,50)
                fiel1+=f"{resnum}個{resitem}\n"

        else:
            #攻擊者計算
            if totaldmg>0:
                if tooth_get:
                    givetooth(id,tooth_get)
                    fiel1+=f"{tooth_get}顆雪狼牙\n"
            else:
                if tooth_get:
                    givefur(id,tooth_get)
                    fiel1+=f"{tooth_get}根雪狼毛\n"

            #mvp計算
            if boss.killed():
                mvp_dice=random.randint(1,100+round(mvp_atkperc*0.2))
                mvp_tooth=int((mvp_dice+10)/100) if mvp!=id else int((mvp_dice)/100)
                #給牙囉
                if mvp_tooth:
                    givetooth(mvp,mvp_tooth)
                    fiel2+=f"{mvp_tooth}顆雪狼牙\n"            

        #改名   
        if "A101" in scrolls_dict:
            alloutmes=alloutmes.replace("狛克","哈庫瑪瑪塌塌").replace("你","狛克").replace("哈庫瑪瑪塌塌","你")
        alloutmes=alloutmes.replace("狛克",boss.name)
        
        #決定標題
        if revived and boss.killed():
            atktype="💀秒殺！"
        elif boss.killed():
            atktype="🪦擊殺！"
        elif allcombos==1 and ("骨頭" in alloutmes) and ("骨頭" not in boss.name):
            atktype="🦴骨頭！"
        elif allcombos==1 and ("嗚汪啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊" in alloutmes) and ("嗚汪啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊" not in boss.name):
            atktype="😱啊啊啊啊！"
        elif "J301" in scrolls_dict:
            atktype="💥同生共死！"
        elif totaldmg>0:
            atktype="⚔️攻擊！"
        elif totaldmg<0:
            atktype="💚補血！"
        else:
            atktype="🐺攻擊...？"

        #最終印出
        if not toolong(alloutmes):
            hitembedmes=discord.Embed(title=atktype,description=alloutmes)
        else:
            outfile=discord.File(createtxt(alloutmes))
            hitembedmes=discord.Embed(title=atktype,description="訊息過長，輸出訊息請見txt檔。")
        embname(hitembedmes,ctx)
        if fiel1:
            hitembedmes.add_field(name="你得到了：",value=fiel1, inline=True)
        if fiel2:
            hitembedmes.add_field(name="MVP得到了：",value=fiel2, inline=True)
        if boss.bosstype=="天堂狛克" and boss.killed():
            for haver in hv_resultdict:
                haver_name=await self.bot.fetch_user(haver)
                hitembedmes.add_field(name=f"{str(haver_name)}得到了：",value=hv_resultdict[haver], inline=True)
        hitembedmes.set_footer(text=f"Tips:{random.choice(tips)}")

        #訊息發送
        if "威爾森" in boss.name:
            hahahalol=discord.File("bug.gif")
        else:
            hahahalol=discord.File(random.choice(gifs["samoyed"]))

        if boss.killed() and toolong(alloutmes):
            await ctx.send(embed=hitembedmes,files=[outfile,hahahalol])
        elif boss.killed():
            await ctx.send(embed=hitembedmes,file=hahahalol)
        elif toolong(alloutmes):
            await ctx.send(embed=hitembedmes,file=outfile)
        else:
            await ctx.send(embed=hitembedmes)

        #次數紀念的恭喜訊息
        secmes=""    #second message
        if boss.killed():
            if len(read_bosskiller().index)%10 == 1:
                secmes+=f"你是第{len(read_bosskiller().index)-1}個把狛克變成薩摩耶的玩家！"
            if read_bosskiller()["playerID"].value_counts()[id]%5 == 0:
                secmes+=f"你目前已經把狛克變成薩摩耶{read_bosskiller()['playerID'].value_counts()[id]}次了！"
        if secmes:
            secmes+=discord.Embed(title="🎉恭喜",description=f"你是第{len(read_bosskiller().index)-1}個把狛克變成薩摩耶的玩家！")
            embname(secmes,ctx)
            await ctx.send(embed=secmes)

####################################################################################################################################
    @commands.command()
    async def bosskill(self,ctx):
        await ctx.send(f'{ctx.author.mention}\n狛克已經變成薩摩耶{len(read_bosskiller().index)}次了！')

    @commands.command()
    async def mykill(self,ctx):
        bosskill_count_series=read_bosskiller()["playerID"].value_counts()
        if ctx.author.id in read_bosskiller()["playerID"].value_counts():
            userkills=bosskill_count_series[ctx.author.id]
        else:
            userkills=0
        await ctx.send(f'{ctx.author.mention}\n你目前已經把狛克變成薩摩耶{userkills}次了！')

    @commands.command()
    async def bosshp(self,ctx):
        global boss
        if boss.killed():
            await ctx.send(f'{ctx.author.mention}\n你拿起偵測儀對著狛克一陣亂拍。\n偵測儀顯示狛克現在還沒復活！')
        else:
            await ctx.send(f'{ctx.author.mention}\n你拿起偵測儀對著狛克一陣亂拍。\n偵測儀顯示狛克現在還有{boss.hp}點血量！')

    @commands.command()
    async def gatcha(self,ctx,arg='1'):
        if not arg.isdecimal():
            await ctx.send(f'{ctx.author.mention}\n消耗雪狼牙數請輸入整數-w-...')
            return

        if not 0<int(arg)<=10:
            await ctx.send(f'{ctx.author.mention}\n消耗雪狼牙數請輸入1到10-w-...')
            return
        
        enough_tooth=removetooth(ctx.author.id,int(arg))
        if type(enough_tooth)!=bool: #bool時耗牙已經完成
            await ctx.send(f'{ctx.author.mention}\n你的雪狼牙數量貌似不足呢-w-...\n(擁有:{enough_tooth},消耗:{arg})')
            return
        
        embedmes1=discord.Embed(title="☘️召喚！", description=f'消耗{int(arg)}個雪狼牙佈陣！\n進行{int(arg)}次召喚！') 
        embname(embedmes1,ctx)
        sentembed = await ctx.send(embed=embedmes1)
        await asyncio.sleep(3)

        embedmes2=discord.Embed(title="🍀召喚！", description=f'消耗{int(arg)}個雪狼牙佈陣！\n進行{int(arg)}次召喚！\n你獲得了：')
        embname(embedmes2,ctx)
        for i in range(int(arg)):
            itemname,itemcount=gatcha(ctx.author.id,50) if i==9 else gatcha(ctx.author.id,0)
            embedmes2.add_field(name=f"{itemcount}個[{inf(itemdict[itemname])['rarity']*'☆'}]**{itemname}**",
                                value=inf(itemdict[itemname])['description'],
                                inline=True)
        await sentembed.edit(embed=embedmes2)

    @commands.command()
    async def redeem(self,ctx,arg1="",arg2='1'):
        if arg1 == "":
            await ctx.send(f'{ctx.author.mention}\n您似乎沒有說明要兌換什麼令牌呢-w-...')
            return
        if not (arg1 in itemdict and itemdict[arg1].startswith("O")):
            await ctx.send(f'{ctx.author.mention}\n這東西似乎不是令牌呢...\n請確定您輸入的是不含稀有度的令牌全名-w-...')
            return
        if not arg2.isdecimal():
            await ctx.send(f'{ctx.author.mention}\n雖然可以輸入要使用的令牌數量...\n不過令牌名稱後面的那個似乎不是整數呢-w-...')
            return
        if int(arg2)<1:
            await ctx.send(f'{ctx.author.mention}\n數量不能是0啦你是在哭喔-w-...')
            return
        if int(arg2)>10:
            await ctx.send(f'{ctx.author.mention}\n太多了啦，一次10個就好-w-...')
            return
        enough_token=checkitem(ctx.author.id,arg1,int(arg2))    
        if enough_token!="OK":
            await ctx.send(f'{ctx.author.mention}\n你這個令牌不夠啦-w-...\n(擁有:{enough_token},消耗:{arg2})')
            return
        
        removeitem(ctx.author.id,arg1,int(arg2))
        
        embedmes1=discord.Embed(title="⏳兌換！", description=f'支付{int(arg2)}個{arg1}！\n等待老闆尋找卷軸-w-...') 
        embname(embedmes1,ctx)
        sentembed = await ctx.send(embed=embedmes1)
        await asyncio.sleep(3)

        embedmes2=discord.Embed(title="⌛兌換！", description=f'支付{int(arg2)}個{arg1}！\n回來啦回來啦-w-...\n你獲得了：')
        embname(embedmes2,ctx)
        for _ in range(int(arg2)):
            tokenget=token_redeem(itemdict[arg1])
            giveitem(ctx.author.id,tokenget)
            embedmes2.add_field(name=f"1個[{inf(itemdict[tokenget])['rarity']*'☆'}]**{tokenget}**",
                                value=inf(itemdict[tokenget])['description'],
                                inline=True)
        await sentembed.edit(embed=embedmes2)

    @commands.command()
    async def myitem(self,ctx):
        myitemuser=ctx.author
        id=myitemuser.id
        item_df=read_item()
        fur_df=read_fur()
        toothcount = int(item_df.loc[item_df["playerID"]==id,"tooths"]) if id in item_df["playerID"].values else 0
        furcount = int(fur_df.loc[fur_df["playerID"]==id,"furs"]) if id in fur_df["playerID"].values else 0

        outmes="您的持有道具如下：\n"
        outmes+=f"雪狼牙：{toothcount}顆\n"
        outmes+=f"雪狼毛：{furcount}顆\n"
        outmes+=f"持有道具：\n"
        itemmes=""
        scroll_df=read_scrolls(id)
        if type(scroll_df)==str:
            itemmes="無。"
        else:
            scroll_dict=scroll_df.to_dict("index")
            del scroll_dict["0"]
            for scrolls in item_fulldata:
                if ch(scrolls) in scroll_dict and scroll_dict[ch(scrolls)]["counts"]>0:
                    itemmes+=f'[{item_fulldata[scrolls]["rarity"]*"☆"}]**{ch(scrolls)}**：{scroll_dict[ch(scrolls)]["counts"]}個\n'
                    itemmes+=f'[{item_fulldata[scrolls]["description"]}]\n\n'
        
        if itemmes=="":
            itemmes="無。"

        if toolong(itemmes):
            outfile=discord.File(createtxt(itemmes))
            await ctx.send(f'{ctx.author.mention}\n{outmes}道具數量過多，請見附檔。',file=outfile)
        else:
            await ctx.send(f'{ctx.author.mention}\n{outmes}{itemmes}')
            
    @commands.command()
    async def hitrank(self,ctx):            
        killer_series=read_bosskiller()["playerID"].value_counts().sort_values(ascending=False)
        outmes=""
        for n in range(10):
            killer_id,killer_times=killer_series.index.values[n],killer_series.iloc[n]
            if ctx.guild.get_member(killer_id):
                mvp_member=ctx.guild.get_member(killer_id)
                killer_name=mvp_member.nick or mvp_member.name
            else:
                killer_name=await self.bot.fetch_user(int(killer_id))
            outmes+=f"第{killer_series.to_list().index(killer_times)+1}名:{killer_name}({killer_times}次)\n"
        await ctx.send(f'{ctx.author.mention}\n目前把狛克變成薩摩耶次數的前10名排行榜：\n{outmes}')

    @commands.command()
    async def furshop(self,ctx,arg1="",arg2="1"):
        outmes=""
        if arg1=="" and arg2=="1":
            embedmes=discord.Embed(title="🪶雪狼毛商店！",description="歡迎來到雪狼毛商店汪！") 
            embedmes.set_thumbnail(url="https://images.plurk.com/zhIdDrzyyu8IwQCJXUAkR.png")
            embedmes.set_footer(text="輸入k!furshop (品項名稱) (數量)來用雪狼毛購買商品汪！\n繪師:Moyu")
            shoplist=[elem for elem in furryshop]
            for count in range(0,len(furryshop)):
                outmes+=f"{count+1}.{shoplist[count]}(價格：{furryshop[shoplist[count]]})\n"
                embedmes.add_field(name=f"{count+1}.{shoplist[count]}(價格：{furryshop[shoplist[count]]})",
                                    value=f"{inf(itemdict[shoplist[count]])['description']}",
                                    inline=True)
            embname(embedmes,ctx)
            await ctx.send(embed=embedmes)
        elif arg1 in furryshop:
            if not arg2.isdecimal():
                await ctx.send(f"{ctx.author.mention}\n商品數量請輸入整數汪！")
                return
            costfur=int(arg2)*furryshop[arg1]
            enough_fur=removefur(ctx.author.id,costfur)
            if type(enough_fur)!=bool:
                await ctx.send(f"{ctx.author.mention}\n你的雪狼毛不夠汪...\n總共需要{costfur}個，你只有{enough_fur}個汪！")
                return
            giveitem(ctx.author.id,arg1,int(arg2))
            embedmes=discord.Embed(title="🪶成交！",description=f"以{costfur}撮雪狼毛獲得了{arg2}個{arg1}！")
            embedmes.set_thumbnail(url="https://images.plurk.com/zhIdDrzyyu8IwQCJXUAkR.png")
            embedmes.set_footer(text="輸入k!furshop (品項名稱) (數量)來用雪狼毛購買商品汪！\n繪師:Moyu")
            embname(embedmes,ctx)
            await ctx.send(embed=embedmes)
        else:
            await ctx.send(f"{ctx.author.mention}\n無法辨識汪！請確定商品編號正確汪！")

    @commands.command()
    async def index(self,ctx,*args):
        outmes=""
        dicting1={"A":"改名型卷軸","B":"傷害保障型卷軸","C":"武器變化類卷軸","D":"連擊型卷軸","E":"追擊類卷軸","F":"傷害變化型卷軸","J":"血量改寫型卷軸","O":"令牌","X":"召喚類卷軸"}
        dicting2={"1":"[☆]道具","2":"[☆☆]道具","3":"[☆☆☆]道具"}
        if not args:
            outmes+=f"輸入[k!index (種類代碼)]來查詢卷軸圖鑑！\n"
            for everything in dicting1:
                outmes+=f"{everything}：{dicting1[everything]}\n"
            for everything in dicting2:
                outmes+=f"{everything}：{dicting2[everything]}\n"
        elif all([ele in {**dicting1,**dicting2} for ele in args]):
            #先篩出符合條件的
            res_scrolls=[]
            cond1=[ele for ele in args if ele in dicting1]
            cond2=[ele for ele in args if ele in dicting2]
            if cond1:
                for scrtype in [ele for ele in args if ele in dicting1]:
                    res_scrolls+=[ele for ele in item_fulldata if ele.startswith(scrtype)]
            else:
                res_scrolls=item_fulldata
            result_scrolls=[]
            if cond2:
                for scrrairity in [ele for ele in args if ele in dicting2]:
                    result_scrolls+=[ele for ele in res_scrolls if inf(ele)["rarity"]==int(scrrairity)]
            else:
                result_scrolls=res_scrolls

            #該開始翻資料囉喔喔喔
            Cdicting={"a":"必定攻擊","b":"必定補血","c":"可能為攻擊或補血"}
            for item in result_scrolls:
                outmes+=f"[{inf(item)['rarity']*'☆'}]**{ch(item)}** (一單位：{inf(item)['availnum'].replace('t','到')}個)\n"
                outmes+=f"{inf(item)['description']}\n"
                if item.startswith("C"):
                    c_moves=inf(item)["weapons"]
                    high_limitation=max([int(ele[3]) for ele in c_moves])
                    low_limitation=min([int(ele[2]) for ele in c_moves])
                    outmes+=f"(行動型態：{Cdicting[inf(item)['move_type']]})\n"
                    outmes+=f"(行動數值範圍：{low_limitation}~{high_limitation})\n"
                outmes+=f"\n"
        else:
            outmes+=f"無法辨識！請確定代碼正確！"
        if toolong(outmes):
            outfile=discord.File(createtxt(outmes))
            await ctx.send(f'{ctx.author.mention}\n文字過多，請見附檔。',file=outfile)
        else:
            await ctx.send(f'{ctx.author.mention}\n{outmes}')
        
def setup(bot):
    bot.add_cog(Rpg(bot))