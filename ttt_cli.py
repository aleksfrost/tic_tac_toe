import socket
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QDialog,
    QFormLayout,
    QGridLayout,
)
from PyQt6 import QtGui, QtCore
from PySide6.QtCore import Slot, QThreadPool





class Board(QMainWindow):
    def __init__(self, cli: "TicTacToeClient"):
        super().__init__()

        self.game_data: list = None
        self.main_layout = QGridLayout()
        self.cli = cli
        self.marker = None
        self.thread_manager = QThreadPool()

        self.label = QLabel("")
        self.one = QPushButton(text=" ")
        self.two = QPushButton(text=" ")
        self.three = QPushButton(text=" ")
        self.four = QPushButton(text=" ")
        self.five = QPushButton(text=" ")
        self.six = QPushButton(text=" ")
        self.seven = QPushButton(text=" ")
        self.eight = QPushButton(text=" ")
        self.nine = QPushButton(text=" ")
        self.butts = [self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight, self.nine]
        for butt in self.butts:
            butt.setMinimumSize(QtCore.QSize(50, 50))
            butt.setMaximumSize(QtCore.QSize(50, 50))
            butt.clicked.connect(lambda: self.move(butt))
        self.main_layout.addWidget(self.label, 0, 0, 3, 1)
        self.main_layout.addWidget(self.one, 1, 0, 1, 1)
        self.main_layout.addWidget(self.two, 1, 1, 1, 1)
        self.main_layout.addWidget(self.three, 1, 2, 1, 1)
        self.main_layout.addWidget(self.four, 2, 0, 1, 1)
        self.main_layout.addWidget(self.five, 2, 1, 1, 1)
        self.main_layout.addWidget(self.six, 2, 2, 1, 1)
        self.main_layout.addWidget(self.seven, 3, 0, 1, 1)
        self.main_layout.addWidget(self.eight, 3, 1, 1, 1)
        self.main_layout.addWidget(self.nine, 3, 2, 1, 1)

        widget = QWidget()
        widget.setFixedSize(500, 500)
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    @Slot()
    def move(self, butt: QPushButton):
        if butt.text == " ":
            self.cli.send_message(self.butts.index(butt))
            #self.block_all()

    @Slot()
    def block_all(self):
        self.label.setText(" ")
        self.label.show()
        for butt in self.butts:
                butt.setDisabled()

    @Slot()
    def unblock_empty(self):
        self.label.setText("Your move")
        self.label.show()
        for butt in self.butts:
                if butt.text == " ":
                    butt.setEnabled()

    @Slot()
    def set_field(self, status: str):
        print(status)
        act, etc = status.split(";")
        if act == "show":
            for butt, txt in zip(self.butts, [int(i) for i in etc.split("_")]):
                if butt.text == "G":
                    butt.setText(txt)
        if act == "win":
            res = etc.split("_")
            player = res[-1]
            seq = res[:3]
            if self.marker == player:
                self.label.setText("You won!")
                for st in [int(i) for i in seq]:
                    self.butts[st].setStyleSheet('background-color: green;')
                    self.butts[st].show()
            else:
                self.label.setText("You loose!")
                for st in [int(i) for i in seq]:
                    self.butts[st].setStyleSheet('background-color: red;')
                    self.butts[st].show()
        #if act == "move":
            #self.unblock_empty()
        if act == "draw":
            self.label.setText("It's a draw, stay put!")
            self.label.show()
            for butt in self.butts:
                butt.setStyleSheet('background-color: red;')
                #butt.setDisabled()
                self.butts[st].show()
        if act == "you":
            self.marker = etc


class TicTacToeClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))
        self.board: Board = None

    def start(self):
        #self.board.show()
        while True:
            board_state = self.client_socket.recv(1024).decode("utf-8").rstrip()
            print(board_state)
            for bs in board_state.split(" "):
                self.board.set_field(bs)

    def send_message(self, msg):
        self.client_socket.send(bytes(msg, "utf-8"))

if __name__ == "__main__":
    client = TicTacToeClient()
    app = QApplication(sys.argv)
    board = Board(client)
    client.board = board
    client.board.show()
    client.start()