#################################################
# Animation Exercise
#################################################

from tkinter import *

def init(data): pass                 # initialize the model (data.xyz)
def mousePressed(event, data): pass  # use event.x and event.y
def mouseDragged(event, data): pass  # use event.x and event.y
def mouseReleased(event, data): pass # use event.x and event.y
def mouseMoved(event, data): pass    # use event.x and event.y
def keyPressed(event, data): pass    # use event.key
def timerFired(data): pass           # respond to timer events
def drawAll(canvas, data): pass      # view the model in the canvas

####################################
# Place your code here:
####################################
import random
import pygame
pygame.mixer.init()

class Table(object):
    def __init__(table, cx, cy, color, change):
        table.cx=cx
        table.cy=cy
        table.color=color
        table.change=change
        table.angle=0
        table.request=''
        table.waitTime=0
        table.eating=False
        table.waiting=False
        table.bumped=False
        table.slow=False
        table.freeze=False
        table.freezetime=0
    
class Food(object):
    def __init__(food, name, type):
        food.name=name
        food.type=type

class People(object):
    def __init__(people,cx, cy, color):
        people.cx=cx
        people.cy=cy
        people.color=color

def gettingTop10():
    Leaderboard= open("Leaderboard.txt","r")
    topScores=Leaderboard.readlines()
    names=[]
    name=''
    scores=[]
    number=''
    leaderboard=[]
    for x in topScores:
        for i in x:
            if i.isalpha():
                name+=i
            elif i.isdigit():
                number+=i 
        if number!='':
            scores.append(int(number))
            names.append(name)
        name=''
        number=''
    for i in range(len(names)):
        names[i]=[names[i]]+[scores[i]]
    Top10=SortTheLists(names, scores)
    Leaderboard.close()
    return Top10
    
def SortTheLists(L1,L2):
    L2.sort()
    L2.reverse()
    leaderboard=[]
    names=len(L1)
    for i in range(len(L2)):
        for name in range(names):
            if L2[i] in L1[name] and L1[name] not in leaderboard:
                leaderboard.append(L1[name])
    return leaderboard

def AddScore(x, data):
    y=input('What is your name? ')
    newScore=x
    board=open("Leaderboard.txt","a+")
    board.write('\n'+y+','+str(newScore))
    board.close()
    
def TableOrder(table, data):
    food=['Entrée','Meal','Omelette','Sandwich']
    while table.request!='' or table.color!='white':
        table=data.tables[random.randint(0,17)]
    table.request=Food(random.choice(food), 'order')
    table.waiting=True
    music=pygame.mixer.Sound('Order.ogg')
    if data.soundEffect==True:
        music.play()
    return table

def RandomizeStyle(data):
    Colors=['navy', 'cyan', 'deep pink', 'dark violet', 'red', 'orange', 'yellow', 'blue', 'green', 'dark green', 'magenta', 'purple', 'gold', 'indian red']
    data.background=random.choice(Colors)
    Colors.remove(data.background)
    data.label=random.choice(Colors)
    Colors.remove(data.label)
    data.kitchen=random.choice(Colors)
    Colors.remove(data.kitchen)
    data.iceCream=random.choice(Colors)
    Colors.remove(data.iceCream)
    data.Lemonade=random.choice(Colors)
    Colors.remove(data.Lemonade)
    return True

def LosingGame(list, data):
    counter=0
    for item in list:
        if (item.waiting==True or item.eating==True):
            counter+=1
        else: return False
    if (counter==len(list)): 
        data.gameOver=True
        data.gameScreen=4
        return data.gameOver

def selectionSlider(x, data):
    circle=0
    if 834<x<850:
        circle=1
    elif 929<x<945:
        circle=2
    elif 1024<x<1040:
        circle=3
    elif 1119<x<1135:
        circle=4
    return circle
    
def timeSlider(x, data):
    if 788<=x<=799.5:
        time=0
    elif 799.5<x<=811:
        time=1
    elif 811<x<=822.5:
        time=2
    elif 822.5<x<=834:
        time=3
    elif 834<x<=850:
        time=4
    elif 850<x<=861.25:
        time=5
    elif 861.25<x<=872.5:
        time=6
    elif 872.5<x<=883.75:
        time=7
    elif 883.75<x<=895:
        time=8
    elif 895<x<=906.25:
        time=9
    elif 906.25<x<=917.5:
        time=10
    elif 917.5<x<=929:
        time=11
    elif 929<x<=945:
        time=12
    elif 945<x<=956.25:
        time=13
    elif 956.25<x<=967.5:
        time=14
    elif 967.5<x<=978.75:
        time=15
    elif 978.75<x<=990:
        time=16
    elif 990<x<=1001.25:
        time=17
    elif 1001.25<x<=1012.5:
        time=18
    elif 1012.5<x<=1024:
        time=19
    elif 1024<x<=1040:
        time=20
    elif 1040<x<=1051.25:
        time=21
    elif 1051.25<x<=1062.5:
        time=22
    elif 1062.5<x<=1073.75:
        time=23
    elif 1073.75<x<=1085:
        time=24
    elif 1085<x<=1096.25:
        time=25
    elif 1096.25<x<=1107.5:
        time=26
    elif 1107.5<x<=1119:
        time=27
    elif 1119<x<=1135:
        time=28
    elif 1135<x<=1150:
        time=29
    elif 1150<x<=1166:
        time=30
    return time
def InstructionMessages(n,data):
    if 0<n<12:
        data.color='cyan'
        data.foodoh=''
        data.selection=[]   
    if n==1:
        message='This is a quick introduction to get you comfortable with the game' 
    elif n==2:
        message='Right above this text you can see in which floor you are in'
    elif n==3:
        message='On the top right corner you can see the time, and your score on the left corner'
    elif n==4:
        message='The cyan diamond in the center of the screen will be your cursor'
    elif n==5:
        message='Each circle represents a table that you will have to serve'
    elif n==6:
        message='To the left of the screen you can see the kitchen, thats where you get the food from'
    elif n==7:
        message="There are two types of food in the kitchen the table's order "+ 'and "Refreshments"'
    elif n==8:
        message="Theres a limited amount of refreshments but they will make the customers happier"
    elif n==9:
        message='Next, lets do a quick tutorial in order to get you ready for the game'
    elif n==10:
        message='If you feel confident you can skip the tutorial and go back to the main screen'
        for table in data.tables:
            table.request=''
            table.waiting=False
    elif n==11:
        message='It looks like one of the tables has an order, get the food from the kitchen'
    elif n==12:
        message='The cursor changed to the food you picked up, now place the food on the table'
        for table in data.tables:
            if table.color=='red':
                table.color='white'
            if table.eating==True:
                table.eating=False
                table.color='white'
                table.waiting=True
    elif n==13:
        message='GREAT JOB! you got the right order to the table on time'
    elif n==14:
        message='when a table is waiting for their food a yellow circle will start to form'
    elif n==15:
        message='Be Careful! in a real game if you do not serve the table on time you will lose points'
    elif n==16:
        message='When the table is eating a red circle will start to form'
    elif n==17:
        message='The table has finished eating and the customers have left, is time to clean up!'
        for table in data.tables:
            if table.color!='white':
                table.color='red'
                table.eating=False
    elif n==18:
        message='Press and hold the mouse to turn on the Cleaning Mode, the cursor will turn pink'
    elif n==19:
        message='Hover over the tables to clean up and then go to the kitchen and release the mouse'
        counter=0
        for table in data.tables:
            if table.color=='white':
                counter+=1
        if counter==len(data.tables):
            table=data.tables[random.randint(0,17)]
            table.color='red'
    elif n==20:
        message='YOU DID IT! keep in mind that you can clean up multiple tables at the same time'
    elif n==21:
        message='Lets check out how the "Refreshments" makes the customers happier'
        for table in data.tables:
            if table.request!='':
                table.request=''
                table.waiting=False
    elif n==22:
        message='Looks like another table has an order, lets give it some Ice Cream for now'
    elif n==23:
        message='Yes, as expected serving ice cream to a table will "freeze" it for a short duration'
    elif n==24:
        message='Lets try serving Lemonade this time'
    elif n==25:
        message='Serving Lemonade to a table will slow down the waiting ratio for that table'
    elif n==26:
        message='your score increases if you serve the correct orders and clean the tables'
    elif n==27:
        message='your score will decrease if you do one of the following actions'
    elif n==28:
        message='serve the wrong order, bump on a table, or do not fulfill an order'
    elif n==29:
        message='Thats all you need to know, go on and enjoy the game, Good Luck!'
    elif n==30:
        message=''
        data.gameScreen=0
        for table in data.tables:
            table.request=''
            table.waitTime=0
            table.eating=False
            table.waiting=False
            table.bumped=False
            table.slow=False
            table.freeze=False
            table.freezetime=0
        data.foodoh=''
    
    return message
def TableStatus(canvas, table, data):
    r=30
    if (table.waiting==True):
        canvas.create_arc(table.cx-r,table.cy-r,table.cx+r,table.cy+r, start=90, extent=table.angle*(-1), fill='yellow')
        canvas.create_text(table.cx, table.cy, text=table.request.name, font='times 12 bold')
    elif (table.eating==True):
        canvas.create_arc(table.cx-r,table.cy-r,table.cx+r,table.cy+r, start=90, extent=table.angle, fill='red',outline='')

def distance(x1,y1,x2,y2):
    d=((x1-x2)**2+(y1-y2)**2)**.5
    return d

def init(data):
    data.timerSec=59
    data.timerDelay=1000
    data.timerMin=4
    data.gameScreen=0
    data.tables=[]
    data.tables2=[]
    data.people=[]
    data.selection=[]
    data.cursorx=0
    data.symbol=PhotoImage(file="soundlogo.png")
    data.SF=PhotoImage(file="SFX.png")
    data.OliveBranchR=PhotoImage(file='OliveBranch2.png')
    data.OliveBranchL=PhotoImage(file='OliveBranch.png')
    data.LeaderboardBackground=PhotoImage(file='Leaderboard.png')
    data.cursory=0
    data.color='cyan'
    data.Win=False
    data.food=False
    data.foodoh=''
    data.controls=False
    data.poh=False
    data.pause=False
    data.Leaderboard=gettingTop10()
    data.highScore=False
    data.error2=''
    data.score=0
    data.difficulty='Normal'
    data.Multiplier=2
    data.difficultyButton=2
    data.LemonadeLeft=10
    data.IceCreamLeft=5
    data.error=''
    data.minSelection=False
    data.minSelectionx=842
    data.minColor='yellow'
    data.minCircle='grey'
    data.secSelection=False
    data.secSelectionx=1166
    data.secColor='yellow'
    data.secCircle='grey'
    data.messageNumber=0
    data.selectionx=0
    data.selectiony=0
    data.Interval=5
    data.gameOver=False
    data.music=True
    data.volume=True
    data.soundEffect=True
    data.entry=True
    data.colorSelected=''
    data.count=0
#-------------------------------Customizeable Colors----------------------------
    data.label='pink'
    data.background='white'
    data.kitchen='yellow'
    data.iceCream='light blue'
    data.Lemonade='pink'
#--------------------------------end game screen--------------------------------
    data.bumps=0
    data.tablesServed=0
    data.tablesCleaned=0
    data.tablesLeft=0
    data.wrongOrders=0
    n=1
    while n<19:
        space=280
        if (n<5):
            table=Table(80+space*n, 130, 'white',False)
            data.tables.append(table)
            space=80
            table=Table(815+space*n, 512, 'white',False)
            data.tables2.append(table)
        elif (n<8):
            table=Table(220+space*(n%4),230, 'white',False)
            data.tables.append(table)
            space=80
            table=Table(855+space*(n%4),540.5, 'white',False)
            data.tables2.append(table)
        elif (n<12):
            table=Table(80+space*(n%7), 330, 'white',False)
            data.tables.append(table)
            space=80
            table=Table(815+space*(n%7), 569, 'white',False)
            data.tables2.append(table)
        elif (n<15):
            table=Table(220+space*(n%11), 430, 'white',False)
            data.tables.append(table)
            space=80
            table=Table(855+space*(n%11), 597.5, 'white',False)
            data.tables2.append(table)
        else:
            table=Table(80+space*(n%14),530, 'white',False)
            data.tables.append(table)
            space=80
            table=Table(815+space*(n%14),626, 'white',False)
            data.tables2.append(table)
        n+=1
def timerFired(data):
    if data.gameScreen!=0:
        data.controls=False
    if data.entry==True and data.music==True and data.volume==True:
        pygame.mixer.music.load('Entry.mp3')
        pygame.mixer.music.play()
    data.entry=False
    LosingGame(data.tables, data)
    if (data.gameOver==False):
#-----------------------------------Time----------------------------------------
        if data.gameScreen==-1 and data.messageNumber>10:
            for table in data.tables:
                if (table.request!='' or table.color!='white'):
                        if table.freeze==False and table.slow==False:
                            table.angle+=20
                        elif table.freeze==True:
                            table.freezetime+=1
                            if table.freezetime==5:
                                table.freeze=False
                                table.freezetime=0
                        elif table.slow==True:
                            table.angle+=10
        if (data.gameScreen==1 and data.pause==False):
            data.timerSec-=1
            if (data.timerSec/data.Interval==data.timerSec//data.Interval):
                table=data.tables[random.randint(0,17)]
                TableOrder(table, data)
            if (data.timerSec==0 and data.timerMin>0):
                data.timerSec=59
                data.timerMin-=1
#-----------------------------people Eating/waiting-------------------------------------
            for table in data.tables:
                if (table.request!='' or table.color!='white'):
                        if table.freeze==False and table.slow==False:
                            table.angle+=20
                        elif table.freeze==True:
                            table.freezetime+=1
                            if table.freezetime==5:
                                table.freeze=False
                                table.freezetime=0
                        elif table.slow==True:
                            table.angle+=10
                        if table.angle==360:
                            table.request=''
                            table.angle=0
                            table.slow=False
                            if table.waiting==True:
                                data.score-=(50*data.Multiplier)
                                data.bumps+=1
                                table.color='white'
                                table.waiting=False
                            elif table.eating==True:
                                table.color='red'
                                table.eating=False
#-----------------------------Game Completed------------------------------------
        if (data.timerSec==0 and data.timerMin==0):
            data.gameOver=True
            data.Win=True
            data.gameScreen=4

def mouseMoved(event,data):
    data.count=0
    if data.gameScreen<2:
        data.cursorx=event.x
        data.cursory=event.y
    else:
        data.selectionx=event.x
        data.selectiony=event.y
    if (data.gameScreen==1):
        for table in data.tables:
            if (distance(table.cx, table.cy, event.x, event.y)<=30):
                if(table.request=='' and table.bumped==False or data.foodoh=='' and table.bumped==False ):
                    table.bumped=True
                    data.error='you bumped into a table!!'
                    data.score-=(10*data.Multiplier)
                    data.bumps+=1
            elif(distance(table.cx, table.cy, event.x, event.y)>30):
                data.count+=1
                if (data.count==len(data.tables)):
                    data.error=''
                table.bumped=False
                
def mouseDragged(event,data):
    data.color='pink'
    for table in data.tables:
        if (table.color=='red' and distance(table.cx, table.cy, event.x, event.y)<30):
            data.poh=True
            table.change=True
    if data.minSelection==True:
        if 788<=event.x<=1166:
            data.minSelectionx=event.x
        elif event.x>1166:
            data.minSelectionx=1166
        elif event.x<788:
            data.minSelectionx=788
        data.timerMin=timeSlider(data.minSelectionx, data)
    elif data.secSelection==True:
        if 788<event.x<1166:
            data.secSelectionx=event.x
        elif event.x<788:
            data.secSelectionx=788
        elif event.x>1166:
            data.secSelectionx=1166
        data.timerSec=2*timeSlider(data.secSelectionx,data)

def mouseReleased(event,data):
    if (data.foodoh==''):
        data.color='cyan'
    elif (data.foodoh!=''):
        data.color='white'
    data.cursorx=event.x
    data.cursory=event.y
    if (event.x<250 and data.poh==True):
        for table in data.tables:
            if table.change==True:
                table.change=False
                table.request=''
                table.color='white'
                table.angle=0
                data.score+=(50*data.Multiplier)
                data.tablesCleaned+=1
                if data.gameScreen==-1:
                    data.messageNumber+=1
        data.poh=False
        
def mousePressed(event,data):
    if data.gameScreen==4:
        if event.x>data.width-250 and event.y>data.height-150:
            if data.highScore==True:
                AddScore(data.score, data)
            data.gameScreen=0
            data.timerMin=4
            data.timerSec=59
            data.entry=True
            data.messageNumber=0
            data.score=0
            data.gameOver=False
            data.Win=False
        for table in data.tables:
            table.request=''
            table.waitTime=0
            table.eating=False
            table.waiting=False
            table.bumped=False
            table.slow=False
            table.freeze=False
            table.freezetime=0
            table.color='white'
    if data.gameScreen==1 or data.gameScreen==-1:
        if(1190<event.x<1229 and 652<event.y<688):
            data.music= not data.music
        elif (1126<event.x<1175 and 656<event.y<685):
            data.soundEffect=not data.soundEffect
        elif(1245<event.x<1294 and 651<event.y<686):
            if data.volume==False:
                data.volume=True
                data.music=True
                data.soundEffect=True
            else: 
                data.music=False
                data.volume=False
                data.soundEffect=False
    if data.gameScreen==3:
        if data.width/2-75<event.x<data.width/2+75 and data.height-100<event.y<data.height-50:
            data.gameScreen=0
    colorCounted=0
    if data.controls==True and data.gameScreen==0:
        if 170<event.y<200:
            if 797<event.x<880:
                data.difficultyButton=1
                data.difficulty='Easy'
                data.Interval=12
                data.IceCreamLeft=5
                data.LemonadeLeft=10
                data.Multiplier=1
            elif 883<event.x<968:
                data.difficultyButton=2
                data.difficulty='Normal'
                data.Interval=10
                data.IceCreamLeft=5
                data.LemonadeLeft=3
                data.Multiplier=2
            elif 968<event.x<1054:
                data.difficultyButton=3
                data.difficulty='Hard'
                data.Interval=5
                data.IceCreamLeft=1
                data.LemonadeLeft=3
                data.Multiplier=3
            elif 1054<event.x<1153:
                data.difficultyButton=4
                data.difficulty='Expert'
                data.Interval=3
                data.IceCreamLeft=1
                data.LemonadeLeft=1
                data.Multiplier=5
        elif 473<event.y<674:
            if 792<event.x<1164:
                data.gameScreen=2
        if 788<event.x<1166:
            if 259<event.y<271:
                data.minSelectionx=event.x
                data.timerMin=timeSlider(data.minSelectionx, data)
                data.minSelection=True
            else: data.minSelection=False
            if 327<event.y<339:
                data.secSelectionx=event.x
                data.timerSec=2*timeSlider(data.secSelectionx,data)
                data.secSelection=True
            else: data.secSelection=False
    if data.gameScreen==2:
#-----------------------------picking out a color-------------------------------
        if data.width-250<event.x<data.width-125:
            if 0<event.y<100:
                data.colorSelected='Navy'
            elif 100<event.y<200:
                data.colorSelected='Cyan'
            elif 200<event.y<300:
                data.colorSelected='Deep Pink'
            elif 300<event.y<400:
                data.colorSelected='Dark Violet'
            elif 400<event.y<500:
                data.colorSelected='Red'
            elif 500<event.y<600:
                data.colorSelected='Orange'
            else: data.colorSelected='yellow'
        elif data.width-125<event.x<data.width:
            if 0<event.y<100:
                data.colorSelected='Blue'
            elif 100<event.y<200:
                data.colorSelected='Green'
            elif 200<event.y<300:
                data.colorSelected='Dark Green'
            elif 300<event.y<400:
                data.colorSelected='Magenta'
            elif 400<event.y<500:
                data.colorSelected='Purple'
            elif 500<event.y<600:
                data.colorSelected='Gold'
            else: data.colorSelected='Indian Red'
#------------------------------placing the colors-------------------------------
        if 0<event.x<1050 and 0<event.y<50:
            data.label=data.colorSelected
        elif 5<event.x<120 and 405<event.y<695:
            data.iceCream=data.colorSelected
        elif 130<event.x<245 and 405<event.y<695:
            data.Lemonade=data.colorSelected
        elif 0<event.x<250 and 50<event.y<data.height:
            data.kitchen=data.colorSelected
        elif data.width-350<event.x<data.width-250 and data.height-60<event.y<data.height:
            RandomizeStyle(data)
        elif data.width/2-100<event.x<data.width/2+100 and data.height-40<event.y<data.height:
            data.controls=False
            data.gameScreen=0
        elif 250<event.x<1050 and 50<event.y<700:
            data.background=data.colorSelected
    else: 
        data.colorSelected=''
    if data.gameScreen==-1:
        if 250+(data.width-250)/2-70<event.x<250+(data.width-250)/2+70 and data.height-40<event.y<data.height:
            init(data)
    if data.messageNumber==18:
        data.messageNumber+=1
#-----------------------------Main Screen Functions--------------------------
    if(data.gameScreen==0):
        if (data.width/2-70<event.x<data.width/2+70):
            if (data.height/2-120<event.y<data.height/2-80):
                data.score=0
                data.gameScreen=1
                data.messageNumber=29
                if data.music==True and data.volume==True:
                    pygame.mixer.music.load('Restaurant.mp3')
                    pygame.mixer.music.play()
            elif data.height/2-70<event.y<data.height/2-30:
                data.controls=not data.controls
            elif(data.height/2-20<event.y<data.height/2+20):
                data.score=0
                data.gameScreen=-1
            elif(data.height/2+30<event.y<data.height/2+70):
                data.Leaderboard=gettingTop10()
                data.gameScreen=3
        elif(1190<event.x<1229 and 14<event.y<44):
            data.music= not data.music
        elif(1245<event.x<1294 and 11<event.y<52):
            if data.volume==False:
                data.volume=True
                data.music=True
                data.soundEffect=True
            else: 
                data.music=False
                data.volume=False
                data.soundEffect=False
    if data.music==False or data.volume==False:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        if (1126<event.x<1175 and 17<event.y<44):
            data.soundEffect=not data.soundEffect
#------------------------------getting food from kitchen------------------------
    if data.gameScreen==1 or data.messageNumber>10:
        if (5<event.x<120):
            if(55<event.y<170):
                data.selection=[Food('Omelette','order')]
                data.foodoh='Omelette'
            elif(180< event.y<295):
                data.selection=[Food('Sandwich', 'order')]
                data.foodoh='Sandwich'
            elif (data.height/2+55<event.y<data.height-5 and data.IceCreamLeft>0):
                if data.messageNumber>21:
                    data.selection=[Food('Ice Cream', 'Refreshment')]
                    if data.gameScreen>0:
                        data.IceCreamLeft-=1
                    data.foodoh='Ice Cream'
            data.color='white'
            data.food=True
        elif (130<event.x<245):
            if(55<event.y<170):
                data.selection=[Food('Meal', 'order')]
                data.foodoh='Meal'
            elif(180<event.y<295):
                data.selection=[Food('Entrée','order')]
                data.foodoh='Entrée'
            elif (data.height/2+55<event.y<data.height-5 and data.LemonadeLeft>0):
                if data.messageNumber>23:
                    data.selection=[Food('Lemonade', 'Refreshment')]
                    data.foodoh='Lemonade'
                    if data.gameScreen>0:
                        data.LemonadeLeft-=1
            data.food=True
            data.color='white'
        if data.color=='white' and data.messageNumber==11 and len(data.selection)>0:
            data.messageNumber+=1
#------------------------------putting food on tables---------------------------
        for table in data.tables:
            if (distance(table.cx,table.cy,event.x,event.y)<30 and  table.request!=
                '' and len(data.selection)!=0):
                if data.selection[0].type=='Refreshment':
                    if data.foodoh=='Lemonade':
                        if data.messageNumber==25:
                            data.messageNumber+=1
                        table.slow=True
                        if data.messageNumber==24:
                            data.messageNumber+=1
                    elif data.foodoh=='Ice Cream':
                        if data.messageNumber==22:
                            data.messageNumber+=1
                        table.freeze=True
                    table.bumped=True
                    data.selection.pop()
                    data.foodoh=''
                    data.color='cyan'
                elif data.selection[0].name==table.request.name:
                    if data.messageNumber!=22:
                        if data.messageNumber!=24:
                            if (table.request.name=='Omelette'):
                                table.color='Green'
                            elif(table.request.name=='Sandwich'):
                                table.color='Purple'
                            elif(table.request.name=='Meal'):
                                table.color='Blue'
                            elif(table.request.name=='Entrée'):
                                table.color='Orange'
                            table.bumped=True
                            table.waiting=False
                            table.eating=True
                            data.selection.pop()
                            table.angle=0
                            data.score+=(50*data.Multiplier)
                            data.tablesServed+=1
                            data.foodoh=''
                            data.food=False
                            data.color='cyan'
                            if data.messageNumber==12:
                                data.messageNumber+=1
                elif data.selection[0].type=='order': 
                    data.selection.pop()
                    data.score-=(20*data.Multiplier)
                    data.wrongOrders+=1
                    data.foodoh=''
                    table.bumped=True
                    if (len(data.selection)==0):
                        data.error2='Wrong Order!'
        if len(data.selection)==1:
            data.error2=''
def keyPressed(event,data):
    a=[11]+[12]+[18]+[19]+[22]+[25]
    a=set(a)
    event.key=event.key.lower()
    if (event.key=='enter' and data.gameScreen==0):
        data.gameScreen=1
    elif (event.key=='r'):
        init(data)
    elif (event.key=='p' and data.gameScreen==1):
        data.pause=not data.pause
    if (data.gameScreen==-1):
        nextPage=pygame.mixer.Sound('Tutorial SF.ogg')
        if event.key=='left':
            if data.messageNumber==0:
                data.gameScreen=0
                for table in data.tables:
                    table.request=''
                    table.waitTime=0
                    table.eating=False
                    table.waiting=False
                    table.bumped=False
                    table.slow=False
                    table.freeze=False
                    table.freezetime=0
            else:
                data.messageNumber-=1
                if data.soundEffect==True:
                    nextPage.play()
        elif event.key=='right':
            if data.messageNumber not in a:
                data.messageNumber+=1
                if data.soundEffect==True:
                    nextPage.play()
                if data.messageNumber==11 or data.messageNumber==22:
                    table=data.tables[random.randint(0,17)]
                    TableOrder(table, data)
def drawAll(canvas, data):
    key='times 20 bold'
    if (data.gameScreen==0):
#--------------------------------------Entry Screen--------------------------------------------------
        canvas.create_rectangle(0,0,data.width,data.height, fill='red')
        canvas.create_arc(0,10, data.width, 2*data.height, start=0, extent=180, fill='black')
        canvas.create_text(data.width/2,data.height/6, text='Press Enter or press start to play!', font='times 20 bold',
        fill='white')
        xm=70
        ym=20
        canvas.create_rectangle(data.width/2-xm, data.height/2-ym-100, data.width/2+xm, data.height/2-80, fill='green')
        canvas.create_rectangle(data.width/2-xm, data.height/2-ym-50,data.width/2+xm, data.height/2-30, fill='yellow')
        canvas.create_rectangle(data.width/2-xm, data.height/2-ym, data.width/2+xm, data.height/2+ym, fill='orange')
        canvas.create_rectangle(data.width/2-xm, data.height/2-ym+50, data.width/2+xm, data.height/2+ym+50, fill='blue')
        canvas.create_text(data.width/2, data.height/10, text='Dining Max', 
        font='times 60 bold italic underline', fill='white')
        canvas.create_text(data.width/2, data.height/2-100, text='Start', font='arial 20 bold',)
        canvas.create_text(data.width/2, data.height/2-50, text='Controls', font='arial 20 bold')
        canvas.create_text(data.width/2, data.height/2, text='Introduction', font='arial 20 bold')
        canvas.create_text(data.width/2, data.height/2+50, text='Leaderboard', font='arial 20 bold')
        canvas.create_text(data.width-150, 30, text='Sound\nEffects', font='arial 15 bold')
        canvas.create_image(data.width-90, 30, image=data.SF)
        canvas.create_image(data.width-30, 30, image=data.symbol)
        if data.music==False:
            canvas.create_line(1190, 44, 1229, 14, fill='black', width=5)
        if data.volume==False:
            canvas.create_line(1245, 52, 1294, 11, fill='black', width=5)
        if data.soundEffect==False:
            canvas.create_line(1126,44,1175, 17, fill='black', width=5)
#-----------------------------------Controls Section---------------------------------------------------
        if data.controls==True:
            canvas.create_polygon(data.width/2+60,data.height/2-50, data.width/2+100, data.height/2-125, data.width/2+100, data.height/2+25, fill='white')
            canvas.create_rectangle(data.width/2+100, 100, data.width-100, data.height, fill='white', outline='')
            canvas.create_rectangle(data.width/2+110, 110, data.width-110, data.height-10, fill='black')
            canvas.create_text(975, 140, text='Difficulty', font='times 40 italic bold', fill='white')
            canvas.create_text(970,234, text='Time', font='times 40 italic bold', fill='white')
            canvas.create_line(788, 262, 1166, 262, fill='grey', width=2)
            canvas.create_line(788, 254, 788, 270, fill='grey', width=2)
            canvas.create_line(1166, 254, 1166, 270, fill='grey', width=2)
            canvas.create_text(971, 298, text=str(data.timerMin)+' Minutes', font='times 25 bold', fill='white')
            canvas.create_line(788, 331, 1166, 331, fill='grey', width=2)
            canvas.create_line(788, 323, 788, 339, fill='grey', width=2)
            canvas.create_line(1166, 323, 1166, 339, fill='grey', width=2)
            canvas.create_text(971, 364, text=str(data.timerSec)+' Seconds', font='times 25 bold', fill='white')
            space=1
            center=95
            xmargin=46.5
            while space<5:
                text='arial 15 bold'
                selected=''
                if space==1:
                    difficulty='Easy'
                    color='light blue'
                    if data.difficultyButton==1:
                        text='arial 20 bold'
                        selected='yellow'
                elif space==2:
                    difficulty='Normal'
                    color='green'
                    if data.difficultyButton==2:
                        text='arial 20 bold'
                        selected='yellow'
                elif space==3:
                    difficulty='Hard'
                    color='orange'
                    if data.difficultyButton==3:
                        text='arial 20 bold'
                        selected='yellow'
                elif space==4:
                    difficulty='Expert'
                    color='red'
                    if data.difficultyButton==4:
                        text='arial 20 bold'
                        selected='yellow'
                if selectionSlider(data.minSelectionx, data)==space:
                    if space==1:
                        data.timerMin=4
                    else: data.timerMin=(space*8)-4
                    data.minColor=''
                    data.minCircle='yellow'
                else: data.minCircle='grey'
                if selectionSlider(data.secSelectionx, data)==space:
                    if space==1:
                        data.timerSec=8
                    else: data.timerSec=(space*16)-8
                    data.secColor=''
                    data.secCircle='yellow'
                else: data.secCircle='grey'
                canvas.create_rectangle((data.width/2+89)+(center*space)-xmargin, 170,(data.width/2+89)+(center*space)+xmargin, 200, fill=color, outline=selected, width=3)
                canvas.create_text((data.width/2+89)+center*space, 185, text=difficulty, fill='black', font=text)
                canvas.create_oval((data.width/2+89)+center*space,254, (data.width/2+105)+center*space, 270, fill=data.minCircle)
                canvas.create_oval((data.width/2+89)+center*space,323, (data.width/2+105)+center*space, 339, fill=data.secCircle)
                space+=1
            if selectionSlider(data.minSelectionx,data)==0:
                data.minColor='yellow'
            if selectionSlider(data.secSelectionx,data)==0:
                data.secColor='yellow'
            canvas.create_text(971, 430, text='Game Layout', font='times 40 italic bold', fill='white')
            canvas.create_text(976, 461, text='Click on the game layout in order to customize its colors', fill='white')
            canvas.create_polygon(data.minSelectionx-5, 262, data.minSelectionx, 252, data.minSelectionx+5, 262, data.minSelectionx, 272,  fill=data.minColor)
            canvas.create_polygon(data.secSelectionx-5, 331, data.secSelectionx, 321, data.secSelectionx+5, 331, data.secSelectionx, 341, fill=data.secColor)
#-------------------------------------small layout screen-----------------------
            width=1164
            height=674
            canvas.create_rectangle(792,487, 1164,674, fill=data.background)
            canvas.create_rectangle(792,487,863, height, fill=data.kitchen)
            canvas.create_text(827,581, text='Kitchen', font='arial 8 bold')
            canvas.create_rectangle(794,491,826,523, fill='green')
            canvas.create_text(810,507, text='Omelette', fill='black', font='arial 6 bold')
            canvas.create_rectangle(829,491,861,523, fill='blue')
            canvas.create_text(845,507, text='Meal', fill='black', font='arial 6 bold')
            canvas.create_rectangle(794,526, 826,558, fill='purple')
            canvas.create_text(810,542, text='Sandwich', fill='black', font='arial 6 bold')
            canvas.create_rectangle(829,526, 861,558, fill='orange')
            canvas.create_text(845,542, text='Entrée', fill='black', font='arial 6 bold')
            canvas.create_rectangle(794,671,826,604, fill=data.iceCream)
            canvas.create_text(810,638, text='Ice Cream', font='arial 6 bold')
            canvas.create_text(810,644, text='Scoops Left:'+str(data.IceCreamLeft), font='times 4 bold')
            canvas.create_rectangle(829,671,861,604, fill=data.Lemonade)
            canvas.create_text(845,638, text='Lemonade', font='arial 6 bold')
            canvas.create_text(845,644, text='Drinks Left:'+str(data.LemonadeLeft), font='times 4 bold')
            for table in data.tables2:
                r=8.5
                canvas.create_oval(table.cx-r, table.cy-r, table.cx+r, table.cy+r, fill='white')
            canvas.create_rectangle(792,487, 1164, 473, fill=data.label)
            canvas.create_text(1141, 480, text='Time: '+str(data.timerMin)+':'+str(data.timerSec), 
            font='arial 6 bold italic')
            canvas.create_text(978, 480, text='Dining Max',font='arial 6 bold italic underline')
            canvas.create_text(815, 480, text='Score: '+str(data.score), font='arial 7 bold')
            canvas.create_polygon(1013-4,581, 1013,581-7, 1013+4, 581, 1013,581+7, fill=data.color)
    if (data.gameScreen<3):
        Floor='First Floor'
        label='Pink'
        floorCenter=250+(data.width-250)/2
#-------------------------------------Going to the layout screen----------------------------
    if data.gameScreen==2:
        canvas.create_rectangle(0,0, data.width, data.height, fill=data.background)
        canvas.create_rectangle(data.width/2-100, data.height-40, data.width/2+100, data.height, fill='green')
        canvas.create_rectangle(data.width-350, data.height-60, data.width-250, data.height, fill='white')
        canvas.create_text(data.width-300, data.height-30, text='Random\nStyle', font='times 20 bold')
        canvas.create_text(data.width/2, data.height-20, text='Return to main screen', font='times 20 bold')
        canvas.create_rectangle(0,0,250, data.height, fill=data.kitchen)
        canvas.create_text(125,data.height/2, text='Kitchen', font='arial 26 bold')
        canvas.create_rectangle(5,55,120,170, fill='green')
        canvas.create_text(63,113, text='Omelette', fill='black', font=key)
        canvas.create_rectangle(130,55, 245,170, fill='blue')
        canvas.create_text(188,113, text='Meal', fill='black', font=key)
        canvas.create_rectangle(5,180, 120,295, fill='purple')
        canvas.create_text(63,238, text='Sandwich', fill='black', font=key)
        canvas.create_rectangle(130,180, 245,295, fill='orange')
        canvas.create_text(188,238, text='Entrée', fill='black', font=key)
        canvas.create_rectangle(5,data.height-5,120,data.height/2+55, fill=data.iceCream)
        canvas.create_text(63,data.height-150, text='Ice Cream', font=key)
        canvas.create_text(63,data.height-130, text='Scoops Left:'+str(data.IceCreamLeft), font='times 15 bold')
        canvas.create_rectangle(130,data.height-5, 245, data.height/2+55, fill=data.Lemonade)
        canvas.create_text(188,data.height-5-145, text='Lemonade', font=key)
        canvas.create_text(188,data.height-130, text='Drinks Left:'+str(data.LemonadeLeft), font='times 15 bold')
        for table in data.tables:
            r=30
            canvas.create_oval(table.cx-r, table.cy-r, table.cx+r, table.cy+r, fill=table.color)
            TableStatus(canvas,table,data)
        canvas.create_rectangle(0,0, data.width, 50, fill=data.label)
        canvas.create_text(data.width-80, 20, text='Time: '+str(data.timerMin)+':'+str(data.timerSec), 
        font='arial 20 bold italic')
        canvas.create_text(floorCenter, 25, text='Dining Max',font='arial 20 bold italic underline')
        canvas.create_text(80, 30, text='Score: '+str(data.score), font='arial 26 bold')
        canvas.create_polygon(floorCenter-15,data.height/2, floorCenter,data.height/2-25, floorCenter+15, data.height/2, floorCenter,data.height/2+25, fill='cyan')
        canvas.create_rectangle(data.width-250,0, data.width, data.height, fill='black')
#-------------------------------------Colors------------------------------------------------
        ColorPairs=0
        changey=100
        while ColorPairs<7:
            if ColorPairs==0:
                color1='Navy'
                color2='Blue'
            elif ColorPairs==1:
                color1='Cyan'
                color2='Green'
            elif ColorPairs==2:
                color1='Deep Pink'
                color2='Dark Green'
            elif ColorPairs==3:
                color1='Dark Violet'
                color2='Magenta'
            elif ColorPairs==4:
                color1='Red'
                color2='Purple'
            elif ColorPairs==5:
                color1='Orange'
                color2='Gold'
            else:
                color1='Yellow'
                color2='Indian Red'
            canvas.create_rectangle(data.width-250,0+ColorPairs*changey, data.width-125, 100+ColorPairs*changey, fill=color1)
            canvas.create_text(data.width-187.5, 50+ColorPairs*changey, text=color1, font='times 20 bold')
            canvas.create_rectangle(data.width-125, 0+ColorPairs*changey, data.width, 100+ColorPairs*changey, fill=color2)
            canvas.create_text(data.width-62.5, 50+ColorPairs*changey, text=color2, font='times 20 bold')
            ColorPairs+=1
        canvas.create_text(data.selectionx, data.selectiony, text=data.colorSelected, font='times 20 bold')
#------------------------------------Instruction Screen--------------------------------------
    if (data.gameScreen==-1):
        canvas.create_rectangle(250+(data.width-250)/2-70,data.height,250+(data.width-250)/2+70, data.height-40, fill='green')
        canvas.create_text(250+(data.width-250)/2, data.height-20, text='Skip Tutorial', font='times 20 bold')
        canvas.create_rectangle(0,0,250, data.height, fill='yellow')
        canvas.create_text(125,data.height/2, text='Kitchen', font='arial 26 bold')
        canvas.create_rectangle(5,55,120,170, fill='green')
        canvas.create_text(63,113, text='Omelette', fill='black', font=key)
        canvas.create_rectangle(130,55, 245,170, fill='blue')
        canvas.create_text(188,113, text='Meal', fill='black', font=key)
        canvas.create_rectangle(5,180, 120,295, fill='purple')
        canvas.create_text(63,238, text='Sandwich', fill='black', font=key)
        canvas.create_rectangle(130,180, 245,295, fill='orange')
        canvas.create_text(188,238, text='Entrée', fill='black', font=key)
        canvas.create_rectangle(5,data.height-5,120,data.height/2+55, fill='light blue')
        canvas.create_text(63,data.height-150, text='Ice Cream', font=key)
        canvas.create_text(63,data.height-130, text='Scoops Left:'+str(data.IceCreamLeft), font='times 15 bold')
        canvas.create_rectangle(130,data.height-5, 245, data.height/2+55, fill='pink')
        canvas.create_text(188,data.height-5-145, text='Lemonade', font=key)
        canvas.create_text(188,data.height-130, text='Drinks Left:'+str(data.LemonadeLeft), font='times 15 bold')
        for table in data.tables:
            r=30
            canvas.create_oval(table.cx-r, table.cy-r, table.cx+r, table.cy+r, fill=table.color)
            TableStatus(canvas,table,data)
        canvas.create_rectangle(0,0, data.width, 50, fill=label)
        canvas.create_text(data.width-80, 20, text='Time: '+str(data.timerMin)+':'+str(data.timerSec), 
        font='arial 20 bold italic')
        canvas.create_text(floorCenter, 25, text=Floor,font='arial 20 bold italic underline')
        canvas.create_text(80, 30, text='Score: '+str(data.score), font='arial 26 bold')
        canvas.create_polygon(floorCenter-15,data.height/2, floorCenter,data.height/2-25, floorCenter+15, data.height/2, floorCenter,data.height/2+25, fill=data.color)
        canvas.create_text(floorCenter,data.height/2, text=data.foodoh)
        canvas.create_text(data.width-150, data.height-30, text='Sound\nEffects', font='arial 15 bold')
        canvas.create_image(data.width-90, data.height-30, image=data.SF)
        canvas.create_image(data.width-30, data.height-30, image=data.symbol)
        if data.music==False:
            canvas.create_line(1190, 688, 1229, 652, fill='black', width=5)
        if data.volume==False:
            canvas.create_line(1245, 686, 1294, 651, fill='black', width=5)
        if data.soundEffect==False:
            canvas.create_line(1126,685,1175, 656, fill='black', width=5)
#-----------------------------------Messages----------------------------------------------------
        if data.gameScreen<0:
            canvas.create_text(floorCenter,data.height-60, text='Press the right arrow key to go to the next message; left key to go to the previous message', font='times 25 bold')
        if data.messageNumber>0:
            Instructions=InstructionMessages(data.messageNumber,data)
            canvas.create_rectangle(floorCenter-525, 50, floorCenter+525, 90, fill='black')
            canvas.create_text(floorCenter, 70, text=Instructions, font='times 30 bold', fill='white')
    if (data.gameScreen==3):
#-----------------------------------Leaderboard Screen-------------------------------------------
        canvas.create_rectangle(0,0,data.width, data.height, fill='orange red')
        canvas.create_rectangle(0,0,75,data.height, fill='black')
        canvas.create_rectangle(data.width, 0, data.width-75, data.height, fill='black')
        
        canvas.create_image(data.width/2, data.height/2, image=data.LeaderboardBackground)
        canvas.create_rectangle(data.width/2-250, 50, data.width/2+250, data.height, fill='black')
        canvas.create_rectangle(data.width/2-75, data.height-100, data.width/2+75, data.height-50, fill='black', outline='orange red', width=3)
        canvas.create_text(data.width/2, data.height-75, text='Main Screen', font='times 20 bold', fill='orange red' )
        canvas.create_image(data.width/2-180, data.height/2+50, image=data.OliveBranchL)
        canvas.create_image(data.width/2+180, data.height/2+50, image=data.OliveBranchR)
        canvas.create_text(data.width/2, 90, text='Leaderboard', font='times 70 bold italic', fill='orange red')
        if len(data.Leaderboard)<10:
            for i in range(len(data.Leaderboard)):
                for item in data.Leaderboard[i]:
                    if str(item).isalpha():
                        canvas.create_text(data.width/2-100, 150+40*i, text=item, font='comics 20 bold', fill='white')
                    else: canvas.create_text(data.width/2+100, 150+40*i, text=str(item),font='comics 20 bold', fill='white')
                canvas.create_text(data.width/2-200, 150+40*i, text=str(i+1), font='comics 30 bold', fill='orange red')
        else:
            for i in range(10):
                for item in data.Leaderboard[i]:
                    if str(item).isalpha():
                        canvas.create_text(data.width/2-100, 150+40*i, text=item, font='comics 20 bold', fill='white')
                    else: canvas.create_text(data.width/2+100, 150+40*i, text=str(item),font='comics 20 bold', fill='white')
                canvas.create_text(data.width/2-200, 150+40*i, text=str(i+1), font='comics 30 bold', fill='orange red')
    if data.gameScreen==1:
#-----------------------------------Game Screen--------------------------------------------------
        canvas.create_rectangle(0,0, data.width, data.height, fill=data.background)
        canvas.create_rectangle(0,0,250, data.height, fill=data.kitchen)
        canvas.create_text(125,data.height/2, text='Kitchen', font='arial 26 bold')
        canvas.create_rectangle(5,55,120,170, fill='green')
        canvas.create_text(63,113, text='Omelette', fill='black', font=key)
        canvas.create_rectangle(130,55, 245,170, fill='blue')
        canvas.create_text(188,113, text='Meal', fill='black', font=key)
        canvas.create_rectangle(5,180, 120,295, fill='purple')
        canvas.create_text(63,238, text='Sandwich', fill='black', font=key)
        canvas.create_rectangle(130,180, 245,295, fill='orange')
        canvas.create_text(188,238, text='Entrée', fill='black', font=key)
        canvas.create_rectangle(5,data.height-5,120,data.height/2+55, fill=data.iceCream)
        canvas.create_text(63,data.height-150, text='Ice Cream', font=key)
        canvas.create_text(63,data.height-130, text='Scoops Left:'+str(data.IceCreamLeft), font='times 15 bold')
        canvas.create_rectangle(130,data.height-5, 245, data.height/2+55, fill=data.Lemonade)
        canvas.create_text(188,data.height-5-145, text='Lemonade', font=key)
        canvas.create_text(188,data.height-130, text='Drinks Left:'+str(data.LemonadeLeft), font='times 15 bold')
        for table in data.tables:
            r=30
            canvas.create_oval(table.cx-r, table.cy-r, table.cx+r, table.cy+r, fill=table.color)
            TableStatus(canvas,table,data)
        canvas.create_rectangle(0,0, data.width, 50, fill=data.label)
        canvas.create_text(data.width-80, 20, text='Time: '+str(data.timerMin)+':'+str(data.timerSec), 
        font='arial 20 bold italic')
        canvas.create_text(floorCenter, 25, text='Dining Max',font='arial 20 bold italic underline')
        canvas.create_text(80, 30, text='Score: '+str(data.score), font='arial 26 bold')
        if (data.foodoh==''):
            canvas.create_polygon(data.cursorx-15,data.cursory, data.cursorx,data.cursory-25, data.cursorx+15, data.cursory, data.cursorx,data.cursory+25, fill=data.color)
        canvas.create_text(data.cursorx,data.cursory, text=data.foodoh)
        canvas.create_text(250+(data.width-250)/2,data.height-100, text=data.error+data.error2, font='arial 20 bold', fill='orange')
        canvas.create_text(data.width-150, data.height-30, text='Sound\nEffects', font='arial 15 bold')
        canvas.create_image(data.width-90, data.height-30, image=data.SF)
        canvas.create_image(data.width-30, data.height-30, image=data.symbol)
        if data.music==False:
            canvas.create_line(1190, 688, 1229, 652, fill='black', width=5)
        if data.volume==False:
            canvas.create_line(1245, 686, 1294, 651, fill='black', width=5)
        if data.soundEffect==False:
            canvas.create_line(1126,685,1175, 656, fill='black', width=5)
        if data.pause==True:
            canvas.create_text(data.width/2, data.height/2, text='PAUSED', font='arial 300 bold')
#--------------------------------------On Game Over Screen-----------------------------
    if data.gameScreen==4:
        space=0
        canvas.create_rectangle(0,0,data.width, data.height, fill='black')
        if (data.Win==True):
            canvas.create_text(data.width/2, 80, text='Time is up!', fill='white', font='arial 120 bold')
            canvas.create_text(data.width/2, 200, text='Great Job!', fill='white', font='arial 100 bold')
            canvas.create_rectangle(data.width/2-400, data.height/2-100, data.width/2+400, data.height, fill='white')
            canvas.create_text(data.width/2-280, data.height/2-80, text='Action', font='times 40 bold')
            canvas.create_text(data.width/2, data.height/2-80, text='points', font='times 40 bold')
            canvas.create_text(data.width/2+200, data.height/2-80, text='Difficulty', font='times 40 bold')
            canvas.create_text(data.width/2+350, data.height/2-80, text='Total', font='times 40 bold')
            canvas.create_text(data.width/2-300, data.height/2-30, text='Number of bumps: '+str(data.bumps), font='times 20 bold')
            canvas.create_text(data.width/2-272, data.height/2+20, text='Number of tables served: '+str(data.tablesServed), font='times 20 bold')
            canvas.create_text(data.width/2-250, data.height/2+70, text='Number of tables unattended: '+str(data.tablesLeft), font='times 20 bold')
            canvas.create_text(data.width/2-267, data.height/2+120, text='Number of tables cleaned: '+str(data.tablesCleaned), font='times 20 bold')
            canvas.create_rectangle(data.width/2-400, data.height/2+200, data.width/2+400, data.height/2+205, fill='black')
            canvas.create_text(data.width/2-270, data.height/2+170, text='Number of wrong orders: '+str(data.wrongOrders), font='times 20 bold')
            canvas.create_text(data.width/2, data.height-100, text='Your Score:'+str(data.score), fill='black', font='arial 50 bold')
            while space<5:
                if space==0: 
                    points=-10
                    action=data.bumps
                elif space==1: 
                    points=50
                    action=data.tablesServed
                elif space==2:
                    points=-50
                    action=data.tablesLeft
                elif space==3: 
                    points=50
                    action=data.tablesCleaned
                elif space==4:
                    points=-20
                    action=data.wrongOrders
                canvas.create_text(data.width/2, data.height/2-30+50*space, text=str(points), font='times 20 bold')
                canvas.create_text(data.width/2+200, data.height/2-30+50*space, text='x'+str(data.Multiplier), font='times 20 bold')
                canvas.create_text(data.width/2+350, data.height/2-30+50*space, text=str(points*action*data.Multiplier), font='times 20 bold')
                space+=1
            if len(data.Leaderboard)<10 or data.score>data.Leaderboard[9][1]:
                canvas.create_text(data.width/2, data.height-40, text="Congratulations!\nYou're in the top 10!", font='times 25 italic bold')
                music=pygame.mixer.Sound('Applause.ogg')
                data.highScore=True
                if data.soundEffect==True:
                    music.play()
        else:
            canvas.create_text(data.width/2, 80, text='GAME OVER!', fill='white', font='arial 120 bold')
            canvas.create_text(data.width/2, 200, text='You Lost!', fill='white', font='arial 100 bold')
        canvas.create_rectangle(data.width, data.height, data.width-250, data.height-150, fill='orange red')
        canvas.create_text(data.width-125, data.height-75, text='Next', font='comic 60 bold')
####################################
# Do not edit code below here!
####################################

class Struct(object): pass

def run(width=300, height=300):
    def drawAllWrapper():
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, width, height, fill='white', width=0)
        drawAll(canvas, data)
        canvas.update()

    def callFn(fn, event=None):
        if (fn == 'mousePressed'): data._mouseIsPressed = True
        elif (fn == 'mouseReleased'): data._mouseIsPressed = False
        if ('mouse' in fn): data._lastMousePosn = (event.x, event.y)
        if (fn in globals()):
            if (fn.startswith('key')):
                c = event.key = event.char
                if ((c in [None, '']) or (len(c) > 1) or (ord(c) > 255)):
                    event.key = event.keysym
                elif (c == '\t'): event.key = 'Tab'
                elif (c in ['\n', '\r']): event.key = 'Enter'
                elif (c == '\b'): event.key = 'Backspace'
                elif (c == chr(127)): event.key = 'Delete'
                elif (c == chr(27)): event.key = 'Escape'
                elif (c == ' '): event.key = 'Space'
                if (event.key.startswith('Shift')): return
            args = [data] if (event == None) else [event, data]
            globals()[fn](*args)
            drawAllWrapper()

    def timerFiredWrapper():
        callFn('timerFired')
        data._afterId1 = root.after(data.timerDelay, timerFiredWrapper)

    def mouseMotionWrapper():
        if (((data._mouseIsPressed == False) and (data._mouseMovedDefined == True)) or
            ((data._mouseIsPressed == True ) and (data._mouseDragDefined == True))):
            event = Struct()
            event.x = root.winfo_pointerx() - root.winfo_rootx()
            event.y = root.winfo_pointery() - root.winfo_rooty()
            if ((data._lastMousePosn !=  (event.x, event.y)) and
                (event.x >= 0) and (event.x <= data.width) and
                (event.y >= 0) and (event.y <= data.height)):
                fn = 'mouseDragged' if (data._mouseIsPressed == True) else 'mouseMoved'
                callFn(fn, event)
        data._afterId2 = root.after(data.mouseMovedDelay, mouseMotionWrapper)

    # Set up data and call init
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    data.mouseMovedDelay = 50 # ditto
    data._mouseIsPressed = False
    data._lastMousePosn = (-1, -1)
    data._mouseMovedDefined = 'mouseMoved' in globals()
    data._mouseDragDefined = 'mouseDragged' in globals()
    data._afterId1 = data._afterId2 = None
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event: callFn('mousePressed', event))
    # root.bind("<B1-Motion>", lambda event: callFn('mouseDragged', event))
    root.bind("<B1-ButtonRelease>", lambda event: callFn('mouseReleased', event))
    root.bind("<Key>", lambda event: callFn('keyPressed', event))
    # initialize, start the timer, and launch the app
    callFn('init')
    if ('timerFired' in globals()): timerFiredWrapper()
    if (data._mouseMovedDefined or data._mouseDragDefined): mouseMotionWrapper()
    root.mainloop()  # blocks until window is closed
    if (data._afterId1): root.after_cancel(data._afterId1)
    if (data._afterId2): root.after_cancel(data._afterId2)
    print("bye!")

if __name__ == '__main__':
    run(1300, 700)