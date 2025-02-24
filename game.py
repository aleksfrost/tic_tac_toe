# The GameRoom class is where the actual game between two players takes place.
# This class handles game logic, communication between players, and the flow of the game
# (turns, checking for a winner, etc.).


class GameRoom:
    def __init__(self, player1_socket, player2_socket):
        self.board = []
        self.players = [(player1_socket, "X"), (player2_socket, "O")]
        self.current_player = 0
        self.make_board()

    def send_board_to_players(self):
        temp = []
        for row in self.board:
            temp.extend(row)
        board_state = "_".join(row)
        for player_socket, _ in self.players:
            player_socket.send(bytes(board_state, "utf-8"))

    def make_board(self):
        [self.board.append([" " for _ in range(3)]) for _ in range(3)]


    def handle_game(self):
        game_over = False
        while not game_over:
            current_socket, current_marker = self.players[self.current_player]
            opponent_socket, _ = self.players[(self.current_player + 1) % 2]

            self.send_board_to_players()

            #current_socket.send(bytes("Your move: ", "utf-8"))
            move = current_socket.recv(1024).decode("utf-8").splt("_")
            print(move)

            i, j = move
            if self.board[i][j] != " ":
                self.board[i][j] = current_marker
                if self.board.checkWinner(current_marker):
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
                self.send_board_to_players()

    def checkWinner(self, marker):
        for line in range(3):
            #lines
            if all([self.board[(line, col)] == marker for col in range(3)]):
                return True
            #rows
            if all([self.board[(col, line)] == marker for col in range(3)]):
                return True
        #croix down
        if all([self.board[(col, col)] == marker for col in range(3)]):
            return True
        #croix up
        if all([self.board[(2 - col, col)] == marker for col in range(3)]):
            return True

    def is_draw(self):
        if all([[butt in ["X", "O"] for butt in row] for row in self.board]):
            return True


# Move Validation: It checks if the move is valid (i.e., it’s a number between 1 and 9, and the position hasn’t already been taken). If valid, the board is updated.
# Winner or Draw: After each move, it checks whether the player has won or if the game has ended in a draw. If so, both players are informed, and the game ends.
# Turn Switching: If the game isn’t over, the turn switches to the next player using self.current_player = (self.current_player + 1) % 2.