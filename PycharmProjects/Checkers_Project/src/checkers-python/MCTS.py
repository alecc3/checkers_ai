import copy
from BoardClasses import *
from random import choice


class MonteCarlo:

    def __init__(self, myBoard, myPlayer, **kwargs):
        self.board = myBoard
        self.player = myPlayer
        self.states = []
        self.wins = {}
        self.plays = {}
        self.stop_criteria = 1
        self.max_moves = 10

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        for _ in range(self.stop_criteria):
            self.run_simulation()

        for board in self.plays.keys():
            print(self.wins[board], self.plays[board])


    def run_simulation(self):
        visited_boards = set()
        board_copy = copy.deepcopy(self.board)

        expand = True
        for _ in range(self.max_moves):

            moves = []
            all_moves = board_copy.get_all_possible_moves(self.player)
            for i in all_moves:
                for j in i:
                    moves.append(j)

            if moves:
                move = choice(moves)
                board_copy.make_move(move, self.player)

            print(self.player)
            print(moves)
            board_copy.show_board()

            if expand and board_copy not in self.plays:
                expand = False
                self.plays[board_copy] = 0
                self.wins[board_copy] = 0

            visited_boards.add((self.player, board_copy))

            winner = board_copy.is_win(self.player)
            if winner != 0:
                print("WINNER")
                break

        for player, board in visited_boards:
            if (player, board) not in self.plays:
                continue
            print("hello")
            self.plays[(player, board)] += 1
            if player == winner:
                self.wins[(player, board)] += 1
