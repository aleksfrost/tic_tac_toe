import socket
import sys
import threading

class Board:
    def __init__(self):
        self.board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def display(self):
        return f"\n{self.board[0]} | {self.board[1]} | {self.board[2]}\n--+---+--\n{self.board[3]} | {self.board[4]} | {self.board[5]}\n--+---+--\n{self.board[6]} | {self.board[7]} | {self.board[8]}"

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
                return True
        return False

    def is_draw(self):
        return all(spot in ["X", "O"] for spot in self.board)

class TicTacToeServer:
    def __init__(self):
        self.board = Board()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(2)  # Listening for two players
        self.players = []
        self.current_player = 0

    def handle_client(self, client_socket, player_marker):
        client_socket.send(bytes(f"You are Player {player_marker}", "utf-8"))
        while True:
            self.send_board_to_all()
            move = client_socket.recv(1024).decode("utf-8")
            if move.isdigit() and int(move) in range(1, 10):
                move = int(move) - 1
                if self.board.board[move] not in ["X", "O"]:
                    self.board.update(move, player_marker)
                    if self.board.is_winner(player_marker):
                        self.send_board_to_all()
                        client_socket.send(bytes(f"Player {player_marker} wins!", "utf-8"))
                        break
                    elif self.board.is_draw():
                        self.send_board_to_all()
                        client_socket.send(bytes("It's a draw!", "utf-8"))
                        break
                    self.current_player = (self.current_player + 1) % 2
            else:
                client_socket.send(bytes("Invalid move. Try again.", "utf-8"))

    def send_board_to_all(self):
        for player_socket in self.players:
            player_socket.send(bytes(self.board.display(), "utf-8"))

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