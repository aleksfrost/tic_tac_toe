from tkinter import Button, messagebox
from tkinter import *



class Board:

    settings = {"text":" ", "font":("Helvetica, 20"), "height":3, "width":7, "bg":"SystemButtonFace"}

    def __init__(self):
        self.root = Tk()
        self.root.title('Tic Tac Toe Game')
        self.buttons = {}
        self.make_butts()
        self.root.mainloop()
        self.move = None


    #Click handler
    def buttonClicked(self, event: Event):
        for pos, butt in self.buttons.items():
            if butt == event.widget:
                self.move = pos
        print(self.move)

    #Block_unblock
    def block_buttons(self):
        for _, butt in self.buttons.items():
            butt.config(state=DISABLED)

    def unblock_buttons(self):
        for _, butt in self.buttons.items():
            butt.config(state=NORMAL)

    # Building the buttons for the game (1-9)
    # Place them for rows and clumns
    def make_butts(self):
        for line in range(3):
            for col in range(3):
                butt = Button(self.root, **Board.settings)
                butt.bind("<Button-1>", self.buttonClicked)
                butt.grid(row=line, column=col)
                self.buttons[(line, col)] = butt

    def display(self):
        butts = []
        for _, butt in self.buttons.items():
            butts.append(butt["text"])
        return butts



if __name__ == "__main__":
    b = Board()