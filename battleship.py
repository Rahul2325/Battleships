"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["boardsize"]=500
    data["cellsize"]=50
    data["numships"]=5
    data["Computerboard"]=[[]]
    data["Userboard"]=[[]]
    data["Computerboard"]=emptyGrid(data["rows"],data["cols"])
    data["Userboard"]=emptyGrid(data["rows"],data["cols"])
    data["Computerboard"]=addShips(data["Computerboard"],data["numships"])
    #data["Userboard"]=addShips(data["Userboard"],data["numships"])
    data["TemporaryShip"]=[]
    data["noofshipsadded"]=0
    data["winner"]=None
    data["max"]=50
    data["current"]=0
    
    return


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["Userboard"],True) # grid for userboard
    drawGrid(data,compCanvas,data["Computerboard"],False) # grid for computerboard
    drawShip(data,userCanvas,data["TemporaryShip"])
    drawGameOver(data,userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event:
        makeModel(data)


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    position=getClickedCell(data,event)
    if data["winner"]!=None:
        return     
    if(board=="user"):
        clickUserBoard(data,position[0],position[1])
    else:
        runGameTurn(data,position[0],position[1])
    return    

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        l1=[]
        for j in range(cols):
            l1.append(EMPTY_UNCLICKED)
        grid.append(l1)
    return grid


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
import random
def createShip():
    rows=random.randint(1,8)
    cols=random.randint(1,8)
    fordirection=random.randint(0,1)
    if(fordirection==1):
        a=[]
        for i in range(rows-1,rows+2,1):
            a.append([i,cols])
    else:
        a=[]
        for i in range(cols-1,cols+2,1):
            a.append([rows,i])
    return a


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in range(len(ship)): 
        if grid[ship[i][0]][ship[i][1]]!=EMPTY_UNCLICKED: 
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count=0
    while count<numShips:
        ship=createShip()
        if checkShip(grid,ship)==True:
            for i in range(len(ship)):
                grid[ship[i][0]][ship[i][1]]=SHIP_UNCLICKED
            count +=1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(0,data["rows"],1):
        for col in range(0,data["cols"],1):
            if grid[row][col] == SHIP_UNCLICKED:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="yellow")
            elif grid[row][col] == EMPTY_UNCLICKED:  
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="blue")
            elif grid[row][col] == SHIP_CLICKED:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="red")
            elif grid[row][col] == EMPTY_CLICKED:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="white")
            if grid[row][col]== SHIP_UNCLICKED and showShips == False:
                canvas.create_rectangle(data["cellsize"]*col, data["cellsize"]*row, data["cellsize"]*(col+1), data["cellsize"]*(row+1), fill="blue")
    return


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    for i in range(0,2,1):
        if ship[i][1]!= ship[i+1][1]:
            return False
    row=[]        
    for i in range(0,3,1):
        row.append(ship[i][0])
        
    row.sort()
    for i in range(0,2,1):
        if (row[i]+1!= row[i+1]):
            return False
    return True
    


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    for i in range(0,2,1):
        if (ship[i][0]!=ship[i+1][0]):
            return False
    col=[]
    for i in range(0,3,1):
        col.append(ship[i][1])
    col.sort()
    for i in range(0,2,1):
        if (col[i]+1!=col[i+1]):
            return False
    return True



'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    return [int(event.y/data["cellsize"]),int(event.x/data["cellsize"])]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in range(len(ship)):
        shipcorx1=data["cellsize"]*ship[i][1]
        shipcory1=data["cellsize"]*ship[i][0]
        shipcorx2=shipcorx1+data["cellsize"]
        shipcory2=shipcory1+data["cellsize"]
        canvas.create_rectangle(shipcorx1,shipcory1,shipcorx2,shipcory2,fill='white') 
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if(len(ship)==3):
        if(checkShip(grid,ship)==True):
            if(isVertical(ship)==True):
                return True
            elif(isHorizontal(ship)==True):
                return True
    else:
        return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    userboar=data["Userboard"]
    tempship=data["TemporaryShip"]
    if shipIsValid(userboar,tempship):
        for i in range(len(tempship)):
            userboar[tempship[i][0]][tempship[i][1]]=SHIP_UNCLICKED
        data["noofshipsadded"]=data["noofshipsadded"]+1
    else:
        print("Ship is not valid")
    data["TemporaryShip"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    userShip = data["TemporaryShip"]
    userCoordinates = [row, col]
    numUserShip = data["noofshipsadded"]

    #check No of user ships
    if numUserShip == 5:
        print("Ships are ready to fire")
        return

    #check if user coordinates are already present in user ship
    #for i in range(len(userShip)):
    if userCoordinates == userShip:
        return
    userShip.append(userCoordinates)

    #check if user passed 3 coordinates for ship
    if len(userShip) == 3:
        placeShip(data)
    #checking No of ships added
    #if numUserShip == 5:
        #print("Ships are ready to fire")
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED

    else:
        if board[row][col]==EMPTY_UNCLICKED:
            board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["Computerboard"][row][col]==SHIP_CLICKED or data["Computerboard"][row][col]==EMPTY_CLICKED:
        return
    else:
        updateBoard(data,data["Computerboard"],row,col,"user")
    guess=getComputerGuess(data["Userboard"])# 1D List is stored in guess variable [1,2]
    updateBoard(data, data["Userboard"], guess[0],guess[1], "comp")
    data["current"]+=1
    if data["current"]==data["max"]:
        data["winner"]="draw"

    return


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row = random.randint(0,9)
    col = random.randint(0,9)
    while board[row][col]==EMPTY_CLICKED or board[row][col]==SHIP_CLICKED:
        row = random.randint(0,9)
        col = random.randint(0,9)
    if board[row][col]==EMPTY_UNCLICKED or board[row][col]==SHIP_UNCLICKED:
        return [row,col]


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col]==SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"]=="user":
        canvas.create_text(300, 50, text="Congratulations you win", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 100, text="Press enter to play again", fill="black", font=('Helvetica 20 bold'))
    elif data["winner"]=="comp":
        canvas.create_text(300, 50, text="Computer wins", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 100, text="Press enter to play again", fill="black", font=('Helvetica 20 bold'))
    elif data["winner"]=="draw":
        canvas.create_text(300, 50, text="Its A Draw", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 100, text="Press enter to play again", fill="black", font=('Helvetica 20 bold'))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    #test.testIsVertical()
    #test.testShipIsValid()
    #test.testDrawShip()
    #test.testGetClickedCell()
    #test.testIsHorizontal()
    #test.testMakeModel()
    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
    #test.testCheckShip()
    #test.testUpdateBoard()
    #test.testGetComputerGuess()
    #test.testIsGameOver()
