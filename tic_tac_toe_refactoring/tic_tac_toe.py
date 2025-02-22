from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Tic Tac Toe Game')

# Player 1 [X] starts first, Player 2 [O] continues
clicked = True
count = 0

# To check whether did anyone won the game and restart the game when someone won the game
def checkWinner():
    global winner
    winner = False
    player = 0

    for line in range(3):
        #lines
        if buttons[(line, 0)]["text"] != " " and all([buttons[(line, col)]["text"] == buttons[(line, 0)]["text"] for col in range(3)]):
            [buttons[(line, col)].config(bg="#80ffaa") for col in range(3)]
            player = [2, 1][buttons[(line, 0)]["text"] == "X"]
        #rows
        if buttons[(0, line)]["text"] != " " and all([buttons[(col, line)]["text"] == buttons[(0, line)]["text"] for col in range(3)]):
            [buttons[(col, line)].config(bg="#80ffaa") for col in range(3)]
            player = [2, 1][buttons[(0, line)]["text"] == "X"]
    #croix down
    if buttons[(0, 0)]["text"] != " " and all([buttons[(col, col)]["text"] == buttons[(0, 0)]["text"] for col in range(3)]):
            [buttons[(col, col)].config(bg="#80ffaa") for col in range(3)]
            player = [2, 1][buttons[(0, 0)]["text"] == "X"]
    #croix up
    if buttons[(2, 0)]["text"] != " " and all([buttons[(2 - col, col)]["text"] == buttons[(2, 0)]["text"] for col in range(3)]):
            [buttons[(2 - col, col)].config(bg="#80ffaa") for col in range(3)]
            player = [2, 1][buttons[(2, 0)]["text"] == "X"]

    if player:
        winner = True
        messagebox.showinfo("Tic Tac Toe", f"Player {player} is the Winner!")
        start()


# To check whether the game is a draw
def checkDraw():
    global count, winner

    if count == 9 and winner == False:
        messagebox.showerror("Tic Tac Toe", "Draw, play again!")
        start()

# To determine the buttons that Player 1 or Player 2 has clicked on
def buttonClicked(event):
    global clicked, count

    if event.widget["text"] == " " and clicked == True:
        event.widget["text"] = "X"
        clicked = False
        count += 1
    elif event.widget["text"] == " " and clicked == False:
        event.widget["text"] = "O"
        clicked = True
        count += 1
    else:
        messagebox.showerror("Tic Tac Toe", "Please select another box.")
    checkWinner()
    checkDraw()

# To start or restart the game
def start():
    global buttons
    global clicked, count
    clicked = True
    count = 0

    # Building the buttons for the game (1-9)
    # Place them for rows and clumns
    buttons = {}
    settings = {"text":" ", "font":("Helvetica, 20"), "height":3, "width":7, "bg":"SystemButtonFace"}
    for line in range(3):
        for col in range(3):
            #DOESN'T WORKED!!!! WHY?
            #butt = Button(root, command=lambda: buttonClicked(butt), **settings)
            butt = Button(root, **settings)
            butt.bind("<Button-1>", buttonClicked)
            butt.grid(row=line, column=col)
            buttons[(line, col)] = butt


# Create game menu
gameMenu = Menu(root)
root.config(menu = gameMenu)

# Create game options menu
optionMenu = Menu(gameMenu, tearoff=False)
gameMenu.add_cascade(label="Options", menu=optionMenu)
optionMenu.add_command(label="Restart Game", command=start)


start()
root.mainloop()

#There was 247 rows