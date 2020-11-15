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

        for board in self.plays.keys():
            print(self.wins[board], self.plays[board])


    def run_simulation(self):
        visited_boards = set()
        board_copy = copy.deepcopy(self.board)

        expand = True
        winner = 0
        while True:

            # randomly pick a move for ourself
            my_moves = []
            all_moves = board_copy.get_all_possible_moves(self.player)
            # print(all_moves)
            for i in all_moves:
                for j in i:
                    my_moves.append(j)
            if my_moves:
                move = choice(my_moves)
                board_copy.make_move(move, self.player)
            board_copy.show_board()

            if expand and board_copy not in self.plays:
                expand = False
                self.plays[board_copy] = 0
                self.wins[board_copy] = 0

            visited_boards.add(board_copy)

            win = board_copy.is_win(self.player)
            if win != 0:
                winner = win
                break

            # randomly pick a move for the opponent
            opp_moves = []
            all_moves = board_copy.get_all_possible_moves(self.opponent[self.player])
            # print(all_moves)
            for i in all_moves:
                for j in i:
                    opp_moves.append(j)
            if opp_moves:
                move = choice(opp_moves)
                board_copy.make_move(move, self.opponent[self.player])
            board_copy.show_board()

            win = board_copy.is_win(self.player)
            if win != 0:
                winner = win
                break

        print(winner)

        for board in visited_boards:
            if board not in self.plays:
                continue
            self.plays[board] += 1
            if self.player == winner:
                self.wins[board] += 1
