"""
This module has the Board Class which is the class which handles the current board.

We are following the javadoc docstring format which is:
@param tag describes the input parameters of the function
@return tag describes what the function returns
@raise tag describes the errors this function can raise
"""


import copy
import re
from Move import Move
class InvalidMoveError(Exception):
    pass

class InvalidParameterError(Exception):
    pass

import Checker

class Board:
    """
    This class describes Board
    """
    opponent = {"W": "B", "B": "W"}
    def __init__(self, col,row, p):
        """
        Intializes board: 
            M = number of rows
            N = number of columns
            P = number of rows containing initial checker pieces
        Adds the white checkers and black checkers to the board based on the board variables (M,N,P)
        provided. N*P should be even to ensure that both players get the same number of checker pieces at the start

        @param row: number of rows in the board
        @param col: number of columns in the board
        @param p: number of rows to be filled with checker pieces at the start
        @return :
        @raise :
        """
        self.tie_counter = 0
        self.tie_max = 40
        self.row = row
        self.col = col
        self.p = p
        self.board = []
        self.saved_move = [ ]#self.saved_move = [Move([]),[],False]
        for row in range(self.row):
            self.board.append([])
            for col in range(self.col):
                self.board[row].append(Checker.Checker(".", [row, col]))

        self.black_count = 0
        self.white_count = 0


    def initialize_game(self):
        """
        Intializes game. Adds the white checkers and black checkers to the board based on the board variables (M,N,P)
        when the game starts
        @param :
        @return :
        @raise :
        """
        self.check_initial_variable()
        for i in reversed(range(self.p)):
            for j in range((self.p - i - 1) % 2, self.col, 2):
                # put white pieces
                i_white = self.row - self.p + i
                self.board[i_white][j] = Checker.Checker("W", [i_white, j])
                # put black pieces
                if (self.row % 2 + self.p % 2) % 2:  # row,p = even,odd or odd,even
                    if i % 2:
                        # odd row, shift to the left and attach a piece to the end when needed
                        if j - 1 >= 0:
                            self.board[i][j-1] = Checker.Checker("B", [i, j-1])
                        if j == self.col - 2 and not self.col % 2:
                            self.board[i][self.col-1] = Checker.Checker("B", [i,self.col-1])
                    else:
                        # even row, shift to the right and attach a piece to the beginning when needed
                        if j + 1 <= self.col - 1:
                            self.board[i][j+1] = Checker.Checker("B", [i,j+1])
                        if (j == self.col - 1 or j == self.col - 2) and not self.p % 2:
                            self.board[i][0] = Checker.Checker("B", [i,0])
                else:  # row,p = even,even or odd,odd
                    self.board[i][j] = Checker.Checker("B", [i,j])
                self.white_count += 1
                self.black_count += 1



    def make_move(self, move, turn):
        """
        Makes Move on the board
        @param move: Move object provided by the StudentAI, Uses this parameter to make the move on the board
        @param turn: this parameter tracks the current turn. either player 1 (white) or player 2(black)
        @return:
        @raise InvalidMoveError: raises this objection if the move provided isn't valid on the current board
        """
        temp_saved_move = [Move([]),[],False]
        if type(turn) is int:
            if turn == 1:
                turn = 'B'
            elif turn == 2:
                turn = 'W'
            else:
                raise InvalidMoveError
        move_list = move.seq
        move_to_check = []
        ultimate_start = move_list[0]
        ultimate_end = move_list[-1]
        is_start_checker_king = self.board[ultimate_start[0]][ultimate_start[1]].is_king
        past_positions = [ultimate_start]
        capture_positions = []
        for i in range(len(move_list)-1):
            move_to_check.append((move_list[i],move_list[i + 1]))
        # e.g move = Move((0,0)-(2,2)-(0,4))
        #     move_to_check = [((0,0),(2,2)),((2,2),(0,4))]
        if_capture = False
        self.tie_counter += 1
        saved_enemy_position = []
        for t in range(len(move_to_check)):
            start = move_to_check[t][0] # e.g. (0,0)
            target= move_to_check[t][1] # e.g. (2,2)
            if self.is_valid_move(start[0],start[1],target[0],target[1],turn) or (if_capture and abs(start[0]-target[0]) == 1):
                # invailid move or attempting to make a single move after capture
                self.board[start[0]][start[1]].color = "."
                self.board[target[0]][target[1]].color = turn
                self.board[target[0]][target[1]].is_king = self.board[start[0]][start[1]].is_king
                self.board[start[0]][start[1]].become_man()
                past_positions.append(target)
                if abs(start[0]-target[0]) == 2:
                    # capture happened
                    if_capture = True
                    self.tie_counter = 0
                    capture_position = ((start[0] + (target[0]-start[0])//2), (start[1] + (target[1]-start[1])//2))
                    # calculate capture position
                    capture_positions.append(capture_position)
                    # record capture position
                    saved_enemy_position.append((capture_position[0],capture_position[1],self.board[capture_position[0]][capture_position[1]].color,self.board[capture_position[0]][capture_position[1]].is_king))
                    self.board[capture_position[0]][capture_position[1]] = Checker.Checker(".", [capture_position[0], capture_position[1]])
                    # capture
                    if turn == "B":
                        self.white_count -= 1
                    else:
                        self.black_count -= 1
                if (turn == 'B' and target[0] == self.row - 1):# and not self.board[target[0]][target[1]].is_king):
                    if not is_start_checker_king:
                        temp_saved_move[2] = True
                    self.board[target[0]][target[1]].become_king()
                    #self.saved_move[2] = True
                    if not is_start_checker_king:
                        break

                elif (turn == 'W' and target[0] == 0):# and not self.board[target[0]][target[1]].is_king):
                    if not is_start_checker_king:
                        temp_saved_move[2] = True
                    self.board[target[0]][target[1]].become_king()
                     #self.saved_move[2] = True
                    if not is_start_checker_king:
                        break
                else:
                    temp_saved_move[2] = False #self.saved_move[2] = False

            else:
                for failed_capture in capture_positions:
                    # recover failed captures
                    self.board[failed_capture[0]][failed_capture[1]] = Checker.Checker(self.opponent[turn],[failed_capture[0],failed_capture[1]])
                for failed_position in past_positions:
                    # recover failed moves
                    self.board[failed_position[0]][failed_position[1]] = Checker.Checker(".", [failed_position[0],failed_position[1]])
                self.board[ultimate_start[0]][ultimate_start[1]] = Checker.Checker(turn, [ultimate_start[0],ultimate_start[1]])
                raise InvalidMoveError

        temp_saved_move[0] = copy.deepcopy(move) #self.saved_move[0] = copy.deepcopy(move)
        temp_saved_move[1] = saved_enemy_position #self.saved_move[1] = saved_enemy_position
        self.saved_move.append(temp_saved_move)
    def is_in_board(self,pos_x,pos_y):
        """
        Checks if the coordinate provided is in board. Is an internal function
        @param pos_x: x coordinte of the object to check for
        @param pos_y: y coordinte of the object to check for
        @return: a bool to describe if object is in the board or not
        @raise:
        """
        return pos_x >= 0 and pos_x < self.row and pos_y >= 0 and pos_y < self.col

    def is_valid_move(self, chess_row, chess_col, target_row, target_col, turn):
        """
        checks if a proposed move is valid or not.
        @param chess_row: row of the object whose move we are checking
        @param chess_col: col of the object whose move we are checking
        @param target_row: row where the object would end up
        @param target_col: col where the object would end up
        @param turn: tracks turn player 1(white) or player 2(black)
        @return: a bool which is True if valid, False otherwise
        @raise :
        """
        if target_row < 0 or target_row >= self.row or target_col < 0 or target_col >= self.col:
        # move out of the board
            return False
        if not self.board[target_row][target_col].color == ".":
        # target position is not empty
            return False
        if not self.board[chess_row][chess_col].color == turn:
        # there must be a chessman at that position
            return False
        diff_col = target_col - chess_col # difference in col number
        diff_row = target_row - chess_row # difference in row number
        if abs(diff_col) != abs(diff_row):
        # each move has to be 1,1 or 2,2
            return False
        chess_being_moved = self.board[chess_row][chess_col]
        if diff_row == 1 and diff_col == 1 : # down, right: king, black
            return chess_being_moved.is_king or chess_being_moved.color == "B"
        if diff_row == 1 and diff_col == -1 : # down, left: king, black
            return chess_being_moved.is_king or chess_being_moved.color == "B"
        if diff_row == -1 and diff_col == 1 : # up, right: king, red
            return chess_being_moved.is_king or chess_being_moved.color == "W"
        if diff_row == -1 and diff_col == -1 : # up, left: king, red
            return chess_being_moved.is_king or chess_being_moved.color == "W"
        if diff_row == 2 and diff_col == 2: # down, right, capture: king, black
            return (chess_being_moved.is_king or chess_being_moved.color == "B") and self.board[chess_row + 1][chess_col + 1].color != turn and self.board[chess_row + 1][chess_col + 1].color != "."
        if diff_row == 2 and diff_col == -2: # down, left, capture: king, black
            return (chess_being_moved.is_king or chess_being_moved.color == "B") and self.board[chess_row + 1][chess_col - 1].color != turn and self.board[chess_row + 1][chess_col - 1].color != "."
        if diff_row == -2 and diff_col == 2:  # up, right, capture: king, red
            return (chess_being_moved.is_king or chess_being_moved.color == "W") and self.board[chess_row - 1][chess_col + 1].color != turn and self.board[chess_row - 1][chess_col + 1].color != "."
        if diff_row == -2 and diff_col == -2:  # up, left, capture: king, red
            return (chess_being_moved.is_king or chess_being_moved.color == "W") and self.board[chess_row - 1][chess_col - 1].color != turn and self.board[chess_row - 1][chess_col - 1].color != "."
        return False




    def get_all_possible_moves(self,color):
        """
        this function returns the all possible moves of the player whose turn it is
        @param color: color of the player whose turn it is
        @return result: a list of Move objects which describe possible moves
        @raise :
        """
        result = []
        if type(color) is int:
            if color == 1:
                color = 'B'
            elif color == 2:
                color = 'W'
        is_capture = False
        temp = 0
        for row in range(self.row):
            for col in range(self.col):
                checker = self.board[row][col]
                if checker.color == color:
                    moves,is_capture = checker.get_possible_moves(self) # calls checker class's get possible moves and filters those moves down
                    if temp == 0 and not is_capture:
                        if moves:
                            result.append(moves)
                    elif temp == 0 and is_capture:
                        result = []
                        temp = 1
                        if moves:
                            result.append(moves)
                    elif temp == 1 and is_capture:
                        if moves:
                            result.append(moves)
        # if is_capture:
        #     for moves in result:
        #         for move in moves:
        #             if len(move.seq) <= 2:
        #                 moves.remove(move)


        return result

    def is_win(self,turn):
        """
        this function tracks if any player has won
        @param :
        @param :
        @return :
        @raise :
        """
        if turn == "W":
            turn = 2
        elif turn == "B":
            turn =  1
        if self.tie_counter >= self.tie_max:
            return -1
        W_has_move = True
        B_has_move = True
        if len(self.get_all_possible_moves(1)) == 0:
            if turn != 1:
                B_has_move = False
        elif len(self.get_all_possible_moves(2)) == 0:
            if turn != 2:
                W_has_move = False

        if W_has_move and not B_has_move:
            return 2
        elif not W_has_move and B_has_move:
            return 1

        W = True
        B = True

        for row in range(self.row):
            for col in range(self.col):
                checker = self.board[row][col]
                if checker.color == 'W':
                    W = False
                elif checker.color == 'B':
                    B = False
                if not W and not B:
                    return 0
        if W:
            return 2
        elif B:
            return 1
        else:
            return 0

    def show_board(self,fh=None):
        """
        prints board to console or to file
        @param fh: file object, incase we need to print to file
        @return :
        @raise :
        """
        print("   ",end="",file=fh)
        print(*range(0,self.col),sep="  ",file=fh)
        # index for debugging easily
        for i, row in enumerate(self.board):
            print(i, end="",file=fh)
            # index for debugging easily
            for j, col in enumerate(row):
                king = self.board[i][j].is_king
                if king:
                    print("%3s" % str(self.board[i][j].get_color()).upper(), end="",file=fh)
                else:
                    print("%3s" % str(self.board[i][j].get_color()).lower(), end = "",file=fh)
                # print("%3s" % str(self.board[i][j]), end="")
            print(file=fh)
        print('----------------------',file=fh)

    def check_initial_variable(self):
        """
        Checks the integrity of the initial board variables provided (M,N,P,Q)
        @param :
        @param :
        @return :
        @raise InvalidParameterError: raises this exception if there is a problem with the provided variables
        """
        # Q > 0
        if self.row - 2 * self.p <= 0:
            raise  InvalidParameterError("Q <= 0")
        # M = 2P + Q
        elif self.row != 2 * self.p + (self.row - 2 * self.p):
            raise InvalidParameterError("M != 2P + Q")
        # N*P is even
        elif self.col * self.p % 2 != 0:
            raise InvalidParameterError("N*P is odd -- must be even")

    def check_initial_variable(self):
        """
        Checks the integrity of the initial board variables provided (M,N,P,Q)
        @param :
        @param :
        @return :
        @raise InvalidParameterError: raises this exception if there is a problem with the provided variables
        """
        # Q > 0
        if self.row - 2 * self.p <= 0:
            raise  InvalidParameterError("Q <= 0")
        # M = 2P + Q
        elif self.row != 2 * self.p + (self.row - 2 * self.p):
            raise InvalidParameterError("M != 2P + Q")
        # N*P is even
        elif self.col * self.p % 2 != 0:
            raise InvalidParameterError("N*P is odd -- must be even")

    def undo(self):
        if self.saved_move != []:
            temp_saved_move = self.saved_move[-1]
            original_point = temp_saved_move[0][0]
            target_point = temp_saved_move[0][-1]

            
 #           original_point = self.saved_move[0][0]
 #           target_point = self.saved_move[0][-1]
            self.board[original_point[0]][original_point[1]].color = self.board[target_point[0]][target_point[1]].color
            if temp_saved_move[2]: #self.saved_move[2]: #if became king in that move, cancel that
                self.board[original_point[0]][original_point[1]].is_king = False
            else:
                self.board[original_point[0]][original_point[1]].is_king = self.board[target_point[0]][target_point[1]].is_king
            if target_point != original_point:
                self.board[target_point[0]][target_point[1]].color = "."
                self.board[target_point[0]][target_point[1]].is_king = False
            for saved_enemy in temp_saved_move[1]:#self.saved_move[1]:
                x,y,c,k = saved_enemy
                self.board[x][y].color = c
                self.board[x][y].is_king = k
            self.tie_counter -= 1
            self.saved_move.pop(-1)
        else:
            raise Exception("Cannot undo operation")
        self.black_count = 0
        self.white_count = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j].color=="W":
                    self.white_count += 1
                elif self.board[i][j].color == "B":
                    self.black_count += 1






if __name__ == "__main__":


    b=Board(7,7,2)
    b.board[1][3] = Checker.Checker("W", [1, 3])


    b.show_board()
    m = b.get_all_possible_moves("W")[0][0]
    b.make_move(m,"W")
    b.show_board()
    m = b.get_all_possible_moves("W")[0][0]
    b.make_move(m,"W")
    b.show_board()
    m = b.get_all_possible_moves("W")[0][0]
    b.make_move(m,"W")
    b.show_board()
    print("Undo")
    b.undo()
    b.show_board()
    print("Undo")
    b.undo()
    b.show_board()
    print("Undo")
    b.undo()
    b.show_board()


