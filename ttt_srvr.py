import socket
import sys
import threading
from itertools import cycle

class Board:

    def __init__(self):
        self.board = self.board()


    def board(self):
        return [str(i) for i in range(1, 10)]


    def display(self):
        print(f"""\n{self.board[0]} | {self.board[1]} | {self.board[2]}\n
                    --+---+--
                    \n{self.board[3]} | {self.board[4]} | {self.board[5]}\n
                    --+---+--
                    \n{self.board[6]} | {self.board[7]} | {self.board[8]}""")
        return self.board

    def update(self, position, marker):
        self.board[position] = marker


    def is_winner(self, marker):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == marker:
                return combo
        return False

    def is_draw(self):
        if all(spot in ["X", "O"] for spot in self.board):
            return True

class TicTacToeServer:
    def __init__(self):
        self.board = Board()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(2)  # Listening for two players
        self.players = []
        self.current_player = 0

    def handle_client(self, client_socket, player_marker):
        client_socket.send(bytes(";".join(("you", player_marker)) + " ", "utf-8"))
        while True:
            self.send_board_to_all(";".join(("show", "_".join(self.board.board))))
            client_socket.send(bytes(";".join(("move", "Z")) + " ", "utf-8"))
            move = client_socket.recv(1024).decode("utf-8")
            move = int(move) - 1
            self.board.update(move, player_marker)
            res = self.board.is_winner(player_marker)
            if res:
                res.append([player_marker])
                self.send_board_to_all(";".join(("win", res)))
                break
            elif self.board.is_draw():
                self.send_board_to_all(";".join(("draw", "Z")))
                break
            self.current_player = (self.current_player + 1) % 2

    def send_board_to_all(self, status):
        self.board.display()
        for player_socket in self.players:
            player_socket.send(bytes(status + " ", "utf-8"))
            print(status)

    def start(self):
        print("Server is waiting for players...")
        for _ in range(2):
            client_socket, address = self.server_socket.accept()
            print(f"Player connected from {address}")
            player_marker = "X" if len(self.players) == 0 else "O"
            self.players.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, player_marker)).start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()