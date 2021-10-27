from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random, math, copy, time, pygame
from datetime import date
from openpyxl import Workbook, load_workbook

'''
Documentation for Workbooks on openpyxl: https://openpyxl.readthedocs.io/en/stable/tutorial.html


######################## Worksheet documentation ##############################
Create new workbook -> wb = Workbook()

Get first sheet -> ws = wb.active

To create a new sheet on workbook -> ws2 = wb.create_sheet(title = "Mysheet", index)
By default create_sheet will create it at the end if no index is specified.
Index 0 is the first position and index -1 is the penultimate

To change title of a sheet -> ws.title = "New Title"

Sheets can be obtained from workbook with their name as key -> ws3 = wb["New Title"]

To see list of all of the sheets in a workbook -> print(wb.sheetnames)

You can also loop through worksheets -> for sheet in wb:


########################## Cells documentation ################################

When a worksheet is created it contains no cells, they must be created first


Cells can be accessed as keys on the ws -> c = ws['A4']

Cells can also be accessed by cells using row and col -> d = ws.cell(row=4, column=2, value=10)

Ranges of cells can be obtained through slicing -> cell_range = ws['A1':'C2']
Example for columns: colC = ws['C'], col_range = ws['C:D']
Example for rows: row10 = ws[10], row_range = ws[5:10]

To iterate through all of the rows in a file -> ws.rows

We can assign values to cells directly -> c.value = 'hello, world'

##########################  Working with Workbooks #############################

To save the current Workbook -> wb.save('balances.xlsx') 
This will overwrite any existing workbook with the given name.

To load up a workbook -> wb2 = load_workbook('test.xlsx')


############################ Tricks and Tips #################################

Set date and time using Python date -> ws['A1'] = datetime.datetime(2010, 7, 21)

Adding a formula to a cell -> ws["A1"] = "=SUM(1, 1)"



'''
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
    def getDate(mode):
        today = date.today()
        month, day = today.strftime("%m"), today.strftime("%d")
        print(month+"-"+day)
        return month+"-"+day

    def getSheet(mode, path):
        workBook = load_workbook(path)
        newSheet = workBook.create_sheet(title = mode.getDate())
        return (workBook, newSheet)

    def getCatalog(mode, path):
        return None

    def appStarted(mode):
        mode.catalog = mode.getCatalog("catalog.txt")
        mode.workBook, mode.sells = mode.getSheet("sellsLog.xlsx")

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

class Product(object):
    def __init__(self, kind):
        pass

class Beverage(object):
    def __init__(self, kind, cx, cy):
        pass

class Transaction(object):
    """
    To get the time for each transaction we do time = now.strftime("%H:%M:%S")
print("time:", time)
    
    """
    def __init__(self):
        pass

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