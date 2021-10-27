from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random, math, copy, time, pygame
pygame.mixer.init()

class EntryScreen(Mode):
    def appStarted(mode):
        pass

    def timerFired(mode):
        pass

    def mousePressed(mode, event):
        pass

    def redrawAll(mode, canvas):
        pass

class initializeSystem(Mode):
    def appStarted(mode):
        pass

    def keyPressed(mode, event):
        pass

    def mousePressed(mode, event):
        pass
        
    def redrawAll(mode, canvas):
        pass

class History(Mode):
    def appStarted(mode):
        pass

    def keyPressed(mode, event):
        pass

    def timerFired(mode):
        pass

    def redrawAll(mode, canvas):
        pass

########## Menu(Sandwiches/Beverages/Desserts) Screens Functions #############    
class Desserts(Mode):
    def appStarted(mode):
        pass

    def mousePressed(mode, event):
        pass

    def timerFired(mode):
        pass
        
    def redrawAll(mode, canvas):
        pass
        
    def keyPressed(mode, event):
        pass

class Sandwiches(Mode):
    def appStarted(mode):
        pass
    
    def timerFired(mode):
        pass

    def keyPressed(mode, event):
        pass

    def redrawAll(mode, canvas):
        pass

class Beverages(Mode):
    def appStarted(mode):
        pass

    def keyPressed(mode, event):
        pass

    def timerFired(mode):
        pass

    def redrawAll(mode, canvas):
        pass

class Checkout(Mode):
    def appStarted(mode):
        pass

    def timerFired(mode):
        pass

    def keyPressed(mode, event):
        pass

    def redrawAll(mode, canvas):
        pass

class Player(Mode):
    def __init__(self, mode):
        self.spriteCount, self.cx, self.cy = 0, 100, mode.height-178
        self.lives, self.action, self.status = 2, 'standing', None
        self.position, self.health, self.special = 'R', 100, 100
        self.previousMove, self.storage, self.moves = None, list(), dict()

class Product(object):
    def __init__(self, kind, cx, cy):
        self.kind, self.cx, self.cy = kind, cx, cy
        if self.cx == 0:
            self.position = 'L'
        else:
            self.position = 'R'
        self.cooldown = 0

class Beverages(object):
    def __init__(self, kind, cx, cy):
        super().__init__(kind, cx, cy)
        self.health, self.gotHit, self.hit, self.speed = 100, 0, False, 0

class Transaction(object):
    def __init__(self, name, cx, cy):
        self.name, self.cx, self.cy = name, cx, cy

### Mode superclass has been inherited from cmu_112_graphics 
### http://www.cs.cmu.edu/~112/notes/hw11.html

class MyApp(ModalApp):
    def appStarted(app):
        app.entryScreen = EntryScreen()
        app.transactionLogScreen = History()
        app.sandwichScreen = Sandwiches()
        app.beverageScreen = Beverages()
        app.checkoutScreen = Checkout()
        app.initialize = initializeSystem()
        app.setActiveMode(app.initialize)
        app.timerDelay = 100

app = MyApp(width=1450, height=850)