
import copy
from random import randint
from random import choice
from MCTS import MonteCarlo
from BoardClasses import Move
from BoardClasses import Board




#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    '''
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)

        opponent = 2 if self.color == 1 else 1

        # check whether m capture an opponent piece or not
        # by calculating the count of opponent's piece
        good_move = []
        for p in moves:
            for m in p:
                board_copy = copy.deepcopy(self.board)

                if opponent == 2:       # if opponent is white
                 counts_before = board_copy.white_count
                elif opponent == 1:     # if opponent is black
                    counts_before = board_copy.black_count

                board_copy.make_move(m, self.color)

                if opponent == 2:       # if opponent is white
                    counts_after = board_copy.white_count
                elif opponent == 1:     # if opponent is black
                    counts_after = board_copy.black_count

                # add move to good_move if the move captures an opponent piece
                if counts_after < counts_before:
                    good_move.append(m)


        if len(good_move) == 0:
            index = randint(0,len(moves)-1)
            inner_index =  randint(0,len(moves[index])-1)
            move = moves[index][inner_index]
        else:
            move = choice(good_move)

        self.board.make_move(move,self.color)
        return move
    '''

    def get_move(self,move):

        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        MCTS = MonteCarlo(self.board, self.color)
        MCTS.get_play()

        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0, len(moves) - 1)
        inner_index = randint(0, len(moves[index]) - 1)
        move = moves[index][inner_index]
        #self.board.make_move(move, self.color)
        return move



