import click
import random
import copy


boardSize = click.prompt("Board Size", type=int, default=5)
winValue = click.prompt("Win Value", type=int, default=2048)


# function for printing the current board
def display(board):

    #to find the largest value
    largest = board[0][0]
    for row in board:
        for element in row:
            if element > largest:
                largest = element

     #max number of spaces
    numSpaces = len(str(largest))

    for row in board:
        currentRow: str = "  "
        for element in row:
            currentRow += (" " * (numSpaces - len(str((element)))) + str(element) + " ")
        print(currentRow)
    print()

    return board




#To merge everything of one row to left
def mergeOneRowLeft(row):
    #move every thing to the left
    for j in range(boardSize - 1):
        for i in range(boardSize - 1, 0, -1):
            if row[i - 1] == 0:
                row[i - 1] = row[i]
                row[i] = 0

     #Add same numbers to left
    for i in range (boardSize - 1):
         if row[i + 1] == row[i]:
             row[i] = row[i] * 2
             row[i+1] = 0

    #moving everything to left again
    for j in range(boardSize - 1):
        for i in range(boardSize - 1, 0, -1):
            if row[i - 1] == 0:
                row[i - 1] = row[i]
                row[i] = 0
    return row

#applying mergeOneRowLeft() to each amd every row i.e. function for merging left
def merge_left(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = mergeOneRowLeft(currentBoard[i])
    return currentBoard



#function for reversing the order of row
def reverse(row):
    new = []
    for i in range(boardSize -1, -1, -1):
        new.append(row[i])
    return new

#function for transposing the array
def transpose(currentBoard):
    for j in range(boardSize):
        for i in range(j,boardSize):
            if not i == j:
                temp = currentBoard[j][i]
                currentBoard[j][i] = currentBoard[i][j]
                currentBoard[i][j] = temp
    return currentBoard



#function for merging right: first reverse then merge left then again reverse
def merge_right(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = reverse(currentBoard[i])
        currentBoard[i] = mergeOneRowLeft(currentBoard[i])
        currentBoard[i] = reverse(currentBoard[i])
    return currentBoard

#function for merging up: first transpose then merge left then again transpose
def merge_up(currentBoard):
    currentBoard = transpose(currentBoard)
    currentBoard = merge_left(currentBoard)
    currentBoard = transpose(currentBoard)
    return currentBoard

#function for merging down: first transpose then merge right then again transpose
def merge_down(currentBoard):
    currentBoard = transpose(currentBoard)
    currentBoard = merge_right(currentBoard)
    currentBoard = transpose(currentBoard)
    return currentBoard


#functions which add 2
def newValue():
    return 2

#randomly selecting an element of array & add new number after a move
def addNewValue():
    row_number = random.randint(0,boardSize - 1)
    column_number = random.randint(0, boardSize - 1)

    while not board[row_number][column_number] == 0:
        row_number = random.randint(0, boardSize - 1)
        column_number = random.randint(0, boardSize - 1)

    board[row_number][column_number] = newValue()


#fuction to test game won
def won():
    for row in board:
        if winValue in row:
            return True
    return False

#fuction to test that any move is possible or not
def noMoves():
    tempBoard1 = copy.deepcopy(board)
    tempBoard2 = copy.deepcopy(board)

    tempBoard1 = merge_down(tempBoard1)
    if tempBoard1 == tempBoard2:
        tempBoard1 = merge_up(tempBoard1)
        if tempBoard1 == tempBoard2:
            tempBoard1 = merge_left(tempBoard1)
            if tempBoard1 == tempBoard2:
                tempBoard1 = merge_right(tempBoard1)
                if tempBoard1 == tempBoard2:
                    return True
    return False




#MAIN PART:
#create blank  board
board = []
for i in range(boardSize):
    row = []
    for j in range (boardSize):
        row.append(0)
    board.append(row)

#fill one random value
row_number = random.randint(0, boardSize - 1)
column_number = random.randint(0, boardSize - 1)

if board[row_number][column_number] == 0:
    board[row_number][column_number] = newValue()

display(board)


if winValue == 2 or boardSize == 1:
    if won():
        print("Won!!")
    else:
        print("Lost!!")
else:

    gameOver = False
    while not gameOver:
        move = input()


        validInput = True


        #to check whether board changed or not, we create a duplicate copy of the board...
        tempBoard = copy.deepcopy(board)


        if move == "W" :
            board = merge_up(board)
        elif move == "A" :
            board = merge_left(board)
        elif move == "S" :
            board = merge_down(board)
        elif move == "D" :
            board = merge_right(board)
        else:
            validInput = False

        if not validInput:
            print("Invalid move")
        else:
            if board == tempBoard:
                print("try different move")
            else:
                if won():
                    display(board)
                    print("Won!!")
                    gameOver = True
                else:
                    addNewValue()
                    display(board)

                if noMoves():
                    print("Lost!!")
                    gameOver = True