from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import numpy as np
import copy
import time



class MCTS_Node():
    def __init__(self, state, color, parent=None):
        self.game_state = state
        self.parent = parent
        self.color = color
        self.children = {}  # format-> move: Node
        self.total_visit = 0
        self.total_win = 0
        self.opponent = {1: 2, 2: 1}
        self.untried_moves = self.find_all_moves()

    def best_child(self):     
        try:
            return max(self.children.values(), key=lambda x: x.score())
        except:
            return self

    def score(self):
        return self.total_win / self.total_visit + math.sqrt(2) * math.sqrt(
            math.log(self.parent.total_visit) / self.total_visit)

    def find_all_moves(self):
        list_1 = self.game_state.get_all_possible_moves(self.color)
        return [x for sublist in list_1 for x in sublist]

    def expand(self):
        next_move = self.untried_moves.pop()
        self.game_state.make_move(next_move, self.color)
        child_node = MCTS_Node(copy.deepcopy(self.game_state), self.opponent[self.color], parent=self)
        self.children[next_move] = child_node
        self.game_state.undo()
        return child_node

    def back_propo(self, game_result):
        self.total_visit += 1
        if game_result == self.color:
            self.total_win += 1
        if self.parent != None:
            self.parent.back_propo(game_result)

    def helper(self, game_state, color):
        all_moves = game_state.get_all_possible_moves(color)
        returned = []
        for i in all_moves:
            for x in i:
                returned.append(x)
        return returned

    def rollout(self):
        temp = copy.deepcopy(self.game_state)
        color = self.color
        while len(self.helper(temp, color)) != 0:
            all_moves = self.helper(temp, color)
            random_move = all_moves[np.random.randint(len(all_moves))]
            temp.make_move(random_move, color)
            color = self.opponent[color]
        return temp.is_win(color)

    def tree_policy(self):
        temp = self
        while temp.game_state.is_win(self.color) == 0:
            if len(temp.untried_moves) != 0:
                return temp.expand()
            else:
                temp = temp.best_child()
        return temp




# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2
        self.count = 0
        self.timeCount = 0
    
    def search(self):
        # player_2 -> iter = 700
        iter = 0
        temp = copy.deepcopy(self.board)
        root = MCTS_Node(temp, self.color)
        t = 10
        while t >= 0:
            start = time.time()
            leaf = root.tree_policy()
            result = leaf.rollout()
            leaf.back_propo(result)
            end = time.time()
            t -= (end - start)
        best = root.best_child()
        for x in root.children.keys():
            if root.children[x] == best:
                return x

    def get_move(self, move): # First X steps will use MiniMax search to save time and increase effectiveness, then use mcts search. If time is almost end (>= 6 mins), then switch from mcts to MiniMax Search.
        start = time.time()
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        '''
        count = 0
        for i in range(self.col):
            for j in range(self.row):
                temp = self.board.board[i][j]
                if temp.get_color() == self.color:
                    count += 1
        '''
        if self.timeCount >= 360:
            moves = self.board.get_all_possible_moves(self.color)
            best_mv = moves[0][0]
            move = self.MiniMax(self.color, 3, -math.inf, best_mv, math.inf, best_mv)[1]
            self.board.make_move(move, self.color)
            return move        
        if self.count < self.col * self.p:
            moves = self.board.get_all_possible_moves(self.color)
            best_mv = moves[0][0]
            move = self.MiniMax(self.color, 3, -math.inf, best_mv, math.inf, best_mv)[1]
            self.board.make_move(move, self.color)
            self.count += 1
            time.sleep(5)
        else:
            move = self.search()
            self.board.make_move(move, self.color)
            self.count += 1
            
        self.timeCount += time.time() - start
            
        return move
        
    def score_helper(self, temp, currentColor, i, j):
        points = 0
        oppositePoints = 0
        if temp.get_color() == currentColor:
            if temp.is_king:
                points += 2000
            else:
                points += 1000
                if currentColor == 1:
                    points += (self.row - j)/self.row * 1000  # approch to king
                else:
                    points += j/self.row * 1000
        else:
            if temp.is_king:
                oppositePoints += 2000
            else:
                oppositePoints += 1000
                if currentColor == 1:
                    oppositePoints += j/self.row * 1000
                else:
                    oppositePoints += (self.row - j)/self.row * 1000
        return points, oppositePoints

    def getCurrentScore(self, currentColor):
        # king 2000
        # normal 1000
        # approch king 1000
        # final count 155 each
        points = 0
        oppositePoints = 0
        if currentColor == 1:   # better performance
            points += (self.board.white_count) * 155
            oppositePoints += (self.board.black_count) * 155
        else:
            points += (self.board.black_count) * 155
            oppositePoints += (self.board.white_count) * 155
            
        for i in range(self.col):
            for j in range(self.row):
                temp = self.board.board[i][j]
                ptadd, opadd = self.score_helper(temp, currentColor, i, j)
                points += ptadd
                oppositePoints += opadd
        return points - oppositePoints

    def MiniMax(self, color, depth, best_sc, best_mv, best_opsc, best_opmv):
        # can not pass int by reference, so we have to combine MiniMax, Min and Max together to one function
        if depth == 0:
            return self.getCurrentScore(color), best_mv
        moves = self.board.get_all_possible_moves(color)
        for move in moves:   
            for m in move:
                self.board.make_move(m, color)
                if color == self.color: # processing max
                    op_color = self.opponent[self.color]
                    best_opsc = self.MiniMax(op_color, depth-1, best_sc, best_mv, best_opsc, best_opmv)[0]
                    if best_sc < best_opsc:
                        best_sc = best_opsc
                        best_mv = m
                else:  # processing min
                    best_sc = self.MiniMax(self.color, depth-1, best_sc, best_mv, best_opsc, best_opmv)[0]
                    if best_opsc > best_sc:
                        best_opsc = best_sc
                        best_opmv = m
                self.board.undo()
        return best_sc, best_mv, best_opsc, best_opmv


    def Max(self, color, depth, best_sc, best_mv, best_opsc, best_opmv):
        # not used
        if depth == 0:
            return self.getCurrentScore(color)
        else:
            moves = self.board.get_all_possible_moves(color)
            for move in moves:
                for m in move:
                    self.board.make_move(m, color)
                    op_score = self.Min(self.board.get_all_possible_moves(self.opponent[self.color]), depth-1, best_sc, best_mv, best_opsc, best_opmv)
                    if best_sc < op_score:
                        best_sc = op_score 
                        best_mv = m
                    self.board.undo()
            return best_sc

    def Min(self, color, depth, best_sc, best_mv, best_opsc, best_opmv):
        # not used
        if depth == 0:
            return self.getCurrentScore(color)
        else:
            moves = self.board.get_all_possible_moves(color)
            for move in moves:
                for m in move:
                    self.board.make_move(m, color)
                    score = self.Max(self.color, depth-1, best_sc, best_mv, best_opsc, best_opmv)
                    if best_opsc > score:
                        best_opsc = score 
                        best_opmv = m
                    self.board.undo()
            return best_sc