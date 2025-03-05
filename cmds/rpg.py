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

furfile="csvfile\\furcount.csv"
damagerec="csvfile\\damagerec.csv"
timenote="csvfile\\timelimit.csv"
boss_killer="csvfile\\killed.csv"
rpgweapon="csvfile\\rpgweapon.csv"
specialrpgweapon="csvfile\\specialrpgweapon.csv"

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

find_id = lambda items : itemdict[items] #中文名字轉ID
inf = lambda item_id : item_fulldata[item_id] #ID轉完整資訊(dict)
ch = lambda item_id : item_fulldata[item_id]['name'] #ID轉中文名字

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

#傷害紀錄表專屬的全清空
def doblank_dmgrec(file):
    blanky=pd.DataFrame([[]])
    csv_write(blanky,file,"w")

#讀取道具表
def read_item():
    with open('csvfile\\item.json','r',encoding='utf-8') as jfile:
        it_dict=json.load(jfile)
    return it_dict

#儲存修改完的道具表
def save_item(dct):
    with open('csvfile\\item.json','w',encoding='utf-8') as it:
        json.dump(dct,it,ensure_ascii=False,indent=4)
    return 'okay'

#讀取時間限制列表
def read_time():
    df=doread(timenote,["playerID","time","uncolddown"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    df.loc[:,"time"]=df["time"].astype("float64")
    df.loc[:,"uncolddown"]=df["uncolddown"].astype("int64")
    return df

#讀取BOSS擊殺者列表
def read_bosskiller():
    df=doread(boss_killer,["playerID"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    return df

#讀取武器表 #串列注意
def read_weapons(file):
    with open(file,'r',encoding='utf-8') as jfile:
        alllines=[]
        raw_data=jfile.readlines()
        for lines in raw_data:
            alllines.append(lines.strip('\n').strip(' ').split(','))
    return alllines

#讀取傷害紀錄表
def read_damagerec():
    df=doread(damagerec,["playerID","dmg"])
    df.loc[:,"playerID"]=df["playerID"].astype("int64")
    df.loc[:,"dmg"]=df["dmg"].astype("int64")
    return df

#讀取玩家道具
def read_scrolls(id):
    it_dict=read_item()
    if str(id) not in it_dict:
        return "Not found"
    return it_dict[str(id)]["items"]

#把改完的道具df寫回道具表
def save_scrolls(id,it_dict):
    dct=read_item()
    dct[str(id)]["items"]=it_dict
    save_item(dct)
    return "okay"

#給牙齒
def givetooth(id,how_many):
    dct=read_item()
    if str(id) in dct:
        dct[str(id)]["tooths"]+=how_many
        save_item(dct)
    else:
        dct[str(id)]={"tooths": how_many,"furs": 0,"items": {}}
        save_item(dct)

#消耗牙齒       #不夠時回報現有數量 #夠時回報True
def removetooth(id,how_many):
    dct=read_item()
    if str(id) in dct:
        available_tooth=dct[str(id)]["tooths"]
        if available_tooth < how_many:
            return available_tooth
        else:
            dct[str(id)]["tooths"]-=how_many
            save_item(dct)
            return True
    else:
        return 0

#給毛
def givefur(id,how_many):
    dct=read_item()
    if str(id) in dct:
        dct[str(id)]["furs"]+=how_many
        save_item(dct)
    else:
        dct[str(id)]={"tooths": 0,"furs": how_many,"items": {}}
        save_item(dct)

#消耗毛     #不夠時回報現有數量 #夠時回報True
def removefur(id,how_many):
    dct=read_item()
    if str(id) in dct:
        available_furs=dct[str(id)]["furs"]
        if available_furs < how_many:
            return available_furs
        else:
            dct[str(id)]["furs"]-=how_many
            save_item(dct)
            return True
    else:
        return 0

#給道具
def giveitem(reciever,arg1,arg2=1):       #receiver是int,arg1是物品名稱 #沒有辨識arg2是否為int的功能
    if arg1 == "":
        return '您似乎沒有說明要使用什麼呢-w-...'
    if arg1 not in itemdict:
        return '這個東西似乎名稱不對呢-w-...\n請確定您輸入的是不含稀有度的道具全名-w-...'
    scr_dct=read_scrolls(reciever)
    if type(scr_dct)==str:
        scr_dct[str(id)]={"tooths": 0,"furs": 0,"items": {arg1:arg2}}
        save_scrolls(reciever,scr_dct)
        return True
    scr_dct[arg1]= arg2 if arg1 not in scr_dct else scr_dct[arg1]+arg2
    save_scrolls(reciever,scr_dct)
    return True

#檢查是否持有足夠道具
def checkitem(reciever,arg1,arg2=1): #回覆持有數
    scr_dct=read_scrolls(reciever)
    if type(scr_dct)==str:
        return 0
    if arg1 not in scr_dct:
        return 0
    if scr_dct[arg1]<arg2:
        return scr_dct[arg1]
    return "OK"

#消耗道具
def removeitem(reciever,arg1,arg2=1):
    scr_dct=read_scrolls(reciever)
    scr_dct[arg1]-=arg2
    save_scrolls(reciever,scr_dct)

#令牌的抽獎
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

#字數爆掉時創造txt用的臨時檔案
def createtxt(mes):
    k=round(time.time()*100)
    with open(f'temporary\{k}.txt','a',encoding='utf-8') as txtfile:
        txtfile.writelines(mes)
    return f'temporary\{k}.txt'
    
#抽卷軸
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

#回報玩家的冷卻秒數
def in_colddown(id,extra_time=0):
    time_df=read_time()
    if extra_time==0:
        if id not in time_df["playerID"].values:
            blanky=pd.DataFrame([[id,time.time()+5,0]])
            csv_write(blanky,timenote,"a")
            return 0
        awaittime = time_df.loc[time_df["playerID"]==id,"time"].values[0]
        if awaittime-time.time()>0:
            a=round(awaittime-time.time())
            time_df.loc[time_df["playerID"]==id,"uncolddown"]+=1
            csv_write(time_df,timenote,"w")
            return 1 if a==0 else a
        else:
            time_df.loc[time_df["playerID"]==id,"time"]=time.time()+5
            time_df.loc[time_df["playerID"]==id,"uncolddown"]=0
            csv_write(time_df,timenote,"w")
            return 0
    else:
        time_df.loc[time_df["playerID"]==id,"time"]+=extra_time
        csv_write(time_df,timenote,"w")


def read_story(id):        #回報list
    it_dict=read_item()
    if str(id) not in it_dict:
        return []
    return it_dict[str(id)].get("story",[])

def check_chapter(id):
    strylst=read_story(id)
    fst_chap=[1,2,3]
    sec_chap=fst_chap+[4,5,6,7]
    trd_chap=sec_chap+[8,9,10,11]
    fth_chap=trd_chap+[12,13]
    strychck = lambda chap,lst : all(ele in lst for ele in chap)
    if strychck(fth_chap,strylst):
        return "終幕"
    elif strychck(trd_chap,strylst):
        return "第四節"
    elif strychck(sec_chap,strylst):
        return "第三節"
    elif strychck(fst_chap,strylst):
        return "第二節"
    else:
        return "第一節"

def givestory(id):
    it_dict=read_item()
    #新手初始化
    if str(id) not in it_dict:
        it_dict[str(id)]={"tooths":0,"furs": 0,"items": {}}
    #讀取故事與當前章節
    stories = it_dict[str(id)].setdefault("story",[])
    chaptering=check_chapter(id)
    #選擇不重複的故事給予
    def selectedstory(itdct,gvelst):
        while True:
            gve=random.choice(gvelst)
            if gve not in itdct[str(id)]["story"]:
                break
        return gve

    if chaptering=="終幕":
        return 0,False    #已全部獲得
    elif chaptering=="第四節":
        gvstry=selectedstory(it_dict,[12,13])
    elif chaptering=="第三節":
        gvstry=8 if 8 not in stories else selectedstory(it_dict,[9,10,11])
    elif chaptering=="第二節":
        gvstry=selectedstory(it_dict,[4,5,6,7])
    else:
        gvstry=selectedstory(it_dict,[1,2,3])
    it_dict[str(id)]["story"].append(gvstry)
    chapterchanged = True if any(ele==len(it_dict[str(id)]["story"]) for ele in (3,7,11,13)) else False
    save_item(it_dict)
    return gvstry,chapterchanged

def scrolldebugging(mult_args):

    #把arg變成只有道具種類的list
    args=list(set(mult_args))

    #是否有道具名稱錯誤
    for used_scroll in args:
        if used_scroll not in itemdict:
            return False
    
    #args變成ID
    args=[find_id(ele) for ele in args if ele in itemdict]

    #錯誤:不可用兌換道具
    for used_scroll in args:
        if used_scroll.startswith("O"):
            return False

    #錯誤:B>1種
    b_args=[ele for ele in args if ele.startswith("B")]
    if len(b_args)>1:
        return False

    #錯誤:C>1種
    c_args=[ele for ele in args if ele.startswith("C")]
    if len(c_args)>1:
        return False

    d_args=[ele for ele in args if ele.startswith("D") and inf(ele)["move_type"]!="c"]

    #讀出上下限與傷害制限種類
    b_type,c_type,d_type="","",""
    if b_args: 
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
    final_type=set([ele for ele in [b_type,c_type,d_type] if ele and ele!="c"])
    if len(final_type)>1:
        return False
    
    #錯誤:C的極限達不到滿足B的條件
    if b_type=="a" and d_type=="a":
        limitation=max(limitation,d_limitation)
    if d_type and not b_type:
        limitation=d_limitation
    if c_args and (b_args or d_args):
        if final_type=={"a"} and high_limitation<limitation:
            return False
        if final_type=={"b"} and low_limitation>-limitation:
            return False
    
    #錯誤:無盡但必定攻擊
    if c_args and c_type=="a" and "D201" in args:
        return False

    #道具數量字典
    scrolls_dict={}
    for scrolls in set(mult_args):
        scrolls_dict[itemdict[scrolls]]=mult_args.count(scrolls)

    if b_args and scrolls_dict[b_args[0]]>1:
        return False
    if c_args and scrolls_dict[c_args[0]]>1:
        return False
    
    #沒問題
    return True

#embed設定author
embname = lambda embed_message, ctx : embed_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
#爆字數檢定
toolong = lambda x: len(x)>1600

#這是一隻BOSS!
class Boss:
    def __init__(self,minhp,maxhp,defaultname):
        self.hp=random.randint(minhp,maxhp)
        self.maxhp=maxhp
        self.minhp=minhp
        self.bosstype=defaultname   #這個不動
        self.name=defaultname       #這個拿來改
        self.overkilling=False
        self.distancing=0
    def hp_reset(self):
        self.hp=random.randint(self.minhp,self.maxhp)
    def killed(self):
        return self.hp <= 0

boss=Boss(500,1000,"狛克")
boss.hp=0
timelimited=True
twinlimittimes=0

###########################################################################################################################
#正式指令開始
class Rpg(Cog_Extension):
    @commands.command()
    async def hit(self,ctx,*args):
        global boss
        global timelimited
        global twinlimittimes
        id=ctx.author.id
        args=list(args)
        mult_args=[]
        error_outmes=""
        revived=False
        totaldmg=0
        alloutmes=""

        #非登錄頻道不可使用
        with open('csvfile\\allowchannel.json','r',encoding='utf-8') as jfile:
            allowchannel=json.load(jfile)
        available_channel=allowchannel["allowedchannel"]
        if ctx.channel.id  not in available_channel:
            await ctx.send(f'本頻道不可使用此指令，或者沒有登錄此頻道。')
            return

        if boss.bosstype=="小偷" and args:
            error_mes=discord.Embed(title="❌卷軸無效",description="不可對當前的BOSS使用卷軸！")
            embname(error_mes,ctx)
            await ctx.send(embed=error_mes)
            return
        
        #把有數量的道具讀進mult_args
        for used_scroll in args:
            if "*" in used_scroll and used_scroll[used_scroll.index("*")+1:].isdecimal() :
                mult_args+=[used_scroll[:used_scroll.index("*")]]*int(used_scroll[used_scroll.index("*")+1:])
            else:
                mult_args+=[used_scroll]

        #地獄級別難度指令--卷軸手稿
        if scrolldebugging(mult_args) and "卷軸手稿" in mult_args:
            scriptbreakinto=[]
            safelist=[ele for ele in item_fulldata if not any([ele.startswith("X"),ele.startswith("O"),ele=="K301",ele=="J301"])]
            for _ in range(mult_args.count("卷軸手稿")):
                for _ in range(random.randint(5,8)):
                    while True:
                        #試試看
                        experiency_scroll=ch(random.choice(safelist))
                        experiency_mult_args=mult_args+[experiency_scroll]
                        if scrolldebugging(experiency_mult_args):
                            mult_args+=[experiency_scroll]
                            giveitem(id,experiency_scroll)
                            scriptbreakinto+=[experiency_scroll]
                            break
            heavengrass_mes=discord.Embed(title="📋️分裂！",description=f"手稿上凌亂的文字產生了各種效果！\n本次行動額外獲得以下卷軸之效果：{'、'.join(scriptbreakinto)}\n")
            embname(heavengrass_mes,ctx)
            await ctx.send(embed=heavengrass_mes)
        
        #把arg變成只有道具種類的list
        args=list(set(mult_args))

        #是否有道具名稱錯誤
        wrong_list=[ele for ele in args if ele not in itemdict]
        if wrong_list:
            for wrong_scroll in wrong_list:
                error_outmes+=f"使用**{wrong_scroll}**時發生錯誤！\n找不到此道具，請檢查是否輸入正確。\n"
            error_mes=discord.Embed(title="❌卷軸無效",description=f"{error_outmes}")
            embname(error_mes,ctx)
            await ctx.send(embed=error_mes)
            return
        
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
        
        #錯誤:無盡但必定攻擊
        if c_args and c_type=="a" and "D201" in args:
            error_outmes+=f"使用**{ch(c_args[0])}**時發生錯誤！\n不得同時使用必定攻擊型的卷軸與無盡！(此卷軸為{typedic[c_type]}型卷軸)\n"
            error_outmes+=f"使用**{ch('D201')}**時發生錯誤！\n不得同時使用必定攻擊型的卷軸與無盡！\n"

        #道具數量字典
        scrolls_dict={}
        for scrolls in set(mult_args):
            scrolls_dict[itemdict[scrolls]]=mult_args.count(scrolls)


        if b_args and scrolls_dict[b_args[0]]>1:
            error_outmes+=f"使用**{ch(b_args[0])}**時發生錯誤！\n傷害保障型卷軸一次只能使用一個！\n"
        if c_args and scrolls_dict[c_args[0]]>1:
            error_outmes+=f"使用**{ch(c_args[0])}**時發生錯誤！\n武器變化型卷軸一次只能使用一個！\n"

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
            time_df=read_time()
            if time_df.loc[time_df["playerID"]==id,"uncolddown"].values[0]<3:
                unc_mes=f"本指令有5秒冷卻！您還有{in_colddown(id)}秒！"
            else:
                unc_mes=f"本指令有5秒冷卻！您還有{in_colddown(id)}...欸不是你到底有完沒完！"
            notcoldmes = await ctx.send(f'{ctx.author.mention}\n{unc_mes}')
            await asyncio.sleep(3)
            await notcoldmes.delete()
            return

        ######此行以下沒有除了變形術以外的return######
        
        #血量重置 #重生
        if boss.killed() or "J101" in scrolls_dict:
            #吟遊機制
            specialkomaroudice=random.randint(1,100)
            poeted=1<=specialkomaroudice<=2
            twined=3<=specialkomaroudice<=6
            enpowered=7<=specialkomaroudice<=8
            theifappear=specialkomaroudice==9
            if poeted:
                boss=Boss(500,1000,"吟遊狛克")
                heavengrass_mes=discord.Embed(title="🪕「旅人們啊，是否願意駐足？」",description=f"吟遊狛克不請自來！\n").set_footer(text="特殊技能：被攻擊時機率無效化整次行動，所有參與戰鬥者獲得故事碎片。")
                embname(heavengrass_mes,ctx)
                await ctx.send(embed=heavengrass_mes)
            elif twined:
                boss=Boss(500,600,"半融合狛克")
                heavengrass_mes=discord.Embed(title="🎁「『來玩吧。』」",description=f"半融合狛克前來！\n").set_footer(text="特殊技能：半融合狛克在10回合後會完全融合成2倍血量的普通狛克。完全融合前雪狼毛掉落率上升一倍，且擊敗時尾刀者獎勵大幅增加。")
                embname(heavengrass_mes,ctx)
                twinlimittimes=11
                await ctx.send(embed=heavengrass_mes)
            elif enpowered:
                boss=Boss(500,1000,"巨尾狛克")
                heavengrass_mes=discord.Embed(title="👊「嘎吼吼吼吼吼！」",description=f"你遇到了尾巴超大的狛克！\n").set_footer(text="特殊技能：單次傷害超過150時，會反過來打你。MVP獎勵大幅上升。")
                embname(heavengrass_mes,ctx)
                await ctx.send(embed=heavengrass_mes)
            elif theifappear:
                boss=Boss(1000,1000,"小偷")
                heavengrass_mes=discord.Embed(title="💸『來人啊！抓小偷啊！』",description=f"小偷從卷軸商人家中衝出！\n別跟丟小偷了！\n\n追捕模式：\n不可使用卷軸。\n使用k!hit以攻擊小偷，小偷每回合會試著與玩家方拉開距離，距離超過30米後會跟丟。\n使用k!slow可以拉近與小偷的距離。")
                embname(heavengrass_mes,ctx)
                await ctx.send(embed=heavengrass_mes)
                boss.distancing=5
                for scroll in scrolls_dict:
                    giveitem(id,ch(scroll),scrolls_dict[scroll])
                return
            else:
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

        if "X102" in scrolls_dict:
            boss=Boss(500,1000,"吟遊狛克")
            doblank_dmgrec(damagerec)
            heavengrass_mes=discord.Embed(title="🪕「此等美妙樂章，敢問能否共奏？」",description=f"你演奏了上古樂譜！\n吟遊狛克被美妙的樂曲吸引而來！\n").set_footer(text="特殊技能：被攻擊時機率無效化整次行動，所有參與戰鬥者獲得故事碎片。")
            embname(heavengrass_mes,ctx)
            await ctx.send(embed=heavengrass_mes)
            revived=True

        if "X101" in scrolls_dict:
            boss=Boss(3000,5000,"天堂狛克")
            doblank_dmgrec(damagerec)
            heavengrass_mes=discord.Embed(title="⚖️「說吧，讓我聆聽你的願望。」",description=f"你餵食了BOSS天國草，BOSS產生了劇烈的變化！\n天堂{boss.name}降臨！\n").set_footer(text="特殊技能：血量超級厚，掉落道具。")
            embname(heavengrass_mes,ctx)
            await ctx.send(embed=heavengrass_mes)
            revived=True

        if revived and not boss.bosstype=="小偷":
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

        #分離
        if "J201" in scrolls_dict:
            for _ in range(scrolls_dict["J201"]):
                boss.hp=round(boss.hp/2)
                boss.hp=1 if boss.hp==0 else boss.hp

        #事先設定保底combo數(D區讀取)
        can_use_combo,critical,lockcount,verticount=0,0,0,0
        while critical<=5:  #5%再行動
            critical=random.randint(1,100)
            can_use_combo+=1
        for Ds in [ele for ele in scrolls_dict if ele.startswith("D")]:
            can_use_combo+=inf(Ds)["combos"]*scrolls_dict[Ds]
            lockcount+=1+scrolls_dict[Ds] if Ds=="D101" else 0
            verticount+=1+3*scrolls_dict[Ds] if Ds=="D202" else 0
        if "C303" in scrolls_dict:      #貓之海
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

            #隨機行動
            if boss.bosstype=="小偷":
                WeaponResult=random.choice(read_weapons(specialrpgweapon))
                mvtype,mvdistance,mvmisspercentage,mvatk=WeaponResult[0],int(WeaponResult[1]),int(WeaponResult[2]),int(WeaponResult[3])
                pineapple=0 if mvdistance>boss.distancing else boss.distancing/mvdistance-1
                mvaimed=(random.randint(1,100)-(100*pineapple-mvmisspercentage*(1-pineapple)))>0
                atk=mvatk if mvaimed else 0
            else:
                hasC = [ele for ele in args if ele.startswith("C")]
                WeaponResult=random.choice(inf(hasC[0])["weapons"]) if hasC else random.choice(read_weapons(rpgweapon))
                mvmain1,mvmain2,mvdown,mvup=WeaponResult[0],WeaponResult[1],int(WeaponResult[2]),int(WeaponResult[3])
                atk = 0 if mvup==0 else random.randint(mvdown,mvup)
                atk = boss.hp if mvup==10000 else atk

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
            if "狛克" in boss.bosstype:
                if len(read_bosskiller().index)%1000 == 0 and atk<0:
                    atk*=5
                if len(read_bosskiller().index)%1000 != 0 and len(read_bosskiller().index)%100 == 0 and not boss.killed():
                    boss.hp+=20

            #傷害訊息印出
            if boss.bosstype=="小偷":
                if atk!=0:
                    weapontextout=f'你{mvtype}，造成了{atk}點傷害。\n'
                elif pineapple>1:
                    weapontextout=f'你{mvtype}，但是距離太遠了沒打中。\n'
                else:
                    weapontextout=f'你{mvtype}，但被小偷躲開了。\n'
            else:
                if atk==0:
                    weapontextout=f'{mvmain1}\n{mvmain2}\n'
                elif mvmain2 == "a":
                    weapontextout=f'{mvmain1}\n'
                else:
                    weapontextout=f'{mvmain1}{abs(atk)}{mvmain2}\n'
            textout=weapontextout

            #巨尾狛克
            if boss.bosstype=="巨尾狛克" and atk>150:
                punishment=random.randint(1,5)
                in_colddown(id,punishment)
                textout+=f"**反擊！**狛克用尾巴將你拍飛，你多了額外{punishment}秒無法行動！\n"

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
                    else:   #未滿足再動條件
                        E_atk=0
                    E_allatk+=0 if mvup==10000 else E_atk

            #鞭屍判定
            if boss.killed():
                boss.overkilling=True

            #傷害小結算
            boss.hp-=(atk+E_allatk)
            totaldmg+=(atk+E_allatk)
                
            #詞綴
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
            
            #B卷軸效果結束時銷毀
            if b_args:
                if inf(b_args[0])["can_combo"]== "N" or (inf(b_args[0])["can_combo"]== "Y" and abs(totaldmg)>inf(b_args[0])["limit"]):
                    b_args,b_type=[],""

            #單次行動結束
            can_use_combo-=1

        #吟遊狛克的7%無效============================================================================
        if boss.bosstype=="吟遊狛克" and random.randint(1,100)<8 and atk+E_allatk>0:
            alloutmes+=f"**發動！**狛克身形一閃，無效化了總計{atk+E_allatk}點傷害！\n"
            boss.hp+=(atk+E_allatk)
            totaldmg,atk,E_allatk=0,0,0

        #寫入傷害表
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
            if boss.bosstype=="小偷":
                alloutmes+=f'小偷被銬上手銬帶走了！\n'
            else:
                alloutmes+=f'狛克被變成了薩摩耶！\n'
            if "威爾森" in boss.name:
                alloutmes=alloutmes.replace("薩摩耶","竹節蟲")

        #改名   
        if "A101" in scrolls_dict:
            alloutmes=alloutmes.replace("狛克","哈庫瑪瑪塌塌").replace("你","狛克").replace("哈庫瑪瑪塌塌","你")
        alloutmes=alloutmes.replace("狛克",boss.name)


        if boss.killed():
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
            alloutmes+=f'本次BOSS輸出之MVP為{str(mvp_name)}，貢獻率為{mvp_atkperc}%\n'

        if boss.killed() and "狛克" in boss.bosstype:
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
            tooth_get=int(tooth_dice/100)
        else:
            tooth_get=int(tooth_dice/95) if not boss.bosstype=="半融合狛克" else int(tooth_dice/50)
        if boss.killed():
            tooth_get+=int(random.randint(1,100)/80)
            if boss.bosstype=="半融合狛克":
                tooth_get+=int(random.randint(300,600)/80)

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
                #篩出有資格拿的人(每5%1個)
                damage_df["can_have_items"]=damage_df["dmg"]/damage_df["dmg"].sum()*20
                damage_df.loc[:,"can_have_items"]=damage_df["can_have_items"].astype("int64")
                canhave_df=damage_df[damage_df["can_have_items"]>0]
                hv_resultdict={}
                #卡進字典裡(攻擊者的會在攻擊者自己的裡面)
                for n in range(canhave_df.shape[0]):
                    award_str=''
                    getter=int(canhave_df.iloc[n]["playerID"])
                    for _ in range(canhave_df.iloc[n]["can_have_items"]):
                        resitem,resnum=gatcha(getter,(70 if n==0 else 50))
                        award_str+=f"{resnum}個{resitem}\n"
                    if getter == id:
                        fiel1+=award_str
                    else:
                        hv_resultdict[getter]=award_str
            else:
                #攻擊者計算
                for _ in range(tooth_get):
                    resitem,resnum=gatcha(id,50)
                    fiel1+=f"{resnum}個{resitem}\n"
        elif boss.bosstype=="小偷":
            if boss.killed():
                tooth_get+=2
                damage_df=read_damagerec()
                damage_df.sort_values(["dmg"],ascending=False,inplace=True)
                #篩出有資格拿的人(每20%1個)
                damage_df["can_have_items"]=damage_df["dmg"]/damage_df["dmg"].sum()*5
                damage_df.loc[:,"can_have_items"]=damage_df["can_have_items"].astype("int64")
                canhave_df=damage_df[damage_df["can_have_items"]>0]
                hv_resultdict={}
                #卡進字典裡(攻擊者的會在攻擊者自己的裡面)
                for n in range(canhave_df.shape[0]):
                    award_str=''
                    getter=int(canhave_df.iloc[n]["playerID"])
                    for _ in range(canhave_df.iloc[n]["can_have_items"]):
                        resitem,resnum=gatcha(getter,95)
                        award_str+=f"{resnum}個{resitem}\n"
                    #MVP專屬獎勵
                    if n==0:
                        giveitem(getter,"卷軸手稿")
                        award_str+=f"1個卷軸手稿\n"
                    if getter == id:
                        fiel1+=award_str
                    else:
                        hv_resultdict[getter]=award_str
            else:
                #攻擊者計算
                for _ in range(tooth_get):
                    resitem,resnum=gatcha(id,75)
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
                    fiel1+=f"{tooth_get}撮雪狼毛\n"

            #mvp計算
            if boss.killed():
                mvp_dice=random.randint(1,100+round(mvp_atkperc*0.2))
                mvp_dice*=10 if boss.bosstype=="巨尾狛克" else 1     #巨尾狛克
                mvp_tooth=int((mvp_dice+10)/100) if mvp!=id else int((mvp_dice)/100)
                mvp_tooth=6 if mvp_tooth>6 else mvp_tooth
                #給牙囉
                if mvp_tooth:
                    givetooth(mvp,mvp_tooth)
                    fiel2+=f"{mvp_tooth}顆雪狼牙\n"            

        #反打的行動
        alloutmes=alloutmes.replace("owowowo",str(random.randint(1,100)))

        #半融合狛克
        if boss.bosstype=="半融合狛克" and not boss.killed():
            if twinlimittimes == 1:
                twinlimittimes=0
                boss.bosstype="狛克"
                boss.name.replace("半融合","")
                boss.hp*=2
                alloutmes+=f'半融合狛克完全融合完成！血量變為{boss.hp}點！\n'
            else:
                twinlimittimes-=1
                if twinlimittimes == 1:
                    alloutmes+=f'半融合狛克離完全融合只差最後一步！\n'
                if twinlimittimes == 3:
                    alloutmes+=f'半融合狛克的融合程序快結束了！\n'
                if twinlimittimes == 5:
                    alloutmes+=f'半融合狛克逐步融合！\n'

        if boss.bosstype=="小偷" and not boss.killed():
            if boss.distancing>30 and random.randint(1,100)<=70:
                alloutmes+=f'小偷遁入不起眼的小巷裡！你們跟丟了！\n'
            else:
                theifaction=[["小偷撒下了一堆釘子，為了躲避釘子而降慢速度的你們被拉開了kmgkmgkmg公尺。",2,5],
                            ["小偷奮力疾跑，與你們拉開了kmgkmgkmg公尺。",1,3],
                            ["小偷往你們腳下施放黏糊糊魔法，速度被拖慢的你們被拉開了kmgkmgkmg公尺。",1,4],
                            ["小偷拐進了巷子裡面，為了尋找小偷的方向，你們被拉開了kmgkmgkmg公尺。",3,5]]
                theifdo=random.choice(theifaction)
                thfmv,thfd,thfu=theifdo[0],theifdo[1],theifdo[2]
                distancy=random.randint(thfd,thfu)
                alloutmes+=f'{thfmv.replace("kmgkmgkmg",str(distancy))}\n'
                boss.distancing+=distancy
                alloutmes+=f'你們目前與小偷的距離為{boss.distancing}公尺！\n'
        
        #決定標題
        if revived and boss.killed():
            atktype="💀秒殺！"
        elif mvup==10000:
            atktype="💀秒殺！"
        elif boss.bosstype=="小偷" and boss.killed():
            atktype="🚓逮捕！"
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
        if boss.bosstype=="天堂狛克" or boss.bosstype=="小偷" and boss.killed():
            for haver in hv_resultdict:
                haver_name=await self.bot.fetch_user(haver)
                hitembedmes.add_field(name=f"{str(haver_name)}得到了：",value=hv_resultdict[haver], inline=True)
        hitembedmes.set_footer(text=f"Tips:{random.choice(tips)}")

        if allcombos==1 and ("那個很會魔法的阿嬤" in alloutmes) and ("那個很會魔法的阿嬤" not in boss.name):
            hitembedmes.set_thumbnail(url="https://images.plurk.com/24XoKNaUPcSRz4zIZgkCgL.png")

        #訊息發送
        if "威爾森" in boss.name:
            hahahalol=discord.File("bug.gif")
        else:
            hahahalol=discord.File(random.choice(gifs["samoyed"]))

        if boss.killed() and boss.bosstype=="小偷":
            await ctx.send(embed=hitembedmes,file=discord.File("pictures\\arrest.png"))
        elif boss.killed() and toolong(alloutmes):
            await ctx.send(embed=hitembedmes,files=[outfile,hahahalol])
        elif boss.killed():
            await ctx.send(embed=hitembedmes,file=hahahalol)
        elif toolong(alloutmes):
            await ctx.send(embed=hitembedmes,file=outfile)
        else:
            await ctx.send(embed=hitembedmes)

        #次數紀念的恭喜訊息
        secmes=""    #second message
        if boss.killed() and "狛克" in boss.bosstype:
            if len(read_bosskiller().index)%10 == 1:
                secmes+=f"你是第{len(read_bosskiller().index)-1}個把狛克變成薩摩耶的玩家！"
            if read_bosskiller()["playerID"].value_counts()[id]%5 == 0:
                secmes+=f"你目前已經把狛克變成薩摩耶{read_bosskiller()['playerID'].value_counts()[id]}次了！"
        if secmes:
            secembmes=discord.Embed(title="🎉恭喜",description=secmes)
            embname(secembmes,ctx)
            await ctx.send(embed=secembmes)

        #吟遊狛克擊殺特殊獎勵
        if boss.bosstype=="吟遊狛克" and boss.killed():
            celemes=""
            damage_df=read_damagerec()
            for players in damage_df["playerID"].values:
                givedstory,chapterchanged=givestory(players)
                if givedstory==0:
                    continue
                playeruser=await self.bot.fetch_user(players)
                playername = playeruser.display_name
                chchmes= f"，並解鎖了{check_chapter(players)}" if chapterchanged else ""
                celemes+=f"{playername}得到了故事碎片{givedstory}{chchmes}！\n"
            if celemes:
                secembmes=discord.Embed(title="🪗「讓這些故事流傳下去吧。」",description=celemes)
                await ctx.send(embed=secembmes)
        
        #小偷重生
        if "小偷遁入不起眼的小巷裡！你們跟丟了！" in alloutmes:
            boss.hp=0
                

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
        #開抽
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
        #開抽
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
        item_dct=read_item()

        outmes="您的持有道具如下：\n"
        outmes+=f"雪狼牙：{item_dct[str(id)]['tooths']}顆\n"
        outmes+=f"雪狼毛：{item_dct[str(id)]['furs']}撮\n"
        outmes+=f"持有道具：\n"
        itemmes=""
        #開始讀取道具
        scroll_dct=read_scrolls(id)
        if type(scroll_dct)==str:
            itemmes="無。"
        else:
            for scrolls in scroll_dct:
                if scroll_dct[scrolls]>0:
                    itemmes+=f'[{inf(find_id(scrolls))["rarity"]*"☆"}]**{scrolls}**：{scroll_dct[scrolls]}個\n'
                    itemmes+=f'[{inf(find_id(scrolls))["description"]}]\n\n'
        
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
            
            #購買成功
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

    @commands.command()
    async def story(self,ctx,arg=""):
        storylist=read_story(ctx.author.id)
        chapternow=check_chapter(ctx.author.id)
        chaptername={'1':"📰一份舊報紙",
        '2':"📷難民聚集地的採訪影像",
        '3':"📬寄至遠方的信件",
        '4':"⚗️與魔法商人的談話紀錄",
        '5':"🎙️山中冒險者的口述",
        '6':"🛖與山頂居民的對話",
        '7':"⛩️與參加祭典者的交談",
        '8':"📘遺落在山谷中的筆記",
        '9':"📹獵人專訪的錄像節錄",
        '10':"📃被揉成團的廢紙",
        '11':"📜一封懺悔書",
        '12':"📙嶄新的筆記本",
        '13':"📱某個群組的對話紀錄",
        '14':"🐺與狼獸人的對峙"}
        if not arg:
            outmes=""
            showname = lambda num,storylist: chaptername[str(num)] if num in storylist else "????????"

            if chapternow in ('終幕', '第四節', '第三節', '第二節', '第一節'):
                outmes+="**第一節————雪色的災殃**\n"
                outmes+=f'1.{showname(1,storylist)}\n'
                outmes+=f'2.{showname(2,storylist)}\n'
                outmes+=f'3.{showname(3,storylist)}\n'
            if chapternow in ('終幕', '第四節', '第三節', '第二節'):
                outmes+="**第二節————風暴中的燈塔**\n"
                outmes+=f'4.{showname(4,storylist)}\n'
                outmes+=f'5.{showname(5,storylist)}\n'
                outmes+=f'6.{showname(6,storylist)}\n'
                outmes+=f'7.{showname(7,storylist)}\n'
            if chapternow in ('終幕', '第四節', '第三節'):
                outmes+="**第三節————白霧掩蓋的真相**\n"
                outmes+=f'8.{showname(8,storylist)}\n'
                outmes+=f'9.{showname(9,storylist)}\n'
                outmes+=f'10.{showname(10,storylist)}\n'
                outmes+=f'11.{showname(11,storylist)}\n'
            if chapternow in ('終幕', '第四節'):
                outmes+="**第四節————虛構之上的天堂**\n"
                outmes+=f'12.{showname(12,storylist)}\n'
                outmes+=f'13.{showname(13,storylist)}\n'
            if chapternow == '終幕':
                outmes+="**終幕————一切的解答**\n"
                outmes+=f'14.{showname(14,storylist)}\n'
            
            embedmes=discord.Embed(title="📖故事",description=outmes)
            embedmes.set_footer(text="輸入k!story (故事碎片編號) 以閱讀故事。")
            embname(embedmes,ctx)
            await ctx.send(embed=embedmes)
        elif arg not in [str(ele) for ele in range(1,15)]:
            await ctx.send(f'{ctx.author.mention}\n找不到故事。\n請輸入正確的故事碎片編號。')
        elif int(arg) not in storylist:
            await ctx.send(f'{ctx.author.mention}\n你還沒有解鎖這份故事碎片。\n故事碎片可以透過討伐吟遊狛克取得。')
        else:
            await ctx.send(f'{ctx.author.mention}\n故事已經傳送到私訊。')
            outmes=f"**故事碎片{arg}:{chaptername[str(arg)]}**\n\n"
            with open(f'../basically_what/kmr_story/'+arg+'.txt','r',encoding='utf-8') as jfile:
                storylines=jfile.read()
            await ctx.author.send(f'{outmes}{storylines}')

            #最終幕解鎖
            if arg in ("12","13") and chapternow=='終幕' and 14 not in storylist:
                it_dict=read_item()
                it_dict[str(ctx.author.id)]["story"].append(14)
                save_item(it_dict)
                await ctx.author.send(f'{ctx.author.mention}\n您已閱讀完畢所有故事碎片，解答篇故事碎片14已解鎖。')

    @commands.command()
    async def slow(self,ctx):
        global boss
        id=ctx.author.id
        if boss.bosstype!="小偷":
            error_mes=discord.Embed(title="❌行動失敗",description="只有BOSS為小偷時，才可使用此指令。")
            embname(error_mes,ctx)
            await ctx.send(embed=error_mes)
            return
        
        if boss.distancing==0:
            error_mes=discord.Embed(title="❌距離過近！",description="小偷已經在你們眼前了！")
            embname(error_mes,ctx)
            await ctx.send(embed=error_mes)
            return

        if timelimited and in_colddown(id):
            time_df=read_time()
            if time_df.loc[time_df["playerID"]==id,"uncolddown"].values[0]<3:
                unc_mes=f"本指令有5秒冷卻！您還有{in_colddown(id)}秒！"
            else:
                unc_mes=f"本指令有5秒冷卻！您還有{in_colddown(id)}...欸不是你到底有完沒完！"
            notcoldmes = await ctx.send(f'{ctx.author.mention}\n{unc_mes}')
            await asyncio.sleep(3)
            await notcoldmes.delete()
            return

        theifaction=[["你們對準小偷的頭丟了石頭過去，小偷灰頭土臉的撲倒在地！你們與小偷拉近了kmgkmgkmg公尺。",6,10],
                            ["你們對準小偷的腳丟了石頭過去，傷到腳的小偷速度暫時變慢，被拉近了kmgkmgkmg公尺。",2,7],
                            ["你們往前面的地板施放冰凍魔法，小偷腳下一滑，被拉近了kmgkmgkmg公尺。",3,6],
                            ["你們憑藉對地形的熟悉看準方向抄了近路，與小偷拉近了kmgkmgkmg公尺。",5,8]]
        theifdo=random.choice(theifaction)
        thfmv,thfd,thfu=theifdo[0],theifdo[1],theifdo[2]
        distancy=random.randint(thfd,thfu)
        truedistancing=distancy if boss.distancing>distancy else boss.distancing
        outmes=f'{thfmv.replace("kmgkmgkmg",str(truedistancing))}\n'
        boss.distancing-=truedistancing
        outmes+=f'你們目前與小偷的距離為{boss.distancing}公尺！\n'

        #紀錄傷害
        damage_df=read_damagerec()
        if ctx.author.id not in damage_df["playerID"].values:
            blanky=pd.DataFrame([[ctx.author.id,truedistancing*50]])
            csv_write(blanky,damagerec,"a")
        else:
            damage_df.loc[damage_df["playerID"]==ctx.author.id,"dmg"]+=truedistancing*50
            csv_write(damage_df,damagerec,"w")

        secembmes=discord.Embed(title="👟拖延！",description=outmes)
        embname(secembmes,ctx)
        await ctx.send(embed=secembmes)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setchannel(self,ctx,arg=""):
        if arg == "":
            await ctx.send(f'{ctx.author.mention}\n此指令為指定k!hit可使用頻道。請輸入k!setchannel (頻道全名)')
            return
        if arg not in [channel.name for channel in ctx.guild.channels]:
            await ctx.send(f'{ctx.author.mention}\n在當前伺服器中找不到{arg}這個頻道。')
            return
        try:
            for channel in ctx.guild.channels:
                if channel.name == arg:
                    break
            await ctx.send(f'{ctx.author.mention}\n請到{arg}頻道確認。')
            with open('csvfile\\allowchannel.json','r',encoding='utf-8') as jfile:
                available_channel=json.load(jfile)
            if channel.id in available_channel["allowedchannel"]:
                org_message = await channel.send(f'{ctx.author.mention}\n是否取消本頻道為k!hit可使用頻道？')
            else:
                org_message = await channel.send(f'{ctx.author.mention}\n是否使用本頻道為k!hit可使用頻道？')
            emoji_y="⭕"
            emoji_n="❌"
            await org_message.add_reaction(emoji_y)
            await org_message.add_reaction(emoji_n)
            try:
                def checkv(reaction,user):
                    return user == ctx.author and str(reaction.emoji) in (emoji_y,emoji_n)
                reaction,user=await self.bot.wait_for("reaction_add", timeout=20, check=checkv)
                if str(reaction.emoji) ==emoji_n:
                    await org_message.delete()
                if str(reaction.emoji) ==emoji_y:
                    await org_message.delete()

                    if channel.id not in available_channel["allowedchannel"]:
                        available_channel["allowedchannel"].append(channel.id)
                        await channel.send(f'{ctx.author.mention}\n本頻道已設定為k!hit可使用頻道。')
                    else:
                        available_channel["allowedchannel"].remove(channel.id)
                        await channel.send(f'{ctx.author.mention}\n本頻道已設定為k!hit不可使用頻道。')
                    
                    with open('csvfile\\allowchannel.json','w',encoding='utf-8') as jfile:
                        json.dump(available_channel,jfile,ensure_ascii=False,indent=4)
            except asyncio.TimeoutError:
                await org_message.delete()
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            await ctx.send(f'{ctx.author.mention}\n向{arg}頻道發送訊息時發生錯誤。')
            pass

    @setchannel.error
    async def setchannel_error(self,error,ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("此指令為指定k!hit可使用頻道。只有擁有管理員權限的成員才能使用。")
        
async def setup(bot):
    await bot.add_cog(Rpg(bot))