import random
import copy

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board in a list

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, player):
        if self.board[square] == ' ':
            self.board[square] = player
            return True
        return False

    def current_winner(self):
        # Check rows
        for row in range(3):
            if self.board[row*3] == self.board[row*3+1] == self.board[row*3+2] != ' ':
                return self.board[row*3]
        # Check columns
        for col in range(3):
            if self.board[col] == self.board[col+3] == self.board[col+6] != ' ':
                return self.board[col]
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return self.board[2]
        return None

    def is_full(self):
        return ' ' not in self.board

    def is_terminal(self):
        return self.current_winner() is not None or self.is_full()

    def evaluate(self):
        winner = self.current_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        else:
            return 0

    def copy(self):
        new_game = TicTacToe()
        new_game.board = self.board.copy()
        return new_game
