import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random
import time
import asyncio

def doread(filea):
    with open(filea,'r',encoding='utf-8') as jfile:
        alines=[]
        t=jfile.readlines()
        for lines in t:
            alines.append(lines.strip('\n').strip(' ').split(','))
    return alines

def readitem(list):
    return list[2].strip('\n').strip(' ').split(';')

def dorecord(file,text):
    with open(file,'a',encoding='utf-8') as opfile:
        opfile.writelines(f'\n{text}')

def removeend(file):
    with open(file,'r',encoding='utf-8') as opfile:
        a=opfile.read()
    b=a.split("\n")
    t="\n".join(b[:-1])
    with open(file,'w+',encoding='utf-8') as opfile:
        for i in range(len(t)):
            opfile.write(t[i])

def doblank(file):
    with open(file,'w',encoding='utf-8') as opfile:
        opfile.writelines('0,0')

def givetooth(id,how_many):
    users=[]
    itemrawdata=doread(item)
    for rawdata in itemrawdata:
        users.append(int(rawdata[0]))
    if id in users:
        available_tooth=int(itemrawdata[users.index(id)][1])
        available_tooth+=how_many
        itemrawdata[users.index(id)][1]=available_tooth
        with open(item,'w',encoding='utf-8') as opfile:
            for a in itemrawdata:
                opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
        removeend(item)
    else:
        dorecord(item,f'{id},{how_many},0%0')

def removetooth(id,how_many):
    users=[]
    itemrawdata=doread(item)
    nohave=False
    for rawdata in itemrawdata:
        users.append(int(rawdata[0]))
    if id in users:
        available_tooth=int(itemrawdata[users.index(id)][1])
        if available_tooth < how_many:
            nohave=True
        else:
            available_tooth-=how_many
            itemrawdata[users.index(id)][1]=available_tooth
            with open(item,'w',encoding='utf-8') as opfile:
                for a in itemrawdata:
                    opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
            removeend(item)
            return True
    else:
        nohave=True
    if nohave:
        return "您似乎雪狼牙的數量不足呢-w-..."

def givefur(id,how_many):
    users=[]
    itemrawdata=doread(furfile)
    for rawdata in itemrawdata:
        users.append(int(rawdata[0]))
    if id in users:
        available_tooth=int(itemrawdata[users.index(id)][1])
        available_tooth+=how_many
        itemrawdata[users.index(id)][1]=available_tooth
        with open(furfile,'w',encoding='utf-8') as opfile:
            for a in itemrawdata:
                opfile.writelines(f'{a[0]},{a[1]}\n')
        removeend(furfile)
    else:
        dorecord(furfile,f'{id},{how_many}')

def removefur(id,how_many):
    users=[]
    nohave=False
    itemrawdata=doread(furfile)
    for rawdata in itemrawdata:
        users.append(int(rawdata[0]))
    if id in users:
        available_tooth=int(itemrawdata[users.index(id)][1])
        if available_tooth < how_many:
            nohave=True
        else:
            available_tooth-=how_many
            itemrawdata[users.index(id)][1]=available_tooth
            with open(furfile,'w',encoding='utf-8') as opfile:
                for a in itemrawdata:
                    opfile.writelines(f'{a[0]},{a[1]}\n')
            removeend(furfile)
            return True
    else:
        nohave=True
    if nohave:
        return "您似乎雪狼毛的數量不足呢-w-..."

def find_item_id(item):             #得到的是str
    return item_id_file[item]

def find_item_value(id):            #得到的是串列
    diction=doread("csvfile\\itemdata.csv")
    for line in diction:
        if id == line[1]:
            return line

def giveitem(reciever,arg1,arg2='1'): #receiver是int,arg1是物品名稱
    if arg1 == "":
        return '您似乎沒有說明要使用什麼呢-w-...'

    if arg1 not in item_id_file:
        return '這個東西似乎名稱不對呢-w-...\n請確定您輸入的是不含稀有度的道具全名-w-...'

    users=[]
    itemrawdata=doread(item)
    for rawdata in itemrawdata:
        users.append(int(rawdata[0]))
    if reciever in users:
        raw_available_item=readitem(itemrawdata[users.index(reciever)])
        item_have=[]
        item_count=[]
        for raw in raw_available_item:
            raw=raw.split('%')
            item_have.append(raw[0])
            item_count.append(int(raw[1]))
        if arg1 in item_have :
            have_count=item_count[item_have.index(arg1)]
            if str(arg2).isdigit():
                nankai=int(arg2)
                #加上去
                item_count[item_have.index(arg1)]+=nankai
                #資料復位
                backto=""
                for a in range(0,len(item_count)):
                    backto+=f"{item_have[a]}%{item_count[a]}"
                    if a!=len(item_count)-1:
                        backto+=";"
                itemrawdata[users.index(reciever)][2]=f"{backto}"
                with open(item,'w',encoding='utf-8') as opfile:
                    for a in itemrawdata:
                        opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
                removeend(item)
                return True
            else:
                return '數量請輸入數字啦-w-...'
        else:
            itemrawdata[users.index(reciever)][2]+=f";{arg1}%{arg2}"
            with open(item,'w',encoding='utf-8') as opfile:
                for a in itemrawdata:
                    opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
            removeend(item)
            return True
    else:
        dorecord(item,f"{reciever},0,0%0;{arg1}%{arg2}")
        return True

def removeitem(reciever,arg1,arg2='1'): #receiver是int,arg1是物品名稱 #成功時回報true反之字串 #arg2可以是str
    no_have=False
    if arg1 == "":
        return '您似乎沒有說明要使用什麼呢-w-...'
    if arg1 not in item_id_file:
        return '這個東西似乎名稱不對呢-w-...\n請確定您輸入的是不含稀有度的道具全名-w-...'
    redeem_item=item_id_file[arg1]
    users=[]
    itemrawdata=doread(item)
    for rawdata in itemrawdata:
        users.append(int(rawdata[0]))
    if reciever not in users:
        return '您似乎這個道具的數量不足呢-w-...'
    raw_available_item=readitem(itemrawdata[users.index(reciever)])
    item_have=[]
    item_count=[]
    for raw in raw_available_item:
        raw=raw.split('%')
        item_have.append(raw[0])
        item_count.append(int(raw[1]))
    if arg1 not in item_have :
        return '您似乎這個道具的數量不足呢-w-...'
    have_count=item_count[item_have.index(arg1)]
    if not str(arg2).isdigit():
        return '數量請輸入數字啦-w-...'
    nankai=int(arg2)
    if have_count < nankai:
        return '您似乎這個道具的數量不足呢-w-...'
    #減下去
    item_count[item_have.index(arg1)]-=nankai
    #資料復位
    backto=""
    for a in range(0,len(item_count)):
        backto+=f"{item_have[a]}%{item_count[a]}"
        if a!=len(item_count)-1:
            backto+=";"
    itemrawdata[users.index(reciever)][2]=f"{backto}"
    with open(item,'w',encoding='utf-8') as opfile:
        for a in itemrawdata:
            opfile.writelines(f'{a[0]},{a[1]},{a[2]}\n')
    removeend(item)
    return True

def O_redeem(redeem_item_ID):
    if redeem_item_ID == "O1":
        a=random.randint(1,100)
        if 0<a<=60:
            b=random.choice(["D1","D2"])
        elif 60<a<=95:
            b=random.choice(["D3","D4"])
        elif 95<a<=100:
            b="D5"
        return b
    elif redeem_item_ID == "O2":
        a=random.randint(1,50)
        a+=50
        if 0<a<=60:
            b=random.choice(["D1","D2"])
        elif 60<a<=95:
            b=random.choice(["D3","D4"])
        elif 95<a<=100:
            b="D5"
        return b
    elif redeem_item_ID == "O2":
        b="D5"
        return b

def ifused(item,itemused):
    if item in itemused:
        return True
    else:
        return False

def conflict(weapontype,bkind,itemused):
    if weapontype=='a' and bkind=='b':
        return True
    if weapontype=='b' and bkind=='a':
        return True
    if weapontype=='b' and ifused("D1",itemused):
        return True
    if weapontype=='b' and ifused("D4",itemused):
        return True
    return False

def createtxt(mes):
    k=round(time.time()*100)
    with open(f'temporary\{k}.txt','a',encoding='utf-8') as txtfile:
        txtfile.writelines(mes)
    return f'temporary\{k}.txt'

def gat(userys,up=0):
    setsumei=doread("csvfile\\itemdata.csv")
    onestar=[ele for ele in setsumei if ele[2]=="[☆]" and not ele[1].startswith("D")]
    twostar=[ele for ele in setsumei if ele[2]=="[☆☆]" and not ele[1].startswith("D")]
    threestar=[ele for ele in setsumei if ele[2]=="[☆☆☆]" and not ele[1].startswith("D")]
    dice=up+random.randint(1,100-up)
    gatcharesult=[]
    if 0<dice<=75:
        gatcharesult=random.choice(onestar)
    elif 75<dice<=95:
        gatcharesult=random.choice(twostar)
    elif 95<dice<=100:
        gatcharesult=random.choice(threestar)
    if not gatcharesult[4].isdecimal():
        des=gatcharesult[4].split("t")
        thenum=random.randint(int(des[0]),int(des[1]))
    else:
        thenum=gatcharesult[4]
    giveitem(userys,gatcharesult[0],thenum)
    return f"您獲得了{thenum}個{gatcharesult[2]}**{gatcharesult[0]}**！\n{gatcharesult[3]}\n"

def timeok(id):
    timelist=doread(timenote)
    timeppl=[]
    timelast=[]
    for a in timelist:
        timeppl.append(int(a[0]))
        timelast.append(float(a[1]))
    if id in timeppl:
        v=timeppl.index(id)
        if time.time()-timelast[v]<10:
            a=10-round(time.time()-timelast[v])
            if a==0:
                a=1
            return a
        else:
            timelast[v]=time.time()
            doblank(timenote)
            for b in range(1,len(timeppl)):
                dorecord(timenote,f"{timeppl[b]},{timelast[b]}")
            return False
    else:
        dorecord(timenote,f"{id},{time.time()}")
        return False

def boss_default():
    global namechanged
    global namechangeto
    doblank(damagerec)
    namechanged=False
    namechangeto=""

damagerec="csvfile\\damagerec.csv"
item="csvfile\\item.csv"
furfile="csvfile\\furcount.csv"
timenote="csvfile\\timelimit.csv"

with open('csvfile\channel.json','r',encoding='utf-8') as jfile:
    gifs=json.load(jfile)
with open('csvfile\itemfile.json','r',encoding='utf-8') as jfile:
    item_id_file=json.load(jfile)
with open('csvfile\\furryshop.json','r',encoding='utf-8') as jfile:
    furryshop=json.load(jfile)

rpglist=doread('csvfile\\rpgweapon.csv')

available_channel=(935768359931371540,935471683911954512,641131990959259667,938827700968231022)

boss_hp=0
namechanged=False
namechangeto=""
heavenly=False
timelimited=True


class Rpg(Cog_Extension):
####################################################################################################################################
    @commands.command()
    async def hit(self,ctx,*args):
        #if ctx.channel.id  not in available_channel:
            #await ctx.send(f'本頻道不可使用此指令，或者沒有登錄此頻道。')
            #return

        timeado=timeok(ctx.author.id)
        if timelimited and timeado:
            notcoldmes = await ctx.send(f'{ctx.author.mention}\n本指令有10秒冷卻！您還有{timeado}秒！')
            await asyncio.sleep(3)
            await notcoldmes.delete()
            return

        #變數預設值
        global boss_hp
        global namechanged
        global namechangeto
        global heavenly
        textout=""
        killed=False
        critical=0
        combo=0
        intkiller=[]
        hpwas=0
        overkill=False
        itemused=[]
        useitem=False
        counted=False
        lance=0 #追擊
        atk=0
        bkind=""
        blimit=0
        bcombo=""
        bdone=True
        totaldamage=0
        weaponchanged=False
        maxda=[0]
        weaponwhat=""
        roll_dice=0
        revived=False

        history=doread("csvfile\\killed.csv")
        for a in history:
            intkiller.append(int(a[0]))

        #讀取使用的道具
        for el in args:
            if el in item_id_file:
                if find_item_id(el).startswith("O"):
                    textout+=f"使用{find_item_value(find_item_id(el))[2]}{el}時發生錯誤！\n本道具為兌換用道具，請以以下格式輸入：k!redeem {el}\n\n"
                    continue
                if el == "神之筆":
                    if args.index(el)+1 == len(args):
                        textout+=f"使用{find_item_value(find_item_id(el))[2]}{el}時發生錯誤！\n請以以下格式輸入：k!hit 神之筆 (想要改變的暱稱)\n\n"
                        continue
                    else:
                        if args[args.index(el)+1].startswith("(") and args[args.index(el)+1].endswith(")"):
                            god_name=args[args.index(el)+1].strip("(").strip(")")
                        else:
                            textout+=f"使用{find_item_value(find_item_id(el))[2]}{el}時發生錯誤！\n下一項並不是指定改名的名稱！請以以下格式輸入：k!hit 神之筆 (想要改變的暱稱)\n\n"
                            continue
                confirm=removeitem(ctx.author.id,el)
                if confirm == True:
                    textout+=f"已使用{find_item_value(find_item_id(el))[2]}**{el}**！\n"
                    itemused.append(find_item_id(el))
                    useitem=True
                else:
                    textout+=f"使用{find_item_value(find_item_id(el))[2]}**{el}**時發生錯誤！\n{confirm}\n\n"

        #B類道具讀取區
        canskipitem=[]
        for item in itemused:
            if item.startswith("B"):
                itemdatB=find_item_value(item)
                if bkind!="":
                    if item not in canskipitem:
                        textout+=f"使用{itemdatB[2]}**{itemdatB[0]}**時發生錯誤！\n你不能同時使用兩種傷害保障型卷軸！\n"
                        textout+=f"已返還{itemused.count(item)}個{itemdatB[2]}**{itemdatB[0]}**！\n\n"
                        giveitem(ctx.author.id,itemdatB[0],itemused.count(item))
                        itemused=[elem for elem in itemused if elem != item]
                        canskipitem.append(item)
                    continue
                else:
                    bkind,blimit,bcombo,bdone=itemdatB[5],int(itemdatB[6]),itemdatB[7],False

        #必定治療與必定攻擊衝突處理
        if bkind=="b" and (ifused("D1",itemused) or ifused("D4",itemused)):
            if "D1" in itemused and not "D1" in canskipitem:
                textout+=f"使用[☆]**鎖定**時發生錯誤！\n不能同時使用必定回復效果卷軸與必定攻擊效果卷軸！\n\n"
                textout+=f"已返還{itemused.count('D1')}個[☆]**鎖定**！\n\n"
                giveitem(ctx.author.id,"鎖定",itemused.count('D1'))
                itemused=[elem for elem in itemused if elem != "D1"]
                canskipitem.append("D1")
            if "D4" in itemused and not "D4" in canskipitem:
                textout+=f"使用[☆☆]**水平四方斬**時發生錯誤！\n不能同時使用必定回復效果卷軸與必定攻擊效果卷軸！\n"
                textout+=f"已返還{itemused.count('D4')}個[☆☆]**水平四方斬**！\n\n"
                giveitem(ctx.author.id,"水平四方斬",itemused.count('D4'))
                itemused=[elem for elem in itemused if elem != "D4"]
                canskipitem.append("D4")

        #C區道具讀取區
        for item in itemused:
            if item.startswith("C"):
                itemdatC=find_item_value(item)
                if weaponchanged:
                    if item not in canskipitem:
                        textout+=f"使用{itemdatC[2]}**{itemdatC[0]}**時發生錯誤！\n不能同時使用兩種武器變化型卷軸！\n"
                        thatcount=itemused.count(item)
                        if item==weaponwhat:
                            thatcount-=1
                        textout+=f"已返還{thatcount}個{itemdatC[2]}**{itemdatC[0]}**！\n\n"
                        giveitem(ctx.author.id,itemdatC[0],thatcount)
                        itemused=[elem for elem in itemused if elem != item]
                        canskipitem.append(item)
                    continue
                else:
                    weapontype=itemdatC[5]
                    if conflict(weapontype,bkind,itemused):
                        textout+=f"使用{itemdatC[2]}**{itemdatC[0]}**時發生錯誤！\n不能同時使用必定回復效果卷軸與必定攻擊效果卷軸！\n"
                        textout+=f"已返還{itemused.count(item)}個{itemdatC[2]}**{itemdatC[0]}**！\n\n"
                        giveitem(ctx.author.id,itemdatC[0],itemused.count(item))
                        itemused=[elem for elem in itemused if elem != item]
                        canskipitem.append(item)
                        continue
                    else:
                        weaponchanged=True
                        weaponnum=int((len(itemdatC)-5)/4)
                        weapons=[]
                        weaponwhat=item
                        for a in range(0,weaponnum):
                            weapons.append([itemdatC[6+(a*4)],itemdatC[7+(a*4)],itemdatC[8+(a*4)],itemdatC[9+(a*4)]])
                            maxda.append(int(itemdatC[9+(a*4)]))
                if ifused("D3",itemused):
                    if "D3" not in canskipitem:
                        textout+=f"使用[☆☆]**抽牌**時發生錯誤！\n不能同時使用抽牌跟必定攻擊的武器變化型卷軸！\n"
                        textout+=f"已返還{itemused.count('D3')}個[☆☆]**抽牌**！\n\n"
                        giveitem(ctx.author.id,"抽牌",itemused.count('D3'))
                        itemused=[elem for elem in itemused if elem != 'D3']
                        canskipitem.append('D3')
                    continue

        if blimit !=0 and maxda!=[0] and max(maxda)<blimit and bcombo=="N":
            theonlyb=[ele for ele in itemused if ele.startswith("B")]
            thatonlyb=find_item_value(theonlyb[0])
            textout+=f"使用{thatonlyb[2]}**{thatonlyb[0]}**時發生錯誤！\n武器變化型卷軸的傷害上限小於傷害保障型卷軸的傷害上限！\n"
            textout+=f"已返還{itemused.count(theonlyb[0])}個{thatonlyb[2]}**{thatonlyb[0]}**！\n\n"
            giveitem(ctx.author.id,thatonlyb[0],itemused.count(theonlyb[0]))
            itemused=[elem for elem in itemused if elem != theonlyb[0]]
            canskipitem.append(theonlyb[0])
            bkind=""
            blimit=0
            bcombo=""

        #天堂狛克召喚
        if ifused("X1",itemused):
            await ctx.send(f"{ctx.author.mention}\n你餵食了狛克天國草，狛克產生了劇烈的變化！\n*「說吧，讓我聆聽你的願望。」*\n天堂狛克降臨！\n特殊技能：血量超級厚，掉落道具。")
            heavenly=True
            boss_hp = random.randint(3000,5000)
            revived=True
            boss_default()

        #BOSS空血時完全重置
        if boss_hp == 0:
            boss_hp = random.randint(500,1000)
            boss_default()
            heavenly=False
            revived=True
            if len(intkiller)%1000 ==0:
                textout+="狛克從湖底甦醒了！\n"
                textout+="特殊技能：被回血時回復5倍。\n"
            if len(intkiller)%1000 !=0 and len(intkiller)%100 ==0:
                textout+="狛克從山上躍下！\n"
                textout+="特殊技能：每次被攻擊固定回復20點血量。\n"

        #重生
        if ifused("J1",itemused):
            boss_hp=(random.randint(3000,5000) if heavenly else random.randint(500,1000))

        #分離
        for item in itemused:
            if item=="J2":
                boss_hp=round(boss_hp/2)
                if boss_hp<1:
                    boss_hp=1
        
        #紀錄原本的血量
        hpwas=boss_hp

        #同生共死
        if ifused("J3",itemused):
            boss_hp = random.randint(200,300)
            textout+="你不顧一切的拖著狛克一起跳下懸崖！\n"
        
        #A2,A3讀取區
        if ifused("A2",itemused):
            namechanged=True
            namechangeto="威爾森"
        if ifused("A3",itemused):
            namechanged=True
            namechangeto=f"{god_name}"

        #傷害判定=============================================================================
        while critical <= 5 and not ifused("J3",itemused):
            #百年特效
            if len(intkiller)%1000 !=0 and len(intkiller)%100 ==0:
                boss_hp+=20
            #隨機武器
            WeaponResult=random.choice(weapons) if weaponchanged else random.choice(rpglist)
            main1,main2,down,up=WeaponResult[0],WeaponResult[1],int(WeaponResult[2]),int(WeaponResult[3])
            
            if boss_hp<=0:
                overkill=True

            #隨機傷害
            if up == 0:
                atk=0
            else:
                atk = random.randint(down,up)
            
            #傷害制限
            if ifused("D1",itemused):
                if atk<75:
                    continue
            if ifused("D4",itemused):
                if atk<0:
                    continue
            if not bdone:
                if bkind=="a" and bcombo=="Y":
                    if atk<0:
                        continue
                if bkind=="a" and bcombo=="N":
                    if atk<blimit:
                        continue
                    bdone=True
                if bkind=="b" and bcombo=="Y":
                    if atk>=0:
                        continue
                if bkind=="b" and bcombo=="N":
                    if -(atk)<blimit:
                        continue
                    bdone=True

            #F讀取
            for item in itemused:
                if item.startswith("F"):
                    itemdatF=find_item_value(item)
                    changenum=float(itemdatF[7])
                    if itemdatF[5]=="a" and atk>0:
                        if itemdatF[6]=="a":
                            atk+=int(changenum)
                        elif itemdatF[6]=="m":
                            atk*=int(changenum)
                    elif itemdatF[5]=="n":
                        if itemdatF[6]=="a":
                            if atk<0:
                                atk-=int(changenum)
                            elif atk>0:
                                atk+=int(changenum)
                        elif itemdatF[6]=="m":
                            atk=round(atk*changenum)

            #紀錄已造成的傷害(在此之下沒有continue)
            totaldamage+=atk

            #輸出格式
            if atk==0:                                      #無傷害
                weaponoutmes=f'{main1}\n{main2}\n'
            elif atk<0:                                       #補血
                if len(intkiller)%1000 ==0:
                    atk*=5
                weaponoutmes=f'{main1}{-(atk)}{main2}\n'
                boss_hp-=atk
            elif main2 == "a":                                #不顯示傷害的武器
                weaponoutmes=f'{main1}\n'
                boss_hp-=atk
            else:
                weaponoutmes=f'{main1}{atk}{main2}\n'             #所有其他武器
                boss_hp-=atk
            textout+=weaponoutmes

            originatk=atk

            #E區道具讀取
            for item in itemused:
                if item.startswith("E"):
                    if item not in canskipitem:
                        itemdatE=find_item_value(item)
                        if itemdatE[5].isdecimal():
                            repeated=int(itemdatE[5])
                        else:
                            wat=itemdatE[5].split("n")
                            repeated=random.randint(int(wat[0]),int(wat[1]))
                        combo+=repeated
                        if item == "E6":
                            textout+=f"影子模仿了你的行動！{weaponoutmes.replace('你','影子').replace(str(atk),(str(up) if atk<0 else str(down)))}"
                        elif item =="E9":
                            textout+=f"影子模仿了你的行動！{weaponoutmes.replace('你','影子').replace(str(atk),(str(up) if atk>=0 else str(down)))}"
                        else:
                            while repeated>0:
                                eatk=random.randint(int(itemdatE[8]),int(itemdatE[9]))

                                #F區
                                for itemF in itemused:
                                    if itemF.startswith("F"):
                                        itemdatF=find_item_value(itemF)
                                        changenum=float(itemdatF[7])
                                        if itemdatF[6]=="a":
                                            if itemdatF[5]=="a" and eatk>0:
                                                eatk+=int(changenum)
                                            elif itemdatF[5]=="n" and eatk!=0:
                                                eatk+=(int(changenum) if eatk>0 else -int(changenum))

                                readyy=f"{itemdatE[6]}{abs(eatk)}{itemdatE[7]}\n"
                                if item=="E1":
                                    if atk>0 and ("真實" not in weaponoutmes):
                                        atk+=eatk
                                        textout+=readyy
                                elif item=="E2":
                                    if atk<0:
                                        atk+=eatk
                                        textout+=readyy
                                elif item=="E3":
                                    if atk>0 and "真實" in weaponoutmes:
                                        atk+=eatk
                                        textout+=readyy
                                else:
                                    atk+=eatk
                                    textout+=readyy
                                repeated-=1

            #紀錄輸出
            damagelist=doread(damagerec)
            damagename=[]
            damagenumber=[]
            for a in damagelist:
                damagename.append(int(a[0]))
                damagenumber.append(int(a[1]))
            if ctx.author.id in damagename:
                v=damagename.index(ctx.author.id)
                damagenumber[v]+=atk
                doblank(damagerec)
                for b in range(1,len(damagename)):
                    dorecord(damagerec,f"{damagename[b]},{damagenumber[b]}")
            else:
                dorecord(damagerec,f"{ctx.author.id},{atk}")

            #爆擊判定
            critical=random.randint(1,100)

            if not counted:
                for item in itemused:
                    if item.startswith("D"):
                        itemdat=find_item_value(item)
                        lance+=int(itemdat[5])
                        counted=True
                    if item == "C19":
                        lance+=random.randint(8,12)
                        counted=True

            #連擊次數消耗
            if lance >0 :
                lance-=1
                critical=0
            #無限連擊類檢定
            if ifused("D3",itemused):
                if originatk >0:
                    critical=0

            if bcombo=="Y":
                if bkind=="a":
                    if totaldamage<blimit:
                        critical=0
                    else:
                        bdone=True
                else:
                    if -(totaldamage)<blimit:
                        critical=0
                    else:
                        bdone=True

            if critical <= 5 :
                combo+=1
                if overkill:
                    textout+="鞭屍！"
                else:
                    if combo%3==1:
                        textout+="緊接著"
                    elif combo%3==2:
                        textout+="然後"
                    else:
                        textout+="再來"
            

        #剩餘血量&訊息印出===============================================================================
        if boss_hp > 0:
            status_=""
            #血量上限
            if not heavenly and boss_hp>1500:
                boss_hp=1500
            if heavenly:
                if hpwas >= 2500 and boss_hp < 2500:
                    status_=f'狛克略顯疲態！\n'
                if hpwas >= 1000 and boss_hp < 1000:
                    status_=f'狛克面色蒼白！\n'
                if hpwas >= 300 and boss_hp < 300:
                    status_=f'狛克跪倒在地！\n'
                if hpwas <= 300 and boss_hp > 300:
                    status_=f'狛克他重新站起來了！\n'
            else:
                if hpwas >= 300 and boss_hp < 300:
                    status_=f'狛克看起來非常的虛弱！\n'
                if hpwas >= 100 and boss_hp < 100:
                    status_=f'狛克看起來已經沒有力氣掙扎了！\n'
                if hpwas <= 100 and boss_hp > 100:
                    status_=f'狛克他重新站起來了！\n'
                if hpwas <= 1000 and boss_hp > 1000:
                    status_=f'狛克感到了前所未有的亢奮！\n'
                if hpwas < 1500 and boss_hp == 1500:
                    status_=f'狛克全身散發著光芒！\n'
            textout+=f'狛克還有{boss_hp}點血量！{status_}\n'
        else:
            killed=True
            textout+=f'尾刀！狛克被變成了薩摩耶！\n'
            if revived==True:
                textout=textout.replace("尾刀","秒殺")
            damagelist2=doread(damagerec)
            damagename2=[]
            damagenumber2=[]
            for a in damagelist2:
                damagename2.append(int(a[0]))
                damagenumber2.append(int(a[1]))
            mvp=damagename2[damagenumber2.index(max(damagenumber2))]
            tr=damagename2.index(mvp)
            fulldamage=0
            for b in range(1,len(damagename2)):
                fulldamage+=damagenumber2[b]
            partofhp=round(damagenumber2[tr]/fulldamage*100,1)
            textout+=f'本次BOSS輸出之MVP為<@{mvp}>，輸出率為{partofhp}%\n'

        #改名
        if ifused("A1",itemused):
            textout=textout.replace("狛克","哈庫瑪瑪塌塌").replace("你","狛克").replace("哈庫瑪瑪塌塌","你")
        if namechanged:
            textout=textout.replace("狛克",f"{namechangeto}")
        if len(intkiller)%1000 ==0:
            textout=textout.replace("狛克","千年狛克")
        if len(intkiller)%1000 !=0 and len(intkiller)%100 ==0:
            textout=textout.replace("狛克","百年狛克")
        if heavenly:
            textout=textout.replace("狛克","天堂狛克")
            
        #傳送訊息
        if killed:
            if namechangeto =="威爾森":
                hahahalol=discord.File("bug.gif")
                textout=textout.replace("薩摩耶","竹節蟲")
            else:
                hahahalol=discord.File(random.choice(gifs["samoyed"]))
            if len(textout)<1900:
                await ctx.send(f'{ctx.author.mention}\n{textout}',file=hahahalol)
            else:
                outfile=discord.File(createtxt(textout))
                await ctx.send(f'{ctx.author.mention}\n',file=outfile)
        else:
            if len(textout)<1900:
                await ctx.send(f'{ctx.author.mention}\n{textout}')
            else:
                outfile=discord.File(createtxt(textout))
                await ctx.send(f'{ctx.author.mention}\n',file=outfile)

        secmes=""
        if killed:
            intkiller=[]
            dorecord("csvfile\\killed.csv",ctx.author.id)
            history=doread("csvfile\\killed.csv")
            for a in history:
                intkiller.append(int(a[0]))
            userkills=intkiller.count(ctx.author.id)
            if userkills %5 == 0 and userkills != 0:
                secmes+=f'{ctx.author.mention}\n恭喜！您已經把狛克變成薩摩耶{userkills}次！\n'
            if len(intkiller) %10 == 1:
                secmes+=f'{ctx.author.mention}\n恭喜！您是第{len(intkiller)-1}個把狛克變成薩摩耶的玩家！\n'
                if len(intkiller) %1000 == 1:
                    giveitem(ctx.author.id,"銀令牌")
                    secmes+=f'你獲得了**銀令牌**！\n'
                    giveitem(mvp,"鐵令牌")
                    secmes+=f'<@{mvp}>，你獲得了**鐵令牌**！\n'
                elif len(intkiller) %100 == 1:
                    giveitem(ctx.author.id,"鐵令牌")
                    secmes+=f'你獲得了**鐵令牌**！\n'
                    giveitem(mvp,"木令牌")
                    secmes+=f'<@{mvp}>，你獲得了**木令牌**！\n'
                elif len(intkiller) %10 == 1:
                    giveitem(ctx.author.id,"木令牌")
                    secmes+=f'你獲得了**木令牌**！\n'
            boss_hp=0

        #掉落寶物
        id=ctx.author.id
        roll_dice+=random.randint(1,100)
        while combo != 0:
            roll_dice+=random.randint(1,20)
            combo-=1
        they_get_it,they_get_fur,how_many,mvp_get_it=False,False,0,False

        if killed:
            if heavenly:
                for userys in damagename2:
                    partofdam=round(damagenumber2[damagename2.index(userys)]/fulldamage*100/5)
                    if partofdam!=0:
                        secmes+=f'<@{userys}>\n'
                    while partofdam != 0:
                        partofdam-=1
                        secmes+=f'{gat(userys)}\n'    #gat自帶給禮物功能
                    mvp_get_it=True
            else:
                if int(roll_dice/80)>0:
                    they_get_it=True
                    how_many=int(roll_dice/80)
                    mvp_dice=random.randint(1,100)
                    if mvp_dice>90:
                        mvp_get_it=True
        else:
            if totaldamage >=0:
                if int(roll_dice/98)>0 :
                    they_get_it=True
                    how_many=int(roll_dice/97)
            else:
                if int(roll_dice/97)>0 :
                    they_get_fur=True
                    how_many=int(roll_dice/97)

        if heavenly:
            if they_get_it or they_get_fur:
                secmes+=f'{ctx.author.mention}\n'
                for a in range(0,how_many):
                    secmes+=f'{gat(id,60)}\n'
            if mvp_get_it:
                secmes+=f'<@{mvp}>\n{gat(mvp,70)}\n'
        else:
            if they_get_it:
                secmes+=f'{ctx.author.mention}\n您獲得了{how_many}顆雪狼牙！\n'
                givetooth(id,how_many)
            if they_get_fur:
                secmes+=f'{ctx.author.mention}\n您獲得了{how_many}撮雪狼毛！\n'
                givefur(id,how_many)
            if mvp_get_it:
                secmes+=f'<@{mvp}>\n您獲得了1顆雪狼牙！\n'
                givetooth(mvp,1)
        if secmes !="":
            if len(secmes)<1900:
                await ctx.send(f'{secmes}')
            else:
                outfileb=discord.File(createtxt(secmes))
                await ctx.send(file=outfileb)

####################################################################################################################################
    @commands.command()
    async def bosskill(self,ctx):
        intkiller=[]
        history=doread("csvfile\\killed.csv")
        for a in history:
                    intkiller.append(int(a[0]))
        await ctx.send(f'{ctx.author.mention}\n狛克已經變成薩摩耶{len(intkiller)-1}次了！')

    @commands.command()
    async def mykill(self,ctx):
        intkiller=[]
        history=doread("csvfile\\killed.csv")
        for a in history:
                    intkiller.append(int(a[0]))
        userkills=intkiller.count(ctx.author.id)
        await ctx.send(f'{ctx.author.mention}\n您目前已經把狛克變成薩摩耶{userkills}次了！')

    @commands.command()
    async def showhp(self,ctx):
        global boss_hp
        if boss_hp == 0:
            boss_hp = random.randint(500,1000)
            boss_default()
            heavenly=False
        await ctx.send(f'{ctx.author.mention}\n你拿起偵測儀對著狛克一陣亂拍。\n偵測儀顯示狛克現在還有{boss_hp}點血量！')

    @commands.command()
    async def gatcha(self,ctx,arg='1'):
        users=[]
        outmes=""
        itemrawdata=doread(item)
        for rawdata in itemrawdata:
            users.append(int(rawdata[0]))
        id=ctx.author.id

        if id not in users:
            await ctx.send(f'{ctx.author.mention}\n您似乎一顆雪狼牙都還沒取得呢-w-...')
            return

        if not arg.isdecimal:
            await ctx.send(f'{ctx.author.mention}\n轉蛋次數請輸入整數-w-...')
            return

        if not int(arg)<=20:
            await ctx.send(f'{ctx.author.mention}\n為了以防字數爆炸，一次請不要超過20次呢-w-...')
            return

        turns=int(arg)
        ressult=removetooth(id,turns)
        if ressult!=True:
            await ctx.send(f'{ctx.author.mention}\n{ressult}')
            return
        embedmes=discord.Embed(title=f"抽取{turns}次！", description=f'你抽到了...')
        embedmes.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
        setsumei=doread("csvfile\\itemdata.csv")
        onestar=[ele for ele in setsumei if ele[2]=="[☆]" and not ele[1].startswith("D")]
        twostar=[ele for ele in setsumei if ele[2]=="[☆☆]" and not ele[1].startswith("D")]
        threestar=[ele for ele in setsumei if ele[2]=="[☆☆☆]" and not ele[1].startswith("D")]
        while turns != 0:
            turns-=1
            dice=random.randint(1,100)
            gatcharesult=[]
            if 0<dice<=75:
                gatcharesult=random.choice(onestar)
            elif 75<dice<=95:
                gatcharesult=random.choice(twostar)
            elif 95<dice<=100:
                gatcharesult=random.choice(threestar)
            if not gatcharesult[4].isdecimal():
                des=gatcharesult[4].split("t")
                thenum=random.randint(int(des[0]),int(des[1]))
            else:
                thenum=gatcharesult[4]
            giveitem(id,gatcharesult[0],thenum)
            embedmes.add_field(name=f"{thenum}個{gatcharesult[2]}{gatcharesult[0]}", value=f"{gatcharesult[3]}", inline=True)
        embedmes.set_footer(text="查看自己的所有物品請輸入k!myitem")
        await ctx.send(embed=embedmes)

    @commands.command()
    async def redeem(self,ctx,arg1="",arg2='1'):
        if arg1 == "":
            await ctx.send(f'{ctx.author.mention}\n您似乎沒有說明要兌換什麼呢-w-...')
            return
        if arg1 not in item_id_file:
            await ctx.send(f'{ctx.author.mention}\n這個東西似乎名稱不對呢-w-...\n請確定您輸入的是不含稀有度的道具全名-w-...')
            return
        redeem_item=item_id_file[arg1]
        outmes=""

        if not redeem_item.startswith("O"):
            await ctx.send(f'{ctx.author.mention}\n這個東西似乎不是可以拿來兌換的東西呢-w-...')
            return

        theresult1=removeitem(ctx.author.id,arg1,arg2)
        if theresult1 != True:
            await ctx.send(f'{ctx.author.mention}\n{theresult1}')
        else:
            nankai=int(arg2)
            outmes+=f"兌換{nankai}個**{arg1}**！\n"
            #開始抽取
            setsumei=doread("csvfile\\itemdata.csv")
            while nankai>0:
                resulting=O_redeem(redeem_item)
                for line in setsumei:
                    if resulting == line[1]:
                        outmes+=f"你拿到了{line[2]}{line[0]}！\n{line[3]}\n\n"
                        theresult2=giveitem(ctx.author.id,line[0],int(line[4]))
                        if theresult2 != True:
                            await ctx.send(f'{ctx.author.mention}\n{theresult2}')
                        else:
                            nankai-=1
            await ctx.send(f'{ctx.author.mention}\n{outmes}')

    @commands.command()
    async def gift(self,ctx,arg1="",arg2="",arg3='1'):     #arg1是物品 #arg2是人ID
        if ctx.author.id != 429825029354553350:
            await ctx.send(f'{ctx.author.mention}\n-w-...(完全不理你)')
            return
        if arg1 == "" or arg2 == "":
            await ctx.send(f'{ctx.author.mention}\n您似乎沒有說要給什麼呢-w-...')
            return
        if arg1 in item_id_file:
            await ctx.send(f'{ctx.author.mention}\n這個東西似乎名稱不對呢-w-...\n請確定您輸入的是不含稀有度的道具全名-w-...')
            return
        theresult=giveitem(int(arg2),arg1,int(arg3))
        if theresult != True:
            await ctx.send(f'{ctx.author.mention}\n{theresult}')
        else:
            await ctx.send(f'{ctx.author.mention}\n您成功給予了{arg2}君{arg3}個{arg1}owo')

    @commands.command()
    async def sethp(self,ctx,arg1=""):
        if ctx.author.id == 429825029354553350:
            global boss_hp
            if arg1=="":
                await ctx.send(f'{ctx.author.mention}\n啊你是要不要說設多少啦-w-...')
            else:
                if arg1.isdecimal():
                    boss_hp=int(arg1)
                    await ctx.send(f'{ctx.author.mention}\n血量已設定成{arg1} owo')
                else:
                    await ctx.send(f'{ctx.author.mention}\n你他媽設的要是數字啦-w-...')
        else:
            await ctx.send(f'{ctx.author.mention}\n-w-...(完全不理你)')

    @commands.command() 
    async def myitem(self,ctx,*args):
        myitemuser=ctx.author
        users=[]
        furusers=[]
        outmes=""
        itemrawdata=doread(item)
        furrawdata=doread(furfile)
        for rawdata in itemrawdata:
            users.append(int(rawdata[0]))
        for rawdata in furrawdata:
            furusers.append(int(rawdata[0]))
        if ctx.author.id in users:
            raw_available_item=readitem(itemrawdata[users.index(ctx.author.id)])
            tooth=(itemrawdata[users.index(ctx.author.id)][1])
            if ctx.author.id in furusers:
                fur=furrawdata[furusers.index(ctx.author.id)][1]
            else:
                fur=0
            outmes+="您的持有道具如下：\n"
            outmes+=f"雪狼牙：{tooth}顆\n"
            outmes+=f"雪狼毛：{fur}撮\n"
            outmes+=f"持有道具：\n"
            item_have=[]
            item_count=[]
            availableitem=0
            for raw in raw_available_item:
                raw=raw.split('%')
                item_have.append(raw[0]) #str全名
                item_count.append(int(raw[1]))
            for allitem in item_id_file:
                if allitem in item_have:
                    if item_count[item_have.index(allitem)] !=0:
                        outmes+=f"{find_item_value(find_item_id(allitem))[2]}**{allitem}**：{item_count[item_have.index(allitem)]}個\n"
                        outmes+=f"{find_item_value(find_item_id(allitem))[3]}\n\n"
                        availableitem+=1
            if availableitem ==0:
                outmes+="您目前沒有任何道具...-w-"
            
            if "show" in args:
                if len(outmes)<1900:
                    await ctx.send(f'{ctx.author.mention}\n{outmes}')
                else:
                    outfile=discord.File(createtxt(outmes))
                    await ctx.send(f'{ctx.author.mention}\n',file=outfile)
            else:
                await ctx.send(f'{ctx.author.mention}\n您的道具資訊已經傳送到私訊了！')
                if len(outmes)<1900:
                    await myitemuser.send(f'{ctx.author.mention}\n{outmes}')
                else:
                    outfile=discord.File(createtxt(outmes))
                    await myitemuser.send(f'{ctx.author.mention}\n',file=outfile)
                    
        else:
            await ctx.send(f'{ctx.author.mention}\n您似乎什麼都沒有呢-w-...')

    @commands.command() 
    async def hitrank(self,ctx):
        intkiller=[]
        intkilltime=[]
        have_counted=[]
        complexlist=[]
        outmes=""
        skippingnumber=[]
        history=doread("csvfile\\killed.csv")
        for a in history:
            if a not in have_counted:
                intkiller.append(int(a[0]))
                intkilltime.append(history.count(a))
                have_counted.append(a)
        for those in intkiller:
            complexlist.append([those,intkilltime[intkiller.index(those)]])
        intkilltime.sort(reverse=True)
        for b in range(1,21):
            if b not in skippingnumber:
                for that in complexlist:
                    if intkilltime[b-1]==that[1]:
                        aple=await self.bot.fetch_user(that[0])
                        truename=aple.display_name
                        outmes+=f"第{b}名:{truename}({that[1]}次)\n"
                if intkilltime.count(intkilltime[b-1])>1:
                    for thth in range(1,intkilltime.count(intkilltime[b-1])):
                        skippingnumber.append(b+thth)
        await ctx.send(f'{ctx.author.mention}\n目前把狛克變成薩摩耶次數的前20名排行榜：\n{outmes}')

    @commands.command()
    async def furshop(self,ctx,arg1="",arg2="1"):
        outmes=""
        if arg1=="" and arg2=="1":
            outmes+=f"歡迎來到雪狼毛商店！\n"
            outmes+=f"輸入[k!furshop (品項名稱) (數量)]來用雪狼毛購買商品！\n"
            shoplist=[elem for elem in furryshop]
            for count in range(0,len(furryshop)):
                outmes+=f"{count+1}.{shoplist[count]}(價格：{furryshop[shoplist[count]]})\n"
        elif arg1 in furryshop:
            if arg2.isdecimal():
                thenum=int(arg2)*furryshop[arg1]
                zzzz=removefur(ctx.author.id,thenum)
                if zzzz !=True:
                    outmes+=f"{zzzz}"
                else:
                    giveitem(ctx.author.id,arg1,arg2)
                    outmes+=f"以{thenum}撮雪狼毛獲得了{arg2}個{arg1}！"
            else:
                outmes+=f"商品數量請輸入整數-w-..."
        else:
            outmes+=f"無法辨識！請確定商品編號正確！"
        await ctx.send(f'{ctx.author.mention}\n{outmes}')

    @commands.command()
    async def index(self,ctx,arg1=""):
        outmes=""
        dicting={"A":"改名型卷軸","B":"傷害保障型卷軸","C":"武器變化類卷軸","D":"連擊型卷軸","E":"追擊類卷軸","F":"傷害變化型卷軸","J":"血量改寫型卷軸","O":"令牌","X":"召喚類卷軸"}
        dicting2={"1":"[☆]道具","2":"[☆☆]道具","3":"[☆☆☆]道具"}
        Cdicting={"a":"必定攻擊","b":"必定補血","c":"可能為攻擊或補血"}
        if arg1=="":
            outmes+=f"輸入[k!index (種類代碼)]來查詢卷軸圖鑑！\n"
            for everything in dicting:
                outmes+=f"{everything}：{dicting[everything]}\n"
            for everything in dicting2:
                outmes+=f"{everything}：{dicting2[everything]}\n"
        elif arg1 in dicting:
            setsumei=doread("csvfile\\itemdata.csv")
            itemlist=[ele for ele in setsumei if ele[1].startswith(arg1)]
            for item in itemlist:
                outmes+=f"{item[2]}**{item[0]}** (一單位：{item[4].replace('t','到')}個)\n{item[3]}\n"
                if item[1].startswith("C"):
                    outmes+=f"(行動型態：{Cdicting[item[5]]})"
                outmes+=f"\n\n"
        elif arg1 in dicting2:
            setsumei=doread("csvfile\\itemdata.csv")
            itemlist=[ele for ele in setsumei if ele[2]==f"[{'☆'*int(arg1)}]"]
            for item in itemlist:
                outmes+=f"{item[2]}**{item[0]}** (一單位：{item[4].replace('t','到')}個)\n{item[3]}\n"
                if item[1].startswith("C"):
                    outmes+=f"(行動型態：{Cdicting[item[5]]})"
                outmes+=f"\n\n"
        else:
            outmes+=f"無法辨識！請確定代碼正確！"
        await ctx.send(f'{ctx.author.mention}\n{outmes}')

    @commands.command()
    async def timelimit(self,ctx,arg):
        if ctx.author.id == 429825029354553350:
            global timelimited
            if arg=="on":
                timelimited=True
                await ctx.send(f'開了啦-w-')
            if arg=="off":
                timelimited=False
                await ctx.send(f'關了啦-w-')
        else:
            await ctx.send(f'{ctx.author.mention}\n-w-...(完全不理你)')

    @commands.command()
    async def announce(self,ctx,arg):
        for channelcode in available_channel:
            channel=self.bot.get_channel(channelcode)
            await channel.send(f'{arg}')
                    
def setup(bot):
    bot.add_cog(Rpg(bot))