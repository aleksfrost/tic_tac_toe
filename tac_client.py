# The client code allows a player to connect to the server,
# wait for an opponent, and play the game. The client receives
# the current state of the board, makes a move, and sends that move back to the server.

import socket

from board import Board

class TicTacToeClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))

    def start(self):
        self.board = Board()
        while True:
            board_state = self.client_socket.recv(1024).decode("utf-8").split("_")
            if "wins" in board_state or "draw" in board_state:
                break
            else:
                for _, butt, txt in zip(self.board.buttons.items(), board_state):
                    butt["text"] = txt
            move = "_".join(self.board.move)
            self.client_socket.send(bytes(move, "utf-8"))
            #self.board.block_buttons()

if __name__ == "__main__":
    client = TicTacToeClient()
    client.start()

# Client Explanation:
# Receiving Board State: The client receives updates about the game
# board from the server using recv(), which allows the player to see the current state of the game.
# Sending Moves: The player inputs a move, which is then sent to the server
# via send() for validation and processing.