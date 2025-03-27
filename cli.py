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