from tkinter import *

"""

Link to change buttons to be sunked or risen:
https://www.geeksforgeeks.org/how-to-set-border-of-tkinter-label-widget/

"""
class Components():
    def __init__(self):
        self.initializeCalculatorDimensions()
        self.initializeCalculator()
        self.initializeVerifyButtonDimensions()
        self.initializeOptionsCardsDimensions()
        self.scrolling = False
        self.optionsWidth, self.optionsHeight, self.optionsGap = 100, 25, 80
        self.backDropWidth = 250
        self.optionsTitleGap, self.optionsTitleFont = 30, "times 40 bold italic"

    def initializeOptionsCardsDimensions(self):
        self.cardFont = "times 28 bold italic"

    def initializeCalculatorDimensions(self):
        self.calcSize, self.calcButtonGap, self.calcWidth = 150, 150, 400
        self.calcHeight, self.calcBorder, self.calcMssgWidth = 400, 30, 200
        self.calcScreenHeight, self.calcScreenWidth = 80, 450
        self.calcButtonsFont, self.calcNumGap = "times 40 bold", 20
        self.calcMssgFont, self.calcExitSize = "times 35 bold italic", 70

    def initializeVerifyButtonDimensions(self):
        self.buttonCy, self.buttonYGap, self.verifyWidth = 200, 250, 250
        self.verifyDecision, self.verifyCy = False, self.buttonCy+self.buttonYGap//2
        self.verifyHeight, self.buttonWidth, self.buttonFont = 150, 250, "times 28 bold"
        self.verifyButtonCy = self.verifyCy+(self.verifyHeight//5*2)
        self.verifyButtonW, self.verifyButtonH = self.verifyWidth//4, self.verifyHeight//4
            
    def initializeCalculator(self):
        self.calcNumber, self.prevNumber, self.calcOperation = "0", "0", None
        self.calcEnteringNumber = True

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

        # Drawing the operation symbols + enter/= button
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
        if(mode.app.getPrice):
            Text(enterX0+opWidth, enterY0+opHeight/2, text = "Enter", font = buttonFont)
        else:
            Text(enterX0+opWidth, enterY0+opHeight/2, text = "=", font = buttonFont)
        
        # Drawing the number displayed on the calculator + message displayed
        numGap = self.calcNumGap
        numCx, numCy = calcScX0+scWidth-numGap, calcScY0+scHeight/2
        for c in self.calcNumber[::-1]:
            Text(numCx, numCy, text = c, font = buttonFont, fill = "white")
            numCx -= numGap 
        Text(mssgX0+mssgWidth/2, mssgY0+scHeight/2, text = mode.calcMssg,
                    font = self.calcMssgFont)

    #   Gets the number that was pressed in the x,y coordinate
    #   on the calculator given the gap between the buttons
    def getNumberPressed(self, x, y, gap):
        numbers = [["1", "2", "3"], ["4", "5", "6"], 
                    ["7", "8", "9"], ["0", "0", "Clear"]]
        row, col = int(y/gap), int(x/gap)
        return numbers[row][col]

    #   Gets the operation that was pressed in the x,y coordinate 
    #   on the calculator given the height and the width of the
    #   buttons
    def getOperationPressed(self, x, y, height, width):
        if(y < height):
            return "Borrar"
        elif(y > height*3):
            return "Enter"
        else:
            operations = [["+", "-"], ["*", "/"]]
            row, col = int((y-height)/height), int(x/width)
            return operations[row][col]

    #   Does the current operation that should be done
    #   on the calculator
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

    #   Handles any action that should be taken 
    #   when the calculator is pressed on the given
    #   x,y coordinate
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

        if(keyPressed == "Enter"):
            return keyPressed
        elif keyPressed.isdigit():
            if(self.calcEnteringNumber):
                if(self.calcNumber == "0"):
                    self.calcNumber = keyPressed
                else:
                    self.calcNumber = self.calcNumber + keyPressed
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

    def drawOptions(self, mode, canvas, options):
        Rectangle, Text = canvas.create_rectangle, canvas.create_text
        cx, cy, optionsGap = mode.width/2, mode.height/2, self.optionsGap
        width = self.optionsWidth
        titleGap, exitSize = self.optionsTitleGap, self.calcExitSize
        bdWidth, height = self.backDropWidth, self.optionsHeight
        bdHeight = titleGap+len(options["items"])*(height*2)

        #   Drawing the options box + title + exit sign
        Rectangle(cx-bdWidth, cy-bdHeight, cx+bdWidth, cy+bdHeight, fill = "white")
        Text(cx, cy-bdHeight+titleGap, text = options["title"],
                font = self.optionsTitleFont)
        Rectangle(cx+bdWidth, cy-bdHeight, cx+bdWidth-exitSize, cy-bdHeight+exitSize,
                    fill = "red")
        Text(cx+bdWidth-exitSize/2, cy-bdHeight+exitSize/2, text = "X", 
                    font = self.calcButtonsFont)

        #   Drawing each of the options
        for i in range(len(options["items"])):
            centerY, item = cy-bdHeight+titleGap+optionsGap*(i+1), options["items"][i]
            Rectangle(cx-width, centerY-height, cx+width, centerY+height,
                        fill = "grey")
            Text(cx, centerY, text = item, font = self.calcButtonsFont)

    def optionsPressed(self, mode, options, x, y):
        cx, cy, optionsGap = mode.width/2, mode.height/2, self.optionsGap
        width = self.optionsWidth
        titleGap, exitSize = self.optionsTitleGap, self.calcExitSize
        bdWidth, height = self.backDropWidth, self.optionsHeight
        bdHeight = titleGap+len(options["items"])*(height*2)

        #   Checking if exit button was pressed
        if(x < cx+bdWidth and x > cx + bdWidth - exitSize
            and y > cy-bdHeight and y < cy-bdHeight+exitSize):
            return "Exit"

        # Checking to see if x coordinate is outside the width of the options
        # and the y coordinate is outside the box
        elif(x < cx-width or x > cx+width or
            y > cy+bdHeight or y < cy-bdHeight):
            return None

        else:
            # Checking to see which item was clicked if any
            items = options["items"]
            for i in range(len(items)):
                centerY, item = cy-bdHeight+titleGap+optionsGap*(i+1), items[i]
                if(y < centerY+height and y > centerY-height):
                    return item
            return None

    def drawVerificationButton(self, mode, canvas):
        self.verifyButtonCx = mode.width//2-self.verifyWidth//2
        Rect, Oval = canvas.create_rectangle, canvas.create_oval
        Text = canvas.create_text
        width, height = self.verifyWidth, self.verifyHeight
        buttonFont = self.buttonFont
        cx, cy = mode.width/2, self.verifyCy
        verifyTextCy = cy-(height//3)
        buttonCy, buttonCx  = self.verifyButtonCy, self.verifyButtonCx
        buttonW, buttonH, buttonGap = self.verifyButtonW, self.verifyButtonH, self.buttonWidth


        Rect(cx-width, cy-height, cx+width, cy+height, fill = "grey")
        Text(cx, verifyTextCy, text ="""¿quieres cancelar esta orden?""",
            font = buttonFont)
        Rect(buttonCx-buttonW, buttonCy-buttonH, buttonCx+buttonW, buttonCy+buttonH,
                fill = "indian red")
        Rect(buttonCx-buttonW+buttonGap, buttonCy-buttonH, 
                buttonCx+buttonW+buttonGap, buttonCy+buttonH, fill = "light green")
        Text(buttonCx, buttonCy, text = "No", font = buttonFont)
        Text(buttonCx+buttonGap, buttonCy, text = "Si", font = buttonFont)

    def pressedVerifyOption(self, event):
        noRange = range(self.verifyButtonCx-self.verifyButtonW,
                            self.verifyButtonCx+self.verifyButtonW+1)
        yesRange = range(self.verifyButtonCx-self.verifyButtonW+self.buttonWidth,
                            self.verifyButtonCx+self.verifyButtonW+self.buttonWidth+1)
        if(event.x in noRange or event.x in yesRange):
            self.verifyDecision = False
            if(event.x in yesRange):
                return True
        return False

    def drawOptionsCards(self, mode, canvas):
        Rect, Oval= canvas.create_rectangle, canvas.create_oval
        self.cardTitleH = -25
        self.cardW, self.cardH = mode.width//6, mode.height//10
        self.cardXGap, self.cardYGap = self.cardW*3, self.cardH*3+80
        self.iconCx = self.cardCx-self.cardW
        Text, cardFont = canvas.create_text, self.cardFont
        cardCx, cardCy, count = self.cardCx, self.cardCy, 0
        cardW, cardH, cardTitleH = self.cardW, self.cardH, self.cardTitleH
        xGap, yGap = self.cardXGap, self.cardYGap

        for card in mode.cards:
            xGapInd, yGapInd = count%2, count//2
            Rect(cardCx-cardW+xGap*xGapInd, cardCy-cardH+yGap*yGapInd, 
                cardCx+cardW+xGap*xGapInd, cardCy+cardH+yGap*yGapInd, 
                fill = "white", outline = "black")
            Text(cardCx+xGap*xGapInd, cardCy-cardH+yGap*yGapInd+cardTitleH, 
                text = card, font = cardFont)
            count += 1

    def drawIcons(self, mode, canvas):
        count = 0
        for option in mode.iconImages:
            xGapInd, yGapInd = count%2, count//2
            cx, cy = self.adjustCenter(xGapInd, yGapInd, option)
            icon = mode.iconImages[option]
            if("Refresco" in option):
                cx -= 10
            canvas.create_image(cx, cy, image = icon.cachedPhotoImage)
            count += 1
    
    def adjustCenter(self, xGap, yGap, icon):
        cx, cy = self.iconCx+self.cardXGap*xGap, self.cardCy+self.cardYGap*yGap
        if("Cafe" in icon):
            cy -= 40
        elif("Jugo" in icon):
            cy -= 20
        elif("Batida" in icon):
            cy -= 27
        elif("Agua" in icon):
            cy -= 20
        return(cx, cy)

    def scrollScreen(self, dist):
        newCardCy = self.cardCy+dist
        (minimum, maximum) = self.screenRange
        self.cardCy = min(newCardCy, maximum)
        self.cardCy = max(self.cardCy, minimum)

    def pressedCard(self, mode, event):
        count = 0
        cardCx, cardCy, count = self.cardCx, self.cardCy, 0
        cardW, cardH = self.cardW, self.cardH
        xGap, yGap = self.cardXGap, self.cardYGap

        # Rect(cardCx-cardW+xGap*xGapInd, cardCy-cardH+yGap*yGapInd, 
        #     cardCx+cardW+xGap*xGapInd, cardCy+cardH+yGap*yGapInd, 
        #     fill = "white", outline = "black")
        
        for card in mode.cards:
            xGapInd, yGapInd  = count%2, count//2
            xRange = range(cardCx+xGap*xGapInd-cardW, cardCx+xGap*xGapInd+cardW)
            yRange = range(cardCy+yGap*yGapInd-cardH, cardCy+yGap*yGapInd+cardH)
            if(event.x in xRange and event.y in yRange):
                return card
        return None
                
