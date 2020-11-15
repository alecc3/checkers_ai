import copy
from BoardClasses import *
from random import choice


class MonteCarlo:

    def __init__(self, myBoard, myPlayer, **kwargs):
        self.board = myBoard
        self.player = myPlayer
        self.opponent = {1: 2, 2: 1}
        self.states = []
        self.wins = {}
        self.plays = {}
        self.stop_criteria = 100

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        for _ in range(self.stop_criteria):
            self.run_simulation()

        for move in self.plays.keys():
            print(move, self.wins[move], self.plays[move])


    def run_simulation(self):
        visited_boards = set()
        board_copy = copy.deepcopy(self.board)

        expand = True
        winner = 0
        while True:

            # randomly pick a move for ourself
            my_moves = []
            chosen_move = None
            all_moves = board_copy.get_all_possible_moves(self.player)
            for i in all_moves:
                for j in i:
                    my_moves.append(j)
            if my_moves:
                chosen_move = choice(my_moves)
                board_copy.make_move(chosen_move, self.player)
            #board_copy.show_board()

            if expand and chosen_move not in self.plays:
                expand = False
                self.plays[chosen_move] = 0
                self.wins[chosen_move] = 0
            visited_boards.add(chosen_move)

            winner = board_copy.is_win(self.player)
            if winner != 0:
                break

            # randomly pick a move for the opponent
            opp_moves = []
            all_moves = board_copy.get_all_possible_moves(self.opponent[self.player])
            for i in all_moves:
                for j in i:
                    opp_moves.append(j)
            if opp_moves:
                move = choice(opp_moves)
                board_copy.make_move(move, self.opponent[self.player])
            #board_copy.show_board()

            winner = board_copy.is_win(self.opponent[self.player])
            if winner != 0:
                break

        for move in visited_boards:
            if move not in self.plays:
                continue
            self.plays[move] += 1
            if self.player == winner:
                self.wins[move] += 1
