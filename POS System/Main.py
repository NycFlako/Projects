from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random, math, copy, time, pygame
pygame.mixer.init()

class EntryScreen(Mode):
    def appStarted(mode):
        mode.entryScreen = mode.loadImage('mainScreen.png')
        mode.entryScreen = mode.scaleImage(mode.entryScreen, 1.5)
        mode.entryScreen.cachedPhotoImage = ImageTk.PhotoImage(mode.entryScreen)
        (mode.characters, mode.counts) = mode.getCharacters()
        mode.difficulty, mode.settings, mode.stage = 'Easy', False, 0
        mode.getDifficultyCharacters()

    def getDifficultyCharacters(mode):
        if mode.difficulty == 'Easy':
            mode.charactersToDraw  = ['zombie', 'cerberus', 'main']
        elif mode.difficulty == 'Medium':
            mode.charactersToDraw  = ['military', 'medusa', 'main']
        else:
            mode.charactersToDraw  = ['ski', 'aneill', 'main']

    @staticmethod
    def getLeaderboard(mode):
        text = open("Leaderboard.txt", "r")
        scores = text.readlines()
        top10Scores = set()
        values = list()
        for entry in scores:
            person = list()
            if not entry[-1].isalnum():
                entry = entry[:-1]
            for detail in entry.split(','):
                if detail.isdigit():
                    top10Scores.add(int(detail))
                person.append(detail)
            values.append(person)
        top10 = sorted(list(top10Scores))
        top10.reverse()
        if len(top10) > 10: top10 = top10[:10]
        leaderboard = list()
        for i in range(len(top10)):
            score = top10[i]
            for person in values:
                if str(score) in person:
                    leaderboard.append((person[0],score))
                    if len(leaderboard) == 10:
                        return leaderboard
        return leaderboard

    def getCharacters(mode):
        d, count = dict(), dict()
        aneillStrip = mode.loadImage('Aneill.png')
        spriteStrip = mode.loadImage('Character.png')
        skiStrip = mode.loadImage('skiMask.png')
        militaryStrip = mode.loadImage('military.png')
        zombieStrip = mode.loadImage('zombie.png')
        cerbStrip = mode.loadImage('cerberus.png')
        medusaStrip = mode.loadImage('medusa.png')
        d['main'] = list()
        count['main'] = 0
        for i in range(9):
            sprite = spriteStrip.crop((43*i, 0, 43*(i+1), 61))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['main'].append(sprite)
        d['ski'] = list()
        count['ski'] = 0
        for i in range(2):
            sprite = skiStrip.crop((251,60*i, 291, 60*(i+1)))
            sprite = mode.scaleImage(sprite, 3)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for i in range(3):
                d['ski'].append(sprite)
        d['military'] = list()
        count['military'] = 0
        for i in range(2):
            sprite = militaryStrip.crop((308+170*i,656,308+170*(i+1),990))
            sprite = mode.scaleImage(sprite, .5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for i in range(3):
                d['military'].append(sprite)
        d['zombie'] = list()
        count['zombie'] = 0
        for i in range(3):
            sprite = zombieStrip.crop((85.2*i,0,85.2*(i+1),117))
            sprite = mode.scaleImage(sprite, 1.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for i in range(2):
                d['zombie'].append(sprite)
        d['aneill'] = list()
        count['aneill'] = 0
        for i in range(3):
            sprite = aneillStrip.crop((54*i,76, 54*(i+1), 150))
            sprite = mode.scaleImage(sprite, 3)
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for i in range(2):
                d['aneill'].append(sprite)
        d['cerberus'] = list()
        count['cerberus'] = 0
        for i in range(4):
            sprite = cerbStrip.crop((192+77*i, 0, 192+77*(i+1), 56))
            sprite = mode.scaleImage(sprite, 3)
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for _ in range(2):
                d['cerberus'].append(sprite)  
        d['medusa'] = list()
        count['medusa'] = 0 
        for i in range(5):
            sprite = medusaStrip.crop((57*i, 351, 57*(i+1),407+1*i))
            sprite = mode.scaleImage(sprite, 4)
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['medusa'].append(sprite)
        return (d, count)
        
    def drawCharacters(mode, canvas):
        if mode.difficulty == 'Easy':
            character = 'zombie'
            boss = 'cerberus'
        elif mode.difficulty == 'Medium':
            character = 'military'
            boss = 'medusa'
        else:
            character = 'ski'
            boss = 'aneill'
        cx, cy = mode.width/2, mode.height/2
        player = mode.characters['main'][mode.counts['main']]
        canvas.create_image(cx-220, cy+180, image = player.cachedPhotoImage)
        finalBoss = mode.characters[boss][mode.counts[boss]]
        if boss == 'cerberus':
            canvas.create_image(cx+405, cy+80, image = finalBoss.cachedPhotoImage)
        else: canvas.create_image(cx+405, cy+40, image = finalBoss.cachedPhotoImage)
        picture = mode.characters[character][mode.counts[character]]
        for i in range(2):
            canvas.create_image(cx+200, cy+140+140*i, image = picture.cachedPhotoImage)
            canvas.create_image(cx+100+200*i, cy+200, image = picture.cachedPhotoImage)
        canvas.create_image(cx, cy+140, image = picture.cachedPhotoImage)

    def timerFired(mode):
        for character in mode.counts:
            if character in mode.charactersToDraw:
                mode.counts[character] = (mode.counts[character]+1)%len(mode.characters[character])

    def createButtons(mode, canvas, cx, gap):
        buttons = [('Start Game','green'), ('Difficulty','orange'),
                    ('Leaderboard','purple'), ('Help','brown')]
        buttonW, buttonH = 100, 25
        for i in range(len(buttons)):
            value, buttonColor, cy = buttons[i][0],buttons[i][1], 150+gap*i
            style, color = 'times 30 bold', 'white'
            canvas.create_rectangle(cx-buttonW, cy-buttonH, cx+buttonW, cy+buttonH, fill=buttonColor)
            canvas.create_text(cx, cy, text = value, font = style, fill=color)

    def buttonAction(mode, y):
        if y <= 175 and y >= 125:
            mode.app.setActiveMode(mode.app.gameMode)
        elif y <= 250 and y >= 200:
            mode.settings = not mode.settings
        elif y <= 325 and y >= 275:
            mode.app.setActiveMode(mode.app.leaderboardMode)
        elif y <= 400 and y >= 350:
            mode.app.setActiveMode(HelpMode())

    def getSettingsOption(mode, x,y):
        if y >= 170 and y <= 210:
            if x >= 710 and x <= 763:
                mode.difficulty = 'Easy'
                mode.stage = 0
                mode.getDifficultyCharacters()
            elif x <= 816:
                mode.difficulty = 'Medium'
                mode.stage = 1
                mode.getDifficultyCharacters()
            elif x <= 870:
                mode.difficulty = 'Hard'
                mode.stage = 2
                mode.getDifficultyCharacters()

    def mousePressed(mode, event):
        if event.x >= 466 and event.x <= 666:
            mode.buttonAction(event.y)
        elif mode.settings:
            if event.x >= 710 and event.x <= 870:
                mode.getSettingsOption(event.x, event.y)

    def drawSettingsOptions(mode, canvas):
        canvas.create_polygon(666, 225, 690, 187.5, 690, 262.5, fill='white')
        canvas.create_rectangle(690, 125, 890, 325, fill='white', outline='')
        canvas.create_rectangle(700, 135, 880, 315, fill='black')
        mid = 700+(880-700)/2
        canvas.create_text(mid, 150, text = 'difficulty', font='times 20 italic', fill='white')
        difficulties = [('Easy','green'),('Medium','orange'),('Hard','red')]
        for i in range(len(difficulties)):
            difficulty, color = difficulties[i][0], difficulties[i][1]
            x0, y0, y1, gap  = 710, 170, 210, (870-710)/len(difficulties)
            canvas.create_rectangle(x0+gap*i, y0, x0+gap*(i+1), y1, fill=color)
            if difficulty == mode.difficulty:
                selectx0, selectx1 = x0+gap*i, x0+gap*(i+1)
            midx, midy =  x0+gap*i+gap/2, 190
            canvas.create_text(midx, midy, text = difficulty, font ='times 10 bold', fill='white')
        canvas.create_rectangle(selectx0, y0, selectx1, y1, fill='', outline='yellow', width=5)
        canvas.create_text(790, 260, text = mode.charactersToDraw[1], \
            font = 'times 30 italic bold', fill='blue')

    def redrawAll(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        canvas.create_rectangle(0,0,mode.width, mode.height, fill='black')
        canvas.create_text(cx-159, 50, text ='Beast Run!', font='times 50 italic bold', fill='red')
        canvas.create_image(cx, cy+30, image = mode.entryScreen.cachedPhotoImage)
        mode.createButtons(canvas, cx-159, 75)
        if mode.settings:
            mode.drawSettingsOptions(canvas)
        mode.drawCharacters(canvas)

class LeaderboardMode(Mode):
    def appStarted(mode):
        mode.background = mode.loadImage('Leaderboard.png')
        mode.background = mode.scaleImage(mode.background, 1.2)
        mode.background.cachedPhotoImage = ImageTk.PhotoImage(mode.background)
        oliveL = mode.loadImage('OliveBranch.png')
        oliveL.cachedPhotoImage = ImageTk.PhotoImage(oliveL)
        oliveR = mode.loadImage('OliveBranch2.png')
        oliveR.cachedPhotoImage = ImageTk.PhotoImage(oliveR)
        mode.olives = [oliveL, oliveR]
        mode.sound = pygame.mixer.Sound('Leaderboard.ogg')
        mode.sound.play()

    def keyPressed(mode, event):
        if event.key == 'up':
            mode.app.setActiveMode(mode.app.entryScreen)

    def drawNames(mode, canvas):
        cx, cy = mode.width/2+30, 230
        leaderboard = mode.app.entryScreen.getLeaderboard(mode)
        for i in range(len(leaderboard)):
            default, gapY, gapX = 'times 30 bold italic',45, 120
            if i < 3: color = 'gold'
            elif i < 5: color = 'silver'
            else: color = 'white'
            entry = leaderboard[i]
            canvas.create_text(cx-gapX, cy+gapY*i, text = str(i+1), font = default, fill=color)
            for j in range(len(entry)):
                value = entry[j]
                canvas.create_text(cx+gapX*j, cy+gapY*i, text =value, font =default, fill=color)

    def mousePressed(mode, event):
        x, y = event.x, event.y
        if x <= 850 and x >= 690 and y <= 800  and y >= 740:
            mode.sound.stop()
            mode.app.setActiveMode(mode.app.entryScreen)
        
    def redrawAll(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        canvas.create_rectangle(0,0,mode.width, mode.height, fill='purple')
        canvas.create_image(cx-200, cy, image = mode.background.cachedPhotoImage)
        canvas.create_image(cx+300, cy, image = mode.background.cachedPhotoImage)
        for i in range(len(mode.olives)):
            picture = mode.olives[i].cachedPhotoImage
            canvas.create_image(cx-200+500*i, cy, image = picture)
        canvas.create_text(cx+50, 160, text = 'Leaderboard', font ='times 40 italic bold underline', fill='black')
        mode.drawNames(canvas)
        w,h = 80, 30
        cx, cy =cx+50, mode.height-80
        canvas.create_rectangle(cx-w, cy-h, cx+w, cy+h, fill='black')
        w,h = w-5, h-5
        canvas.create_rectangle(cx-w, cy-h, cx+w, cy+h, fill='purple')
        canvas.create_text(cx, cy, text = 'Main Screen', font = 'times 25 italic bold', fill='black')

class HelpMode(Mode):
    def appStarted(mode):
        mode.page = 0
        (mode.backgrounds, mode.platforms) = mode.getBackgroundImages()
        mode.background, mode.platform = mode.backgrounds[0], mode.platforms[0]
        mode.userInterface = mode.app.gameMode.getUIImages(mode)
        mode.count = 0
        mode.score = 0
        mode.pageSoundEffect = pygame.mixer.Sound('Tutorial SF.ogg')
        mode.player1 = Player(mode)
        mode.player = mode.app.entryScreen.characters['main']

    def getBackgroundImages(mode):
        backgrounds, platforms = list(), list()
        images = [('sky.jpg','platform.png'), ('medusaBackground.png','forestPlatform.png')]
        for (link, platform) in images:
            Platform = mode.loadImage(platform)
            if platform == 'forestPlatform.png':
                Platform = mode.scaleImage(Platform, 2)
            Platform.cachedPhotoImage = ImageTk.PhotoImage(Platform)
            File = mode.loadImage(link)
            File = mode.scaleImage(File, 2)
            File.cachedPhotoImage = ImageTk.PhotoImage(File)
            platforms.append(Platform)
            backgrounds.append(File)
        return (backgrounds, platforms)

    def keyPressed(mode, event):
        if event.key == 'Right':
            mode.pageSoundEffect.play()
            mode.page += 1
            if mode.page > 11:
                mode.app.setActiveMode(mode.app.entryScreen)
        elif event.key == 'Left' and mode.page > 0:
            mode.pageSoundEffect.play()
            mode.page -= 1

    def timerFired(mode):
        mode.count = (mode.count+1)%len(mode.player)

    def drawMessages(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        default = 'times 20 bold'
        if mode.page == 0:
            message = '''Press the right key to go to the next page
and the left arrow key to go to the previous page'''
            canvas.create_text(cx, 150, text = 'Welcome to Beast Run', font = 'times 50 bold')
        elif mode.page == 1:
            message = '''At the top left corner you can see your health and special bars,
aswell as your lives, and the items you have in your storage'''
        elif mode.page == 2:
            message = '''At the top of the screen you can see your score, score is based on:
obstacles avoided, enemies killed and enemies avoided'''
        elif mode.page == 3:
            message = '''At the beginning of the game you will start in a running stage 
make it through the running stage in order to get to the battle arena
press 'Space' for your character to jump over the obstacles'''
        elif mode.page == 4: 
            mode.background = mode.backgrounds[0]
            mode.platform = mode.platforms[0]
            message = ''' Press "Space" while in the running arena to jump'''
        elif mode.page == 5:
            mode.background = mode.backgrounds[1]
            mode.platform = mode.platforms[1]
            message = '''This is the battle arena, in here you will battle a ton of enemies
plust a final boss at the end of it.'''
        elif mode.page == 6:
            message = '''While in the battle arena you can press "D" to attack in the front,
you can press "A" to attack behind you, or you can press "Enter" to make a special attack'''
        elif mode.page == 7:
            message = '''If your special bar is full you can press "S" to fully power
your character, allowing you to make unlimited special attacks'''
        elif mode.page == 8:
            message = '''You can use the items in your storage to grant you extra support
press 1 for the left most item, 2 for the middle one and 3 for the one on the right'''
        elif mode.page == 9:
            message = '''The heart grants you a life, the "+" symbol fills your health,
the snail shell grants you a temporary shield, and the special icon powers you up'''
        elif mode.page == 10:
            message = '''Each difficulty has its own battle arena and boss, try them all out!'''
        elif mode.page == 11:
            message = '''Have Fun and enjoy the game!!!
Press the right arrow key to go back to the main screen'''
        canvas.create_text(cx, cy, text = message, font = default)

    def drawPlatform(mode, canvas):
        if mode.page >= 5:
            for i in range(4):
                cx = mode.width//3
                canvas.create_image(cx*i, mode.height-30, image = mode.platform.cachedPhotoImage)
        else:
            cx = mode.width/2
            canvas.create_image(cx, mode.height, image = mode.platform.cachedPhotoImage)

    def redrawAll(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        canvas.create_image(cx, cy-100, image = mode.background.cachedPhotoImage)
        mode.drawPlatform(canvas)
        player = mode.player[mode.count]
        canvas.create_image(cx-200, mode.height-160, image = player.cachedPhotoImage)
        mode.drawMessages(canvas)
        if mode.page < 11:
            mode.app.gameMode.drawUI(mode, canvas)

################### SinglePlayerMode Functions #####################    
class GameMode(Mode):
    def appStarted(mode):
        mode.player1 = Player(mode)
        mode.stage, mode.difficulty = mode.app.entryScreen.stage, mode.app.entryScreen.difficulty
        mode.loadCharacter(mode.player1.moves)
        mode.background = {'sky': list(), 'platform': list()}
        mode.playerStatus = mode.loadPlayerStatus()
        mode.powerUps = mode.loadPowerUpImages()
        backgrounds = ['sky.jpg', 'transitionSky.jpg', 'darkSky.jpg']
        mode.lightning = mode.loadImage('lightning.png')
        mode.lightning.cachedPhotoImage = ImageTk.PhotoImage(mode.lightning)
        mode.countdownSound = False
        mode.countdown = mode.getCountdown()
        mode.userInterface = mode.getUIImages(mode)
        mode.score, mode.startup = 0, 0
        mode.obstaclesList = list()
        mode.thunderSound = pygame.mixer.Sound('Thunder.ogg')
        for background in backgrounds:
            mode.getBackgrounds(mode.background, background)
        mode.getPlatforms(mode.background, 'platform.png')
        mode.screenRoller, mode.platformScroller = 0, 0
        mode.obstacles = mode.getObstacles()
        mode.transition = False
        mode.cooldown = 0

    def loadPlayerStatus(mode):
        d = dict()
        shield = mode.loadImage('shield.png')
        shield = mode.scaleImage(shield, .35)
        shield.cachedPhotoImage = ImageTk.PhotoImage(shield)
        powered = mode.loadImage('superReady.png')
        powered = mode.scaleImage(powered, .75)
        powered1 = mode.scaleImage(powered, 1.05)
        powered2 = mode.scaleImage(powered, 1.1)
        powered.cachedPhotoImage = ImageTk.PhotoImage(powered)
        powered1.cachedPhotoImage = ImageTk.PhotoImage(powered1)
        powered2.cachedPhotoImage = ImageTk.PhotoImage(powered2)
        d['powered'] = [powered, powered1, powered2, powered1, powered]
        d['shield'] = shield
        return d

    def mousePressed(mode, event):
        mode.app.setActiveMode(mode.app.battleArena)
    
    def getCountdown(mode):
        L = list()
        numbers =['number 3.png', 'number 2.png', 'number 1.png', 'Go.png']
        for link in numbers:
            number = mode.loadImage(link)
            number = mode.scaleImage(number, .4)
            L.append(number)
        return L

    @staticmethod
    def getUIImages(mode):
        d = dict()
        life = mode.loadImage('characterFace.png')
        life = mode.scaleImage(life, 2)
        life.cachedPhotoImage = ImageTk.PhotoImage(life)
        d['lifeSymbol'] = life
        return d

    def loadPowerUpImages(mode):
        d = dict()
        spriteStrip = mode.loadImage('powerUps.png')
        health = spriteStrip.crop((100, 192, 125, 224))
        health = mode.scaleImage(health, 1.8)
        health.cachedPhotoImage = ImageTk.PhotoImage(health)
        powerUp = spriteStrip.crop((63, 164 ,96 , 192))
        powerUp = mode.scaleImage(powerUp, 1.8)
        powerUp.cachedPhotoImage = ImageTk.PhotoImage(powerUp)
        life = spriteStrip.crop((130, 194, 160, 220))
        life = mode.scaleImage(life, 1.8)
        life.cachedPhotoImage = ImageTk.PhotoImage(life)
        shield = spriteStrip.crop((162, 65, 190, 92))
        shield = mode.scaleImage(shield, 1.8)
        shield.cachedPhotoImage = ImageTk.PhotoImage(shield)
        d['life'] = life
        d['health'] = health
        d['powerUp'] = powerUp
        d['shield'] = shield
        return d

    def getObstacles(mode):
        d = dict()
        spriteStrip = mode.loadImage('obstacles.png')
        flames = spriteStrip.crop((733, 52, 866, 166))
        flames = mode.scaleImage(flames, .7)
        flames.cachedPhotoImage = ImageTk.PhotoImage(flames)
        d['flames'] = flames
        missile = spriteStrip.crop((193, 2, 316, 72))
        missile = mode.scaleImage(missile, .5)
        missile.cachedPhotoImage = ImageTk.PhotoImage(missile)
        d['missile'] = missile
        return d

    def getBackgrounds(mode, d, link):
        image = mode.loadImage(link)
        image = mode.scaleImage(image, 2)
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
        d['sky'].append(image)
        
    def getPlatforms(mode, d, link):
        image = mode.loadImage('platform.png')
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
        d['platform'] = image

    def loadCharacter(mode, d):
        counts = dict()
        spriteStrip = mode.loadImage('Character.png')
        d['jumping'] = list()
        counts['jumping'] = 0
        for i in range(5):
            if i == 1 or i == 2:
                x1, x2 = .6, 1.4
            elif i == 3:
                x1, x2 = 6, 4
            else:
                x1, x2 = 7, 1.4
            sprite = spriteStrip.crop((410 + x1+50*i, 0, 410+x2+50*(i+1), 61))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['jumping'].append(sprite)
            d['jumping'].append(sprite)
        d['running'] = list()
        counts['running'] = 0
        for i in range(8):
            #get the jumping sprite from running
            if i == 1 or i == 2:
                x1, x2 = .6, 1.4
            elif i == 3 or i == 7:
                x1, x2 = 6, 4
            else:
                x1, x2 = 7, 1.4
            sprite = spriteStrip.crop((410 + x1+50*i, 0, 410+x2+50*(i+1), 61))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['running'].append(sprite)
        d['standing'] = list()
        counts['standing'] = 0
        for i in range(9):
            sprite = spriteStrip.crop((43*i, 0, 43*(i+1), 61))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['standing'].append(sprite)
        d['styling'] = list()
        counts['styling'] = 0
        for i in range(6):
            sprite = spriteStrip.crop((49*i, 61, 49*(i+1), 122))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['styling'].append(sprite)
        for i in range(9):
            sprite = spriteStrip.crop((309+61*i, 61, 309+61*(i+1), 122))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['styling'].append(sprite)
        d['onGuard'] = list()
        counts['onGuard'] = 0
        for i in range(5):
            sprite = spriteStrip.crop((61*i, 123, 60*(i+1), 184))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['onGuard'].append(sprite)
        d['threat'] = list()
        counts['threat'] = 0
        for i in range(5):
            sprite = spriteStrip.crop((310+55*i, 123, 315+52*(i+1), 190))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['threat'].append(sprite)
        d['enraged'] = list()
        counts['enraged'] = 0
        for i in range(6):
            if i < 2:
                sprite = spriteStrip.crop((595+54*i, 123, 595+49*(i+1), 190))
            elif i == 2:
                sprite = spriteStrip.crop((585+56*i, 123, 595+54*(i+1), 190))
            else:
                sprite = spriteStrip.crop((595+56*i, 123, 595+56*(i+1), 190))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for i in range(3):
                d['enraged'].append(sprite)
        d['dancing'] = list()
        counts['dancing'] = 0
        for i in range(4):
            sprite = spriteStrip.crop((400+51*i, 190, 400+51*(i+1), 258))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['dancing'].append(sprite)
        d['celebrating'] = list()
        counts['celebrating'] = 0
        for i in range(8):
            if i < 3:
                sprite = spriteStrip.crop((50*i, 188.5, 50*(i+1), 258))
            else:
                sprite = spriteStrip.crop((40+40*i, 188.5, 40+39.8*(i+1), 258))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['celebrating'].append(sprite)
        d['backAttack'] = list()
        counts['backAttack'] = 0
        for i in range(6):
            if i < 4:
                sprite = spriteStrip.crop((620+50*i, 188.5, 620+50.2*(i+1), 258))
            else:
                sprite = spriteStrip.crop((627+50.5*i, 188.5, 627+50*(i+1), 258))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['backAttack'].append(sprite)
        d['frontAttack'] = list()
        counts['frontAttack'] = 0
        for i in range(6):
            if i < 3:
                sprite = spriteStrip.crop((60*i, 285, 59*(i+1), 343))
            else:
                sprite = spriteStrip.crop((65*i-3, 285, 65*(i+1)-3, 343))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            d['frontAttack'].append(sprite)
        d['smash'] = list()
        counts['smash'] = 0
        for i in range(5):
            if i < 2:
                sprite = spriteStrip.crop((405+60*i, 260, 405+60*(i+1), 340))
            else:
                sprite = spriteStrip.crop((310+110*i, 258, 310+110*(i+1), 340))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for _ in range(2):
                d['smash'].append(sprite)
        d['special'] = list()
        counts['special'] = 0
        for i in range(4):
            if i < 3:
                sprite = spriteStrip.crop((52*i, 340, 53*(i+1),403))
            else:
                sprite = spriteStrip.crop((54*i, 340, 63*(i+1),403))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            for i in range(2):
                d['special'].append(sprite)
        backToPosition = list()

        for i in range(4):
            if i < 2:
                sprite = spriteStrip.crop((370+72*i, 342, 370+72*(i+1), 403))
            else:
                sprite = spriteStrip.crop((387+65*i, 342, 387+65*(i+1), 403))
            sprite = mode.scaleImage(sprite, 2.5)
            sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
            backToPosition.append(sprite)
        d['special'].extend(backToPosition)
        projectile = mode.loadImage('Projectile.png')
        projectile = mode.scaleImage(projectile, 2)
        projectile.cachedPhotoImage = ImageTk.PhotoImage(projectile)
        d['projectile'] = projectile

    def drawTransitionEffect(mode, canvas):
        if mode.player1.cx >= mode.width:
            overX = (mode.width-(mode.player1.cx - mode.width))*2
            overY = (mode.player1.cx - mode.width)*2
            canvas.create_rectangle(mode.width, 0, overX, overY, fill='black' )

    def makeJump(mode):
        midpoint = len(mode.player1.moves['jumping'])/2
        if mode.player1.spriteCount <= midpoint: 
            mode.player1.cy -= 60
        else:
            mode.player1.cy += 60
        if mode.player1.spriteCount == len(mode.player1.moves['jumping'])-1:
            mode.player1.cy, mode.player1.action = mode.height-178, 'running'
            mode.player1.spriteCount = 0
    
    def updatePlayer(mode, player, action):
        lengthOfSprites = len(player.moves[action])
        player.spriteCount = (player.spriteCount+1)%lengthOfSprites 
        if action == 'jumping':
            mode.makeJump()   

    def createObstacles(mode):
        if not mode.transition:
            choices = list()
            for obstacle in mode.obstacles:
                choices.append(obstacle)
            if mode.difficulty == 'Easy': interval = 30
            elif mode.difficulty == 'Medium': interval = 25
            else: interval = 20
            guess = random.randint(0,interval)
            mode.cooldown += 1
            if mode.cooldown == interval or (guess == 7 and mode.cooldown > 7):
                kind = random.choice(choices)
                newObstacle = Obstacle(kind, mode.width, mode.height-178)
                mode.obstaclesList.append(newObstacle)
                mode.cooldown = 0

    def checkForInteractions(mode):
        if mode.player1.status == 'newLife' or mode.player1.status == 'shield':
            return None
        for item in mode.obstaclesList:
            if item.name == 'flames':
                if item.cx <=  mode.player1.cx+40 and item.cx >= mode.player1.cx-40:
                    if mode.player1.cy+80 >= item.cy-25:
                        mode.score -= 500
                        mode.player1.lives -= 1
                        if mode.player1.lives < 0:
                            mode.app.setActiveMode(mode.app.gameoverMode)
                        mode.player1.cy = mode.height-178
                        mode.player1.status, mode.startup = 'newLife', 0
                        mode.player1.action ='enraged'
                        return item
            elif item.name == 'missile':
                if item.cx-25 <= mode.player1.cx+40 and item.cx+25 >= mode.player1.cx-40:
                    if mode.player1.cy+80 >= item.cy-15:
                        mode.score -= 1000
                        mode.player1.lives -= 1
                        if mode.player1.lives < 0:
                            mode.app.setActiveMode(mode.app.gameoverMode)
                        mode.player1.cy = mode.height-178
                        mode.player1.status, mode.startup = 'newLife', 0
                        mode.player1.action = 'enraged'
                        return item
        return None

    @staticmethod
    def removeItems(mode, items, L):
        for item in items:
            L.remove(item)
    
    def removeObstacles(mode):
        toRemove = set()
        for obstacle in mode.obstaclesList:
            obstacle.cx -= 40
            if obstacle.cx <= 0:
                mode.score += 100
                toRemove.add(obstacle)
        interaction = mode.checkForInteractions()
        if interaction != None:
            toRemove.add(interaction)
        mode.removeItems(mode, toRemove, mode.obstaclesList)

    def drawBackgrounds(mode, canvas, d):
        cx, cy = mode.width/2, mode.height/2
        background = d['sky'][mode.stage].cachedPhotoImage
        roller = mode.screenRoller
        canvas.create_image(roller+2640, 3*cy/4, image = background)

    def drawPlatforms(mode, canvas, d):
        cx, cy = mode.width/2, mode.height/2
        platform = d['platform'].cachedPhotoImage
        roller = mode.platformScroller
        for i in range(2):
            canvas.create_image(cx*(i+1)+roller, mode.height, image = platform)

    def drawRandomLightning(mode, canvas):
        possibility = random.randint(0,60)
        if possibility == 7:
            mode.thunderSound.play()
            randomX, cy = random.randint(0,mode.width), mode.height/2
            canvas.create_image(randomX, cy, image = mode.lightning.cachedPhotoImage)
        
    def entryEffect(mode):
        mode.startup += 1
        if mode.startup == 48:
            mode.player1.action = 'styling'
        elif mode.startup == 64:
            mode.player1.status = None
            mode.player1.action, mode.player1.spriteCount ='running', 0

    def timerFired(mode):
        mode.updatePlayer(mode.player1, mode.player1.action)
        if mode.startup < 64:
            mode.entryEffect()
        else:
            if 3090+mode.screenRoller >= mode.width:
                mode.screenRoller -= 5
                mode.platformScroller -= 40
                mode.score += 10
            else:
                mode.transition = True
                mode.player1.cx += 40
                if mode.player1.cx > 2.1*mode.width:
                    mode.app.setActiveMode(mode.app.battleArena)
            if abs(mode.platformScroller) >= mode.width/2:
                mode.platformScroller = 0
            mode.createObstacles()
            mode.removeObstacles()

    @staticmethod
    def drawUI(mode, canvas):
        gap = 0
        cx, cy = mode.width - 200, 50
        canvas.create_text(mode.width/2, cy, text =f'Score: {mode.score}', font='times 26 italic bold')
        for key in mode.userInterface:
            symbol = mode.userInterface[key].cachedPhotoImage
            if key == 'lifeSymbol':
                for i in range(mode.player1.lives):
                    canvas.create_image(50 + 70*i, cy, image = symbol)
            else:
                canvas.create_image(cx+gap, cy,  image = symbol)
                gap += 75
        # Draw Special Bar
        canvas.create_rectangle(22, 80,22+mode.player1.special,100, fill='yellow')
        canvas.create_rectangle(22, 80, 122, 100, fill='', outline ='black', width=5)
        canvas.create_text(77, 90, text = f'{mode.player1.special}%', font = 'arial 12 bold')
        # Draw Health Bar
        canvas.create_rectangle(22,110,22+mode.player1.health,130, fill='red')
        canvas.create_rectangle(22, 110, 122, 130, fill='', outline ='black', width=5)
        canvas.create_text(77, 120, text = f'{mode.player1.health}%', font = 'arial 12 bold')
        # Draw Storage
        for i in range(3):
            gapX, gapY = 50, 50 
            canvas.create_rectangle(170+gapX*i, 25, 170+gapX*(i+1), 25+gapY, fill='grey', outline ='black', width = 5)
        for i in range(len(mode.player1.storage)):
            item = mode.player1.storage[i]
            picture = mode.powerUps[item].cachedPhotoImage
            canvas.create_image(195+50*i, 50, image = picture)

    def drawPlayer(mode, canvas, player):
        action = player.action
        if player.status != None and player.status != 'newLife':
            status = player.status
            sprite = mode.powerUps[status].cachedPhotoImage
            canvas.create_image(player.cx, player.cy, image = sprite)
            return
        elif player.status == 'newLife':
            if mode.startup%2 == 0:
                sprite = player.moves[player.action][player.spriteCount].cachedPhotoImage
                canvas.create_image(player.cx, player.cy, image = sprite)
        else:
            sprite = player.moves[action][player.spriteCount].cachedPhotoImage
            canvas.create_image(player.cx, player.cy, image = sprite) 
    
    def drawCountdownEffect(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        index = mode.startup//18
        picture = mode.scaleImage(mode.countdown[index], 1/(mode.startup%18+1))
        picture = ImageTk.PhotoImage(picture)
        canvas.create_image(cx, cy, image = picture)

    def countDownEffect(mode, canvas):
        if mode.startup < 64:
            if not mode.countdownSound:
                pygame.mixer.music.load('countdown.mp3')
                pygame.mixer.music.play()
                mode.countdownSound = True
            mode.drawCountdownEffect(canvas)
        elif mode.countdownSound:
            pygame.mixer.music.load('mainMusic.mp3')
            pygame.mixer.music.play()
            mode.countdownSound = False

    def drawObstacles(mode, canvas):
        for obstacle in mode.obstaclesList:
            picture = mode.obstacles[obstacle.name].cachedPhotoImage
            cx, cy = obstacle.cx, obstacle.cy
            if obstacle.name == 'flames':
                canvas.create_image(cx, cy+25, image = picture)
            else:
                canvas.create_image(cx, cy, image = picture)
        
    def redrawAll(mode, canvas):
        mode.drawBackgrounds(canvas, mode.background)
        mode.drawRandomLightning(canvas)
        mode.countDownEffect(canvas)
        mode.drawPlatforms(canvas, mode.background)
        mode.drawUI(mode, canvas)
        mode.drawPlayer(canvas, mode.player1)
        mode.drawObstacles(canvas)
        mode.drawTransitionEffect(canvas)
        
    def keyPressed(mode, event):
        if mode.startup == 64:
            if event.key == 'Space' and mode.player1.action != 'jumping':
                mode.player1.action = 'jumping'
                mode.player1.spriteCount = 0
            else:
                mode.app.timerDelay = 100

class BattleArenaMode(Mode):
    def appStarted(mode):
        mode.stage = mode.app.gameMode.stage
        mode.player1 = mode.getPlayerInfo()
        mode.difficulty = mode.app.gameMode.difficulty
        mode.getStageInfo()
        mode.playerStatus = mode.app.gameMode.playerStatus
        mode.powerUps = mode.app.gameMode.powerUps
        mode.userInterface = mode.app.gameMode.userInterface
        mode.score = mode.app.gameMode.score
        mode.enemies = copy.deepcopy(mode.app.entryScreen.characters)
        mode.enemiesCounts = mode.app.entryScreen.counts
        mode.flipEnemies(mode.enemies)
        mode.playerStatus = mode.app.gameMode.playerStatus
        mode.poweredCount, mode.bossOnStage, mode.enemyCreatedTime = 0, 0, 0
        mode.resizeCharacters()
        mode.powerUpCount = 0
        mode.createObjectLists()
        mode.shieldTime = 30
        pygame.mixer.music.load('finalBossMusic.mp3')
        pygame.mixer.music.play()

    def createObjectLists(mode):
        mode.powerUpList = list()
        mode.enemiesList = list()
        mode.projectileList = list()

    def loadBosses(mode, boss):
        if boss == 'cerberus':
            boss = dict()
            cerbStrip = mode.loadImage('cerberus.png')
            boss['attacking'] = list()
            boss['count'] = 0
            for i in range(6):
                sprite = cerbStrip.crop((52+73*i, 198,52+73*(i+1),260))
                sprite = mode.scaleImage(sprite, 3)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                boss['attacking'].append(sprite)
            boss['standing'] = list()
            for i in range(4):
                sprite = cerbStrip.crop((192+77*i, 0, 192+77*(i+1), 56))
                sprite = mode.scaleImage(sprite, 3)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                for _ in range(2):
                    boss['standing'].append(sprite)
            boss['moving'] = list()
            for i in range(6):
                if i == 0:
                    sprite = cerbStrip.crop((82, 140, 148, 198))
                elif i == 1:
                    sprite = cerbStrip.crop((262, 262, 344, 330))
                elif i == 2:
                    sprite = cerbStrip.crop((412, 62, 494, 112))
                elif i == 3:
                    sprite = cerbStrip.crop((317, 60, 403, 106))
                elif i == 4:
                    sprite = cerbStrip.crop((152, 136, 218, 200))
                else:
                    sprite = cerbStrip.crop((82, 141, 148, 198))
                sprite = mode.scaleImage(sprite, 3)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                boss['moving'].append(sprite)
        elif boss == 'medusa':
            boss = dict()
            medusaStrip = mode.loadImage('medusa.png')
            boss['moving'] = list()
            boss['count'] = 0
            for i in range(2):
                sprite = medusaStrip.crop((62*i,415,62*(i+1),468))
                sprite = mode.scaleImage(sprite, 4)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                for _ in range(3):
                    boss['moving'].append(sprite)
            boss['standing'] = list()
            for i in range(5):
                sprite = medusaStrip.crop((57*i, 351, 57*(i+1),407+1*i))
                sprite = mode.scaleImage(sprite, 4)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                boss['standing'].append(sprite)
            boss['attacking'] = list()
            for i in range(2):
                if i == 0:
                    sprite = medusaStrip.crop((383, 250,444,308))
                else:
                    sprite = medusaStrip.crop((297,247,380,306))
                sprite = mode.scaleImage(sprite, 4)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                for _ in range(2):
                    boss['attacking'].append(sprite)
        else:
            boss = dict()
            aneillStrip = mode.loadImage('Aneill.png')
            boss['standing'] = list()
            boss['count'] = 0
            for i in range(3):
                sprite = aneillStrip.crop((54*i,76, 54*(i+1), 150))
                sprite = mode.scaleImage(sprite, 3)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                for i in range(2):
                    boss['standing'].append(sprite)
            boss['moving'] = list()
            for i in range(8):
                if i < 2:
                    sprite = aneillStrip.crop((57*i,237,57*(i+1), 295))
                elif i < 4:
                    sprite = aneillStrip.crop((62*i,237,63*(i+1), 295))
                elif i < 7:
                    sprite = aneillStrip.crop((65*i,237,66*(i+1), 295))
                else:
                    sprite = aneillStrip.crop((66*i,237,66*(i+1), 295))
                sprite = mode.scaleImage(sprite, 3)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                boss['moving'].append(sprite)
            boss['attacking'] = list()
            for i in range(5):
                if i < 2:
                    sprite = aneillStrip.crop((58*i,392,58*(i+1), 460))
                elif i == 2:
                    sprite = aneillStrip.crop((59*i,392,61*(i+1), 460))
                elif i == 3:
                    sprite = aneillStrip.crop((62*i,392,61*(i+1), 460))
                else:
                    sprite = aneillStrip.crop((62*i,392,65*(i+1), 460))
                sprite = mode.scaleImage(sprite, 3)
                sprite.cachedPhotoImage = ImageTk.PhotoImage(sprite)
                boss['attacking'].append(sprite)
        return boss

    def getDifficultyInfo(mode):
        if mode.difficulty == 'Easy':
            mode.mainEnemies('zombie')
        elif mode.difficulty == 'Medium':
            mode.mainEnemies('military')
        else:
            mode.mainEnemies('ski')
        
    def getStageInfo(mode):
        if mode.stage == 0:
            mode.background = mode.loadImage('forest.jpg')
            mode.platform = mode.loadImage('forestPlatform.png')
            mode.boss = 'cerberus'
        elif mode.stage == 1:
            mode.background = mode.loadImage('medusaBackground.png')
            mode.platform = mode.loadImage('medusaPlatform.png')
            mode.boss = 'medusa'
        elif mode.stage == 2:
            mode.background = mode.loadImage('aneillBackground.jpg')
            mode.platform = mode.loadImage('aneillPlatform.png')
            mode.boss = 'aneill'
        mode.background.cachedPhotoImage = ImageTk.PhotoImage(mode.background)
        mode.platform.cachedPhotoImage = ImageTk.PhotoImage(mode.platform)
    
    def getPlayerInfo(mode):
        player = mode.app.gameMode.player1
        player.cx, player.cy = mode.width/2, mode.height-125
        player.action = 'standing'
        mode.flipPlayerMoves(player)
        return player
        
    def mainEnemies(mode, toStay):
        for enemy in mode.enemies:
            if enemy != toStay: 
                mode.enemies.pop(character)
        
    def resizeCharacters(mode):
        for move in mode.player1.moves:
            images = mode.player1.moves[move]
            if type(images) != list:
                image = mode.scaleImage(images, .7)
                image.cachedPhotoImage = ImageTk.PhotoImage(image)
                mode.player1.moves[move] = image
            else:
                for i in range(len(images)):
                    image = images[i]
                    image = mode.scaleImage(image, .7)
                    image.cachedPhotoImage = ImageTk.PhotoImage(image)
                    images[i] = image
        for enemy in mode.enemies:
            images = mode.enemies[enemy]
            for i in range(len(images)):
                image = images[i]
                image = mode.scaleImage(image, .7)
                image.cachedPhotoImage = ImageTk.PhotoImage(image)
                images[i] = image
        for status in mode.playerStatus:
            images = mode.playerStatus[status]
            if type(images) != list:
                image = mode.scaleImage(images, .7)
                image.cachedPhotoImage = ImageTk.PhotoImage(image)
                mode.playerStatus[status] = image
            else:
                for i in range(len(images)):
                    image = images[i]
                    image = mode.scaleImage(image, .7)
                    image.cachedPhotoImage = ImageTk.PhotoImage(image)
                    images[i] = image

    def updateSprites(mode, player, action):
        lengthOfSprites = len(player.moves[action])
        player.spriteCount = (player.spriteCount+1)%lengthOfSprites
        for enemy in mode.enemiesList:
            length = len(mode.enemies[enemy.kind])
            mode.enemiesCounts[enemy.kind] = (mode.enemiesCounts[enemy.kind]+1)%length
            mode.enemiesCounts[enemy.kind+'R'] = (mode.enemiesCounts[enemy.kind]+1)%length
    def makePlayerMove(mode, player, action):
        toRemove = set()
        if 'running' in action:
            if player.position == 'L' and player.cx > 0:
                player.cx -= 20
            elif player.cx < mode.width:
                player.cx += 20
        elif 'special' in action:
            if player.spriteCount == 8:
                projectile = Obstacle('projectile', player.cx+5, player.cy)
                projectile.position = player.position
                mode.projectileList.append(projectile)
                if player.position =='R': player.action = 'standing'
                else: player.action = 'standingL'
                player.spriteCount = 0

    def checkForMissileInteraction(mode):
        for projectile in mode.projectileList:
            if type(mode.bossOnStage) != int:
                if projectile.position == 'R':
                    if projectile.cx+38 >= mode.boss.cx-95 and projectile.cx-38 <= mode.boss.cx+95:
                        mode.boss.health -= 10
                        if mode.boss.health < 1:
                            mode.app.setActiveMode(mode.app.stagecleared)
                        return (projectile, None)
                else:
                    if projectile.cx-38 <= mode.boss.cx+95 and projectile.cx+38 >= mode.boss.cx-95:
                        mode.boss.health -= 10
                        if mode.boss.health < 1:
                            mode.app.setActiveMode(mode.app.stagecleared)
                        return (projectile, None)
            for enemy in mode.enemiesList:
                if projectile.position == 'R':
                    if projectile.cx+38 >= enemy.cx-20 and projectile.cx-38 <= enemy.cx+20:
                        return (projectile, enemy)
                else:
                    if projectile.cx-38 <= enemy.cx+20 and projectile.cx+38 >= enemy.cx-20:
                        return (projectile, enemy)
    
    def moveProjectile(mode, projectile):
        toRemove = set()
        if projectile.position == 'R':
            projectile.cx += 40
        else:
            projectile.cx -= 40
        if projectile.cx > mode.width or projectile.cx < 0:
            toRemove.add(projectile)
        projectileHit = mode.checkForMissileInteraction()
        if projectileHit != None:
            toRemove.add(projectileHit[0])
            if mode.player1.special < 100: 
                mode.player1.special += 1
                mode.score += 50
            if projectileHit[1] != None:
                mode.app.gameMode.removeItems(mode, set([projectileHit[1]]), mode.enemiesList)
        mode.app.gameMode.removeItems(mode, toRemove, mode.projectileList)

    def moveObjects(mode):
        for projectile in mode.projectileList:
            mode.moveProjectile(projectile)

    def updateEnemies(mode):
        if len(mode.enemiesList) != 0:
            for enemy in mode.enemiesList:
                if enemy.cx >= mode.player1.cx:
                    enemy.position = 'L'
                else:
                    enemy.position = 'R'

    def checkForAttackInteraction(mode, enemy):
        player = mode.player1
        if 'Attack' in player.action:
            if type(mode.bossOnStage) != int and mode.boss.gotHit == 0:
                if abs(mode.boss.cx-mode.player1.cx) < 140:
                    mode.boss.health -= 5
                    mode.boss.gotHit = 10
                    if mode.boss.health < 1:
                        mode.app.setActiveMode(mode.app.stagecleared)
            if 'frontAttack' in player.action:
                if player.position == 'R' and enemy.position =='L':
                    if enemy.cx-20 <= player.cx+55:
                        return enemy
                elif player.position == 'L' and enemy.position == 'R':
                    if enemy.cx+20 >= player.cx-55:
                        return enemy
            else:
                if player.spriteCount >= 4:
                    if player.position == enemy.position:
                        if player.position == 'R':
                            if player.cx-40 <= enemy.cx+20:
                                return enemy
                        else:
                            if player.cx+40 >= enemy.cx-20:
                                return enemy

    def moveEnemies(mode):
        if len(mode.enemiesList) != 0:
            toRemove = set()
            for enemy in mode.enemiesList:
                if enemy.position == 'R':
                    if mode.player1.cx-enemy.cx>40:
                        enemy.cx += enemy.speed
                else:
                    if enemy.cx-mode.player1.cx>40:
                        enemy.cx -= enemy.speed
                enemyHit = mode.checkForAttackInteraction(enemy)
                if enemyHit != None:
                    if mode.player1.special < 100: 
                        mode.player1.special += 5
                        mode.score += 100
                    toRemove.add(enemyHit)
            mode.app.gameMode.removeItems(mode, toRemove, mode.enemiesList)

    def newLifeEffect(mode):
        player = mode.player1
        player.lives -= 1
        if player.lives < 0:
            mode.app.setActiveMode(mode.app.gameoverMode)
        else:
            mode.enemiesList = list()
            mode.player1.action = 'enraged'
            mode.player1.status = 'newLife'
            mode.player1.health = 100

    def makeEnemiesAttack(mode):
        player = mode.player1
        if len(mode.enemiesList) > 0:
            for enemy in mode.enemiesList:
                if enemy.cooldown == 0:
                    if enemy.position == 'R':
                        if player.cx-30 <= enemy.cx+20 and player.cy == 725:
                            if player.status != 'shield':
                                player.health -= 20
                                enemy.cooldown = 5
                                if player.health <= 0:
                                    mode.newLifeEffect()
                    else:
                        if player.cx+30 >= enemy.cx-20 and player.cy == 725:
                            if player.status != 'shield':
                                player.health -= 20
                                enemy.cooldown = 5
                                if player.health <= 0:
                                    mode.newLifeEffect()
                else:
                    enemy.cooldown -= 1

    def makeJump(mode):
        player, action = mode.player1, mode.player1.action
        if 'standing' in player.previousMove: dx = 0
        elif player.position == 'R': dx = 20
        else: dx = -20
        midPoint = len(player.moves[action])/2-1
        player.cx += dx
        if player.spriteCount <= midPoint:
            player.cy -= 40
        else:
            player.cy += 40
        if player.spriteCount == len(player.moves['jumping'])-1:
            player.spriteCount = 0
            player.cy, player.action = 725, player.previousMove
         
    def bossMakeMove(mode):
        boss = mode.boss
        if mode.difficulty == 'Medium' and random.randint(0,60) == 7 \
            or mode.difficulty == 'Hard' and random.randint(0,40) == 7 \
            or mode.difficulty == 'Easy' and random.randint(0,80) == 7:
            if boss.side == 'R':
                boss.speed = (boss.cx-95-(mode.player1.cx+55))/12
                boss.moves['count'], boss.action = 0, 'movingL'
            else:
                boss.speed = (mode.player1.cx-55-(boss.cx+95))/12
                mode.boss.action, boss.moves['count'] = 'moving', 0

    def moveBossBack(mode):
        boss = mode.boss
        if boss.cx >= mode.player1.cx:
            boss.speed = abs(boss.speed)
            boss.cx += boss.speed
            if boss.cx >= mode.width-120:
                boss.moves['count'] = 0
                boss.cx, boss.side, boss.action = mode.width-120, 'R', 'standingL'
        else:
            boss.speed = abs(boss.speed)
            boss.cx -= boss.speed
            if boss.cx <= 120:
                boss.cx, boss.side, boss.action, boss.moves['count'] = 120, 'L', 'standing', 0

    def moveBoss(mode):
        boss = mode.boss
        if boss.side == 'R' and 'L' in boss.action:
            boss.cx -= boss.speed
            if abs(mode.player1.cx-boss.cx) < 140:
                boss.cx, boss.action = mode.player1.cx+110, 'attackingL'
        elif boss.side == 'L' and 'L' not in boss.action:
            boss.cx += boss.speed
            if abs(mode.player1.cx-boss.cx) < 140:
                boss.cx, boss.action = mode.player1.cx-110, 'attacking'
        else:
            mode.moveBossBack()
 

    def checkForBossAttack(mode):
        if mode.boss.side == 'R':
            if mode.boss.cx-80 <= mode.player1.cx+55 and \
                mode.player1.cx-55 < mode.boss.cx-80 and mode.player1.status != 'shield':
                mode.player1.health -= 30
                mode.score -= 50
                if mode.player1.health < 1:
                    mode.newLifeEffect()
                mode.boss.hit = True
            else:
                mode.boss.hit = False
        else:
            if mode.boss.cx+80 >= mode.player1.cx-55 and \
                mode.player1.cx+55 > mode.boss.cx+80 and mode.player1.status != 'shield':
                mode.player1.health -= 30
                mode.score -= 50
                if mode.player1.health < 1:
                    mode.newLifeEffect()
                mode.boss.hit = True
            else:
                mode.boss.hit = False
    
    def updateBossSprite(mode):
        boss = mode.boss
        if boss.gotHit > 0:
            boss.gotHit -= 1
        if 'moving' in boss.action:
            mode.moveBoss()
        lengthOfSprites = len(boss.moves[boss.action])
        boss.moves['count'] = (boss.moves['count']+1)%lengthOfSprites
        if 'attacking' in boss.action:
            if boss.moves['count'] == lengthOfSprites//2:
                mode.checkForBossAttack()
            elif boss.moves['count'] == lengthOfSprites-1 and boss.hit == False:
                if boss.side == 'R':
                    boss.speed = boss.speed*-1
                    boss.action, boss.moves['count'] = 'moving', 0
                else:
                    boss.speed = boss.speed*-1
                    boss.action, boss.moves['count'] = 'movingL', 0
    
    def dropRandomPowerUp(mode):
        mode.powerUpCount += 1
        if mode.difficulty == 'Easy': interval = 30
        elif mode.difficulty == 'Medium': interval = 60
        else: interval = 90
        if mode.powerUpCount%interval == 0:
            choices = ['life', 'health', 'powerUp', 'shield']
            power, cx, cy = random.choice(choices), random.randint(300,mode.width-300), 0
            mode.powerUpList.append([power, cx, cy])
    
    def updatePowers(mode):
        toRemove = set()
        for i in range(len(mode.powerUpList)):
            item = mode.powerUpList[i]
            item[2] += 5
            if abs(mode.player1.cx-item[1]) <= 30 and abs(mode.player1.cy-item[2]) <= 50\
                and len(mode.player1.storage) < 3:
                mode.player1.storage.append(item[0])
                toRemove.add(i)
            if item[2] > mode.height-120:
                toRemove.add(i)
        for index in toRemove:
            mode.powerUpList.pop(index)
        
    def timerFired(mode):
        mode.updateSprites(mode.player1, mode.player1.action)
        mode.makePlayerMove(mode.player1, mode.player1.action)
        mode.createEnemies()
        mode.updateEnemies()
        mode.moveEnemies()
        mode.moveObjects()
        mode.makeEnemiesAttack()
        mode.updatePowers()
        mode.dropRandomPowerUp()
        if 'jumping' in mode.player1.action:
            mode.makeJump()
        if type(mode.bossOnStage) != int:
            mode.updateBossSprite()
            if 'standing' in mode.boss.action: mode.bossMakeMove()
        if mode.player1.status == 'powered':
            mode.player1.special -= 1
            if mode.player1.special == 0: mode.player1.status = None
            mode.poweredCount = (mode.poweredCount+1)%len(mode.playerStatus['powered'])
        elif mode.player1.status == 'shield':
            mode.shieldTime -= 1
            if mode.shieldTime == 0:
                mode.player1.status = None
                mode.shieldTime = 30
    
    def createEnemies(mode):
        if mode.difficulty == 'Easy': interval = 20
        elif mode.difficulty == 'Medium': interval = 15
        else: interval = 10
        guess = random.randint(0,interval)
        if mode.enemyCreatedTime >= interval//3:
            if guess == 7 or mode.enemyCreatedTime >= (interval//2)*1.5:
                cy = mode.height-140
                edges = random.choice([0, mode.width])
                if mode.difficulty == 'Easy':
                    kind, speed = 'zombie', 5
                elif mode.difficulty == 'Medium':
                    kind, speed = 'military', 10
                else:
                    kind, speed = 'ski', 15
                newEnemy = Enemy(kind, edges, cy)
                newEnemy.speed =  speed
                if type(mode.bossOnStage) == int:
                    mode.bossOnStage += 1
                    if mode.bossOnStage == 35-interval:
                            mode.createBoss()
                            mode.flipBoss()
                            mode.bossOnStage = True
                mode.enemiesList.append(newEnemy)
                mode.enemyCreatedTime = 0
        else:
            mode.enemyCreatedTime += 1
        
    def flipBoss(mode):
        if mode.boss.kind == 'cerberus': moves = ['standing', 'attacking', 'moving']
        elif mode.boss.kind == 'medusa': moves = ['standing', 'attacking', 'projectile', 'moving']
        elif mode.boss.kind == 'aneill': moves = ['standing', 'moving', 'attacking']
        leftMoves = dict()
        for move in moves:
            images = mode.boss.moves[move]
            leftMoves[move+'L'] = list()
            for i in range(len(images)):
                image = images[i]
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                image.cachedPhotoImage = ImageTk.PhotoImage(image)
                leftMoves[move+'L'].append(image)
        mode.boss.moves.update(leftMoves)

    def flipEnemies(mode, enemies):
        leftMoves = dict()
        leftMovesCount = dict()
        for move in enemies:
            images = enemies[move]
            leftMoves[move+'R'] = list()
            leftMovesCount[move+'R'] = 0
            for i in range(len(images)):
                image = images[i]
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                image.cachedPhotoImage = ImageTk.PhotoImage(image)
                leftMoves[move+'R'].append(image)
        enemies.update(leftMoves)
        mode.enemiesCounts.update(leftMovesCount)

    def flipPlayerMoves(mode, player):
        leftMoves = dict()
        for move in player.moves:
            images = player.moves[move]
            leftMoves[move+'L'] = list()
            if type(images) != list:
                image = images.transpose(Image.FLIP_LEFT_RIGHT)
                image.cachedPhotoImage = ImageTk.PhotoImage(image)
                leftMoves[move+'L'] = image
            else:
                for i in range(len(images)):
                    image = images[i]
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    image.cachedPhotoImage = ImageTk.PhotoImage(image)
                    leftMoves[move+'L'].append(image)
        player.moves.update(leftMoves)

    def moveCharacter(mode, position, player):
        if position == 'Left' and player.cx >= 0:
            if player.position == 'R':
                player.position = 'L'
        elif position == 'Right' and player.cx <= mode.width:
            if player.position == 'L':
                player.position = 'R'
    
    def makeBackAttack(mode, player):
        if player.status != 'shield':
            if player.position == 'R':
                player.action = 'backAttack'
            else:
                player.action = 'backAttackL'

    def makeFrontAttack(mode, player):
        if player.status != 'shield':
            if player.position == 'R':
                player.action = 'frontAttack'
            else:
                player.action = 'frontAttackL'

    def makeSpecialAttack(mode, player):
        if player.status != 'shield':
            player.previousMove = player.action
            if player.position == 'R':
                player.action = 'special'
            else:
                player.action = 'specialL'
    
    def usePowerUp(mode, command):
        storage = mode.player1.storage
        'life''health''powerUp''shield'
        if len(storage) > 0 and command in '1!':
            index = 0
        elif len(storage) > 1 and command in '2@':
            index = 1
        elif len(storage) > 2 and command in '3#':
            index = 2
        else: index = None
        if index != None:
            action = storage.pop(index)
            if action =='powerUp':
                mode.player1.special = 100
                mode.player1.status = 'powered'
            elif action =='shield':
                mode.player1.status = 'shield'
            elif action =='life' and mode.player1.lives < 2:
                mode.player1.lives += 1
            elif action =='health':
                mode.player1.health = 100


    def playerCommands(mode, command):
        player = mode.player1
        player.spriteCount, player.previousMove = 0, player.action
        if player.status == 'newLife': player.status = None
        if command == 'Left' or command == 'Right':
            if command == 'Left': mode.player1.action = 'runningL'
            else: mode.player1.action = 'running'
            mode.moveCharacter(command, player)
        elif command == 'Space':
            mode.doJump()
        elif command == 'Down':
            if player.position == 'R':
                player.action = 'standing'
            else:
                player.action = 'standingL'
        elif command in 'Dd':
            mode.makeFrontAttack(player)
        elif command in 'Aa':
            mode.makeBackAttack(player)
        elif command in '123!@#':
            mode.usePowerUp(command)
        elif command in 'Ss':
            if player.status == 'powered':
                mode.makeSpecialAttack(player)
            elif player.special >= 50:
                player.special -= 50
                mode.makeSpecialAttack(player)
        elif command == 'Enter' and player.special == 100:
            player.status = 'powered'

    def doJump(mode):
        if mode.player1.position == 'R':
            mode.player1.action = 'jumping'
        else:
            mode.player1.action = 'jumpingL'

    def keyPressed(mode, event):
        player = mode.player1
        if event.key == '6':
            moe.score = 999999
            mode.app.setActiveMode(mode.app.stagecleared)
        if 'jumping' not in player.action and 'special' not in player.action:
            mode.playerCommands(event.key)

    def drawPlatform(mode, canvas):
        for i in range(6):
            canvas.create_image(mode.width/12+(mode.width/6)*i, mode.height-40, image = mode.platform.cachedPhotoImage)

    def drawPlayer(mode, canvas, player):
        action = player.action
        if player.status == 'newLife':
            if player.spriteCount%2 == 0:
                sprite = player.moves[player.action][player.spriteCount].cachedPhotoImage
                canvas.create_image(player.cx, player.cy, image = sprite)
        else:
            sprite = player.moves[player.action][player.spriteCount].cachedPhotoImage
            if 'frontAttack' in action:
                canvas.create_image(player.cx, player.cy+5, image = sprite)
            elif 'backAttack' in action:
                canvas.create_image(player.cx, player.cy-5, image = sprite)
            else:
                canvas.create_image(player.cx, player.cy, image = sprite) 

    def drawPlayerStatus(mode, canvas):
        player = mode.player1
        if player.status != None:
            if player.status == 'powered':
                status = mode.playerStatus[player.status][mode.poweredCount]
                canvas.create_image(player.cx+5, player.cy-25, image = status.cachedPhotoImage)
            elif player.status != 'newLife':
                status = mode.playerStatus[player.status]
                canvas.create_image(player.cx, player.cy, image = status.cachedPhotoImage)
    
    def drawEnemies(mode, canvas):
        for enemy in mode.enemiesList:
            cx, cy= enemy.cx, enemy.cy
            if enemy.position == 'R':
                kind  = enemy.kind+enemy.position
            else:
                kind = enemy.kind
            picture = mode.enemies[kind][mode.enemiesCounts[kind]]
            canvas.create_image(cx, cy, image = picture.cachedPhotoImage)
    
    def drawProjectile(mode, canvas):
        for projectile in mode.projectileList:
            cx, cy = projectile.cx, projectile.cy
            if projectile.position == 'R':
                projectile = mode.player1.moves['projectile'].cachedPhotoImage
            else:
                projectile = mode.player1.moves['projectileL'].cachedPhotoImage
            gapx, gapy = 38, 27
            canvas.create_image(cx, cy, image = projectile)

    def createBoss(mode):
        if mode.player1.cx <= mode.width/2: cx, side = mode.width-120, 'R'
        else: cx, side = 120, 'L'
        cy, moves = mode.height-140, mode.loadBosses(mode.boss)
        mode.boss = Boss(mode.boss, cx, cy)
        mode.boss.moves, mode.boss.side = moves, side
        if side == 'R':
            mode.boss.action = 'standingL'
        else:
            mode.boss.action = 'standing'

    def drawBoss(mode, canvas):
        cx, cy, boss = mode.width/2, mode.height/2, mode.boss
        gapX, gapY = 95, 80
        picture = boss.moves[boss.action][boss.moves['count']]
        canvas.create_image(boss.cx, boss.cy, image = picture.cachedPhotoImage)
        # Boss health Bar
        cx, cy, gapX, gapY = mode.width/2, mode.height-40, 500, 20
        canvas.create_rectangle(cx-gapX, cy-gapY, (cx-gapX)+boss.health*10, cy+gapY, fill='red')
        canvas.create_rectangle(cx-gapX, cy-gapY, cx+gapX, cy+gapY, fill='', width=5)
        canvas.create_text(cx, cy, text=boss.kind, font = 'times 20 bold')

    def drawPowerUps(mode, canvas):
        for item in mode.powerUpList:
            power, cx, cy = item[0], item[1], item[2]
            picture = mode.powerUps[power].cachedPhotoImage
            canvas.create_image(cx, cy, image = picture)

    def redrawAll(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        canvas.create_image(cx, cy, image = mode.background.cachedPhotoImage)
        mode.drawPlatform(canvas)
        mode.app.gameMode.drawUI(mode, canvas)
        mode.drawEnemies(canvas)
        mode.drawPlayer(canvas, mode.player1)
        mode.drawProjectile(canvas)
        mode.drawPlayerStatus(canvas)
        mode.drawPowerUps(canvas)
        if type(mode.bossOnStage) != int:
            mode.drawBoss(canvas)

class StageClearedMode(Mode):
    def appStarted(mode):
        mode.stage = mode.app.battleArena.stage
        mode.player1 = mode.app.gameMode.player1
        mode.player1.status, mode.player1.spriteCount = None, 0
        mode.platform = mode.app.battleArena.platform
        mode.score = mode.app.battleArena.score
        mode.score = mode.updateScore()
        mode.powerUps = mode.app.battleArena.powerUps
        mode.top10 = mode.app.entryScreen.getLeaderboard(mode)
        lowestScore = mode.top10[-1][1]
        mode.applause = pygame.mixer.Sound('Applause.ogg')
        mode.userInterface = mode.app.battleArena.userInterface
        mode.background = mode.app.battleArena.background
        mode.difficulty = mode.app.entryScreen.difficulty
        if mode.score > lowestScore:
            mode.highScore = True
        else: mode.highScore = False

    def updateScore(mode):
        if mode.stage == 0: return mode.score
        if mode.stage == 1: return mode.score*2
        else: return mode.score*3
    
    def addScore(mode):
        y = mode.getUserInput('What is your name? ')
        newScore = mode.score
        board = open("Leaderboard.txt","a+")
        board.write('\n'+y+','+str(newScore))
        board.close()

    def keyPressed(mode, event):
        if event.key == 'Enter':
            if mode.highScore:
                mode.applause.play()
                mode.addScore()
            mode.app.entryScreen.appStarted()
            mode.app.gameMode.appStarted()
            mode.app.battleArena.appStarted()
            mode.app.setActiveMode(mode.app.entryScreen)

    def timerFired(mode):
        player = mode.player1
        player.spriteCount = (player.spriteCount+1)%len(player.moves[player.action])

    def redrawAll(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        if mode.highScore:
            mode.applause.play()
            mode.player1.action = 'dancing'
            message ='''            Congratulations you made it to the top 10!!!
Tell us your name so that you can go down in history as one of the greatest!'''
        else:
            mode.player1.action = 'celebrating'
            message = '''Congratulations you completed this diffulty level!!!
Sadly you were '''+str(mode.top10[-1][1]-mode.score)+''' points away from making it to the leaderboard
press Enter to go back to the main screen'''
        canvas.create_image(cx, cy, image = mode.background.cachedPhotoImage)
        for i in range(6):
            canvas.create_image(mode.width/12+(mode.width/6)*i, mode.height-40, image = mode.platform.cachedPhotoImage)
        mode.app.gameMode.drawUI(mode, canvas)
        canvas.create_text(cx, cy, text = message, fill ='red', font = 'times 40 italic bold')
        player = mode.player1.moves[mode.player1.action][mode.player1.spriteCount]
        canvas.create_image(cx, mode.height-120, image = player.cachedPhotoImage)

class GameoverMode(Mode):
    def appStarted(mode):
        mode.player1 = mode.app.gameMode.player1
        mode.player1.spriteCount = 0

    def timerFired(mode):
        mode.player1.spriteCount = (mode.player1.spriteCount+1)%len(mode.player1.moves['smash'])

    def keyPressed(mode, event):
        if event.key in 'qQ':
            mode.app.entryScreen.appStarted()
            mode.app.gameMode.appStarted()
            mode.app.battleArena.appStarted()
            mode.app.setActiveMode(mode.app.entryScreen)

        elif event.key in 'rR':
            mode.app.gameMode.appStarted()
            mode.app.battleArena.appStarted()
            mode.app.setActiveMode(mode.app.gameMode)

    def redrawAll(mode, canvas):
        cx, cy = mode.width/2, mode.height/2
        canvas.create_rectangle(0,0,mode.width, mode.height, fill='black')
        canvas.create_text(cx, cy/2, text = 'GAME OVER!!', font = 'times 50 bold italic underline', \
            fill = 'red')
        canvas.create_text(cx, cy, text = '''You can press "q" to quit to the main screen
            or press "r" to try again''', font = 'times 40 bold italic underline', fill ='white')
        player = mode.player1.moves['smash'][mode.player1.spriteCount]
        canvas.create_image(cx, mode.height-180, image = player.cachedPhotoImage)

class Player(Mode):
    def __init__(self, mode):
        self.spriteCount, self.cx, self.cy = 0, 100, mode.height-178
        self.lives, self.action, self.status = 2, 'standing', None
        self.position, self.health, self.special = 'R', 100, 100
        self.previousMove, self.storage, self.moves = None, list(), dict()

class Enemy(object):
    def __init__(self, kind, cx, cy):
        self.kind, self.cx, self.cy = kind, cx, cy
        if self.cx == 0:
            self.position = 'L'
        else:
            self.position = 'R'
        self.cooldown = 0

class Boss(Enemy):
    def __init__(self, kind, cx, cy):
        super().__init__(kind, cx, cy)
        self.health, self.gotHit, self.hit, self.speed = 100, 0, False, 0

class Obstacle(object):
    def __init__(self, name, cx, cy):
        self.name, self.cx, self.cy = name, cx, cy

### Mode superclass has been inherited from cmu_112_graphics 
### http://www.cs.cmu.edu/~112/notes/hw11.html

class MyApp(ModalApp):
    def appStarted(app):
        app.entryScreen = EntryScreen()
        app.gameMode = GameMode()
        app.battleArena = BattleArenaMode()
        app.stagecleared = StageClearedMode()
        app.gameoverMode = GameoverMode()
        app.leaderboardMode = LeaderboardMode()
        app.setActiveMode(app.entryScreen)
        app.timerDelay = 50

app = MyApp(width=1450, height=850)