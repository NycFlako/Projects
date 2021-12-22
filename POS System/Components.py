from tkinter import *

class Components():
    def __init__(self):
        self.initializeCalculatorDimensions()
        self.initializeCalculator()
        
    def initializeCalculatorDimensions(self):
        self.calcSize, self.calcButtonGap, self.calcWidth = 150, 150, 400
        self.calcHeight, self.calcBorder, self.calcMssgWidth = 400, 30, 200
        self.calcScreenHeight, self.calcScreenWidth = 80, 450
        self.calcButtonsFont, self.calcNumGap = "times 40 bold", 20
        self.calcMssgFont, self.calcExitSize = "times 35 bold italic", 70

    def initializeCalculator(self):
        self.calcNumber, self.prevNumber, self.calcOperation = "0", "0", None
        self.calcEnteringNumber = True

    # Component that draws the calculator
    def drawCalculator(self, mode, canvas):
        Rectangle, Text = canvas.create_rectangle, canvas.create_text
        Polygon = canvas.create_polygon
        cx, cy, width = mode.width/2, mode.height/2, self.calcWidth
        height, size, border = self.calcHeight, self.calcSize, self.calcBorder
        calcX0, calcY0, calcX1  = cx-width+border, cy-height+border, cx+width-border
        calcY1, scBorder, exitSize = cy+height-border, border/2, self.calcExitSize
        calcScX0, calcScY0 = calcX0+scBorder, calcY0+scBorder
        scHeight,scWidth = self.calcScreenHeight,self.calcScreenWidth
        buttonsGap, buttonNumber, scBorder = self.calcButtonGap, 0, border/2
        buttonFont = self.calcButtonsFont

        # Drawing Screens, borders and exit button
        Rectangle(cx-width, cy-height, cx+width, cy+height, fill = "brown")
        Rectangle(calcX0, calcY0, calcX1, calcY1, fill = "dark grey")
        Rectangle(calcScX0, calcScY0, calcScX0+scWidth, 
                    calcScY0+scHeight, fill="black")
        Rectangle(cx+width, cy-height, cx+width-exitSize, 
                    cy-height+exitSize, fill = "white")
        Text(cx+width-exitSize/2, cy-height+exitSize/2, text = "X",
                font = buttonFont)

        # Drawing the number pad
        for row in range(3):
            for col in range(3):
                buttonNumber += 1
                buttonsX0 = calcScX0 + buttonsGap*col
                buttonsY0 = calcScY0+scHeight+border+buttonsGap*row
                Rectangle(buttonsX0, buttonsY0, buttonsX0+size, buttonsY0+size,
                            fill = "light blue")
                Text(buttonsX0+size/2, buttonsY0+size/2, 
                        text = str(buttonNumber), font = buttonFont)
        Rectangle(calcScX0, buttonsY0+size, calcScX0+size*2, buttonsY0+size*2,
                    fill = "light blue")
        Text(calcScX0+size, buttonsY0+size*3/2, text = "0", font = buttonFont)
        Rectangle(calcScX0+size*2, buttonsY0+size, calcScX0+size*3, 
                    buttonsY0+size*2, fill = "red")
        Text(calcScX0+size*5/2, buttonsY0+size*3/2, text = "C", font = buttonFont)

        # Drawing the message screen + delete button
        mssgX0, mssgY0 = calcScX0+scWidth+border, calcScY0
        mssgWidth = self.calcMssgWidth
        Rectangle(mssgX0, mssgY0, mssgX0 + mssgWidth, 
                    mssgY0+scHeight, fill = "white")
        deleteY0 = mssgY0+scHeight+border
        Rectangle(mssgX0, deleteY0, mssgX0+mssgWidth, 
                    deleteY0 + size, fill = "grey")
        Polygon(870, 255, 920, 215, 920, 295, fill = "dark grey", width = 0)
        Rectangle(920, 215, 1010, 295, fill = "dark grey", width = 0)
        Text(955, 255, text = "Borrar", font = "times 25 bold")

        # Drawing the operation symbols + enter button
        operations = ["+", "-", "*", "/"]
        for i in range(len(operations)):
            op, row, col = operations[i], i//2, i%2 
            opWidth, opHeight = (mssgWidth/2), buttonsGap
            x0 = mssgX0+opWidth*col
            y0 = calcScY0+scHeight+border+opHeight*(row+1)
            Rectangle(x0, y0, x0+opWidth, y0+opHeight, fill = "light blue")
            Text(x0+opWidth/2, y0+opHeight/2, text = op, font = buttonFont)
        enterX0, enterY0 = mssgX0, y0+opHeight
        Rectangle(enterX0, enterY0, enterX0+opWidth*2, enterY0+opHeight,
                    fill = "green")
        Text(enterX0+opWidth, enterY0+opHeight/2, text = "Enter", font = buttonFont)
        
        # Drawing the number displayed on the calculator + message displayed
        numGap = self.calcNumGap
        numCx, numCy = calcScX0+scWidth-numGap, calcScY0+scHeight/2
        for c in self.calcNumber[::-1]:
            Text(numCx, numCy, text = c, font = buttonFont, fill = "white")
            numCx -= numGap 
        Text(mssgX0+mssgWidth/2, mssgY0+scHeight/2, text = mode.calcMssg,
                    font = self.calcMssgFont)

    def getNumberPressed(self, x, y, gap):
        numbers = [["1", "2", "3"], ["4", "5", "6"], 
                    ["7", "8", "9"], ["0", "0", "Clear"]]
        row, col = int(y/gap), int(x/gap)
        return numbers[row][col]

    def getOperationPressed(self, x, y, height, width):
        if(y < height):
            return "Borrar"
        elif(y > height*3):
            return "Enter"
        else:
            operations = [["+", "-"], ["*", "/"]]
            row, col = int((y-height)/height), int(x/width)
            return operations[row][col]

    def doOperation(self):
        prev, op, curr = self.prevNumber, self.calcOperation, self.calcNumber
        if(op == None):
            return
        if(op in "+-/*"):
            if(op == "+"):
                self.calcNumber = str(int(prev) + int(curr))
            elif(op == "-"):
                self.calcNumber = str(int(prev) - int(curr))
            elif(op == "*"):
                self.calcNumber = str(int(prev) * int(curr))
            else:
                self.calcNumber = str(int(int(prev) / int(curr)))
        self.calcOperation = None
        self.prevNumber = "0"

    def calculatorPressed(self, mode, x, y):
        border, cx, cy = self.calcBorder, mode.width/2, mode.height/2
        width, height, scWidth = self.calcWidth, self.calcHeight, self.calcScreenWidth
        calcX0, calcY0 = cx-width+border, cy-height+border
        scBorder, size, scHeight = border/2, self.calcSize, self.calcScreenHeight
        numbersX0, numbersY0 = calcX0+scBorder, calcY0+scBorder+scHeight+border
        numbersWidthRange = range(int(numbersX0), int(numbersX0+size*3))
        numbersHeightRange = range(int(numbersY0), int(numbersY0+size*4))
        operationX0, opWidth = numbersX0+scWidth+border, self.calcMssgWidth
        operationsWidthRange = range(int(operationX0), int(operationX0 + opWidth))
        exitSize = self.calcExitSize
        exitWidthRange = range(int(cx+width-exitSize), int(cx+width))
        exitHeightRange = range(int(cy-height), int(cy-height+exitSize))
        if(x in exitWidthRange and y in exitHeightRange):
            return "Exit"
        elif(x in numbersWidthRange and y in numbersHeightRange):
            keyPressed = self.getNumberPressed(x-numbersX0, y-numbersY0, size)
        elif(x in operationsWidthRange and y in numbersHeightRange):
            keyPressed = self.getOperationPressed(x-operationX0, y-numbersY0, 
                                    size, opWidth/2)
        else:
            return

        if keyPressed.isdigit():
            if(self.calcEnteringNumber):
                if(self.calcNumber == "0"):
                    self.calcNumber = keyPressed
                    print(self.calcNumber)
                else:
                    self.calcNumber = self.calcNumber + keyPressed
                    print(self.calcNumber)
            else:
                self.initializeCalculator()
                self.calcNumber = keyPressed
        elif(keyPressed == "Clear"):
            self.initializeCalculator()
        elif(keyPressed == "Enter"):
            self.doOperation()
            self.calcEnteringNumber = False
        elif(keyPressed == "Borrar"):
            if(self.calcNumber != "0"):
                self.calcNumber = self.calcNumber[:-1]
                if(self.calcNumber == ""):
                    self.calcNumber = "0"

        elif(self.calcOperation == None):
            if(not self.calcEnteringNumber):
                self.calcEnteringNumber = True
            self.calcOperation = keyPressed
            self.prevNumber = self.calcNumber
            self.calcNumber = "0"
        else:
            self.doOperation()
            self.calcOperation = keyPressed
            self.prevNumber = self.calcNumber
            self.calcNumber = "0"


            


