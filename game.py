# The GameRoom class is where the actual game between two players takes place.
# This class handles game logic, communication between players, and the flow of the game
# (turns, checking for a winner, etc.).

from board import Board


class GameRoom:
    def __init__(self, player1_socket, player2_socket):
        self.board = Board()
        self.players = [(player1_socket, "X"), (player2_socket, "O")]
        self.current_player = 0

#__init__(): Initializes a new game room with two players. The players list stores
# each player’s socket and their respective marker (“X” or “O”). The current_player is used to track whose turn it is.

#Player Sockets: Each player has a socket connection. This allows the server to send and receive data (like moves) from the client.

    def send_board_to_players(self):
        board_state = self.board.display()
        for player_socket, _ in self.players:
            player_socket.send(bytes(board_state, "utf-8"))

#send_board_to_players(): Sends the current state of the board to both players.
# The board is displayed after each move to keep both players updated.

    def handle_game(self):
        game_over = False
        while not game_over:
            current_socket, current_marker = self.players[self.current_player]
            opponent_socket, _ = self.players[(self.current_player + 1) % 2]

            self.send_board_to_players()

            current_socket.send(bytes("Your move: ", "utf-8"))
            move = current_socket.recv(1024).decode("utf-8")

#handle_game(): This is the core of the game. It runs in a loop until the game is over.
# It alternates between players, prompting each player for their move and processing it.
#Player Turns: The current player is prompted to make a move using recv(), which listens
# for data from the player’s socket. The move is then processed, and the board is updated.

            if move.isdigit() and int(move) in range(1, 10):
                move = int(move) - 1
                if self.board.board[move] not in ["X", "O"]:
                    self.board.update(move, current_marker)
                    if self.board.is_winner(current_marker):
                        self.send_board_to_players()
                        current_socket.send(bytes(f"Player {current_marker} wins!", "utf-8"))
                        opponent_socket.send(bytes(f"Player {current_marker} wins!", "utf-8"))
                        game_over = True
                    elif self.board.is_draw():
                        self.send_board_to_players()
                        current_socket.send(bytes("It's a draw!", "utf-8"))
                        opponent_socket.send(bytes("It's a draw!", "utf-8"))
                        game_over = True
                    else:
                        self.current_player = (self.current_player + 1) % 2
                else:
                    current_socket.send(bytes("Invalid move. Try again.", "utf-8"))
            else:
                current_socket.send(bytes("Invalid move. Try again.", "utf-8"))

# Move Validation: It checks if the move is valid (i.e., it’s a number between 1 and 9, and the position hasn’t already been taken). If valid, the board is updated.
# Winner or Draw: After each move, it checks whether the player has won or if the game has ended in a draw. If so, both players are informed, and the game ends.
# Turn Switching: If the game isn’t over, the turn switches to the next player using self.current_player = (self.current_player + 1) % 2.