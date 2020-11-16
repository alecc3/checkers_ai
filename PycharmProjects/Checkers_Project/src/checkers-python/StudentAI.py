
import copy
from random import randint
from random import choice
from BoardClasses import Move
from BoardClasses import Board



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
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move
    '''

    def get_move(self,move):

        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        MCTS = MonteCarlo(self.board, self.color)
        move = MCTS.get_move()
        self.board.make_move(move, self.color)

        return move



class MonteCarlo:

    def __init__(self, myBoard, myPlayer, sc=100):
        self.board = myBoard
        self.player = myPlayer
        self.opponent = {1: 2, 2: 1}
        self.wins = {}              # key:move, value:number of wins for the move
        self.plays = {}             # key:move, value:number of simulations for the move
        self.stop_criteria = sc     # number of total simulations

    def get_move(self):
        # run a number of simulations, calculate the probability of wins/plays,
        # and return a move with the highest win ratio
        for _ in range(self.stop_criteria):
            self.run_simulation()

        # DEBUG PRINTING
        #for move in self.plays:
        #    print(move, self.wins[move], self.plays[move], self.wins[move]/self.plays[move] )

        # create a dictionary of all the original/available moves from the initial state
        valid_moves = {}
        moves = self.board.get_all_possible_moves(self.player)
        for i in moves:
            for j in i:
                valid_moves[j] = 0

        # for all the moves in valid_moves, calculate the probabilities,
        # and put the result in the valid_moves dictionary
        for move1 in valid_moves:
            for move2 in self.plays:
                if move1[0] == move2[0] and move1[1] == move2[1]:
                    valid_moves[move1] = self.wins[move2]/self.plays[move2]

        # DEBUG PRINTING
        #for m in valid_moves:
        #    print(m, valid_moves[m])

        # choose the move with the highest probability from valid_moves
        best_move = max(valid_moves, key=valid_moves.get)
        return best_move


    def run_simulation(self):
        visited_boards = set()
        board_copy = copy.deepcopy(self.board)

        expand = True
        winner = 0
        while True:

            # randomly pick a move for ourself from all possible moves
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

            # check whether the move is already in the "plays" dictionary
            is_in = False
            for p in self.plays:
                if chosen_move[0] == p[0] and chosen_move[1] == p[1]:
                    is_in = True

            # if we have not expanded in this simulation and the move is not in the dictionary
            # add the move in the dictionary (create a node)
            if expand and not is_in:
                expand = False
                self.plays[chosen_move] = 0
                self.wins[chosen_move] = 0
            visited_boards.add(chosen_move)

            # check if winner after making a move
            winner = board_copy.is_win(self.player)
            if winner != 0:
                break

            # randomly pick a move for the opponent from all possible move
            opp_moves = []
            all_moves = board_copy.get_all_possible_moves(self.opponent[self.player])
            for i in all_moves:
                for j in i:
                    opp_moves.append(j)
            if opp_moves:
                move = choice(opp_moves)
                board_copy.make_move(move, self.opponent[self.player])
            #board_copy.show_board()

            # check if winner after making a move
            winner = board_copy.is_win(self.opponent[self.player])
            if winner != 0:
                break

        # for all the moves in visited_boards
        # if the move is in the dictionary, increase the number of simulations
        # if the move led to a win, increase the number of wins
        for move1 in visited_boards:
            for move2 in self.plays:
                if move1[0] == move2[0] and move1[1] == move2[1]:
                    self.plays[move2] += 1
                    if self.player == winner:
                        self.wins[move2] += 1
