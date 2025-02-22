# The client code allows a player to connect to the server,
# wait for an opponent, and play the game. The client receives
# the current state of the board, makes a move, and sends that move back to the server.

import socket

class TicTacToeClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))

    def start(self):
        while True:
            board_state = self.client_socket.recv(1024).decode("utf-8")
            print(board_state)
            if "wins" in board_state or "draw" in board_state:
                break
            move = input("Enter your move (1-9): ")
            self.client_socket.send(bytes(move, "utf-8"))

if __name__ == "__main__":
    client = TicTacToeClient()
    client.start()

# Client Explanation:
# Receiving Board State: The client receives updates about the game
# board from the server using recv(), which allows the player to see the current state of the game.
# Sending Moves: The player inputs a move, which is then sent to the server
# via send() for validation and processing.