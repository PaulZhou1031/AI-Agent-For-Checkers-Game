"""
This module has the Checkers Class that describes checker pieces.

We are following the javadoc docstring format which is:
@param tag describes the input parameters of the function
@return tag describes what the function returns
@raise tag describes the errors this function can raise
"""
from Move import Move
from copy import deepcopy
from copy import copy
class Checker():
    def __init__(self, color, location):
        """
        Initializes Checker pieces
        @param color: stores the color of this checker
        @param location: has the location of this checker
        """
        self.color = color
        self.row = location[0] # stores the row of the piece
        self.col = location[1] # stores the col of the piece
        self.is_king = False # stores if this piece is king or not

    def get_possible_moves(self,board):
        """
        Get all possible moves of this checker. These moves may be filtered in the context of the board.
        @param board: has the current state of the board
        @return result: a list of Move objects that describes the possible move for this checker
        """
        # determine possible move directions from the color of this checker
        # explore_direction: a list of tuples of coordinates of possible move
        # - current position.
        # e.g. now we have a checker piece at 1,1 black. It can move to 2,0
        # and 2,2. explore_direction will be [(1,-1), (1, 1)]
        if self.color == '.':
            return []
        directions = {"W":[(-1,-1),(-1,1)],"B":[(1,-1),(1,1)]}
        result = []
        multiple_jump = []
        board = copy(board)
        is_capture = False
        explore_direction = directions[self.color]
        if self.is_king:
            explore_direction.extend(directions[board.opponent[self.color]])
            # a king can go all directions
            # but do we allow fly king?
        for i in explore_direction:
            pos_x,pos_y = self.row+i[0],self.col+i[1]
            if board.is_in_board(pos_x,pos_y):
                if board.board[pos_x][pos_y].color == '.':
                    result.append(Move([(self.row,self.col),(pos_x,pos_y)]))
        # save_color = board.board[self.row][self.col].color
        save_color = board.board[self.row][self.col].color
        board.board[self.row][self.col].color = "."
        self.binary_tree_traversal(self.row,self.col,multiple_jump, board, explore_direction, [],save_color)
        # filter out those at margins
        if multiple_jump != []:
            is_capture = True
            result = []
        for jump in multiple_jump:
            jump.insert(0,(self.row,self.col))
            result.append(Move(jump))
        board.board[self.row][self.col].color = save_color
        return result, is_capture

    def binary_tree_traversal(self,pos_x,pos_y,multiple_jump,board,direction,move,self_color):
        """
        Internal helper function for get_possible_moves. Students should not use this.
        This function handles the move chain if multiple jumps are possible for this checker piece
        @param pos_x: x coordinate of the checker piece whose move is being explored
        @param pos_y: y coordinate of the checker piece whose move is being explored
        @param multiple_jump: a list of the current multiple jump moves found
        @param board: current state of the board
        @param direction: current direction to explore in
        @param move: current move chain being explored
        """
        for i in direction:
            temp_x, temp_y = pos_x + i[0], pos_y + i[1]
            if board.is_in_board(temp_x,temp_y) and \
                    board.board[temp_x][temp_y].color == board.opponent[self_color] \
                    and board.is_in_board(temp_x+i[0],temp_y+i[1]) and board.board[temp_x + i[0]][temp_y+ i[1]].color == '.':
                break
        else:
            if move != []:
                multiple_jump.append(move)
            return
        for i in direction:
            temp_x,temp_y = pos_x + i[0],pos_y + i[1]
            if board.is_in_board(temp_x,temp_y) and board.board[temp_x][temp_y].color == board.opponent[self_color]:

                if board.is_in_board(pos_x + i[0]+i[0],pos_y + i[1]+i[1]) and board.board[pos_x + i[0] + i[0]][pos_y + i[1] + i[1]].color == '.':
                    backup = board.board[pos_x + i[0]][pos_y + i[1]].color
                    board.board[pos_x + i[0]][pos_y + i[1]].color = "."
                    move.append((pos_x + i[0]+i[0],pos_y + i[1]+i[1]))
                    self.binary_tree_traversal(pos_x + i[0] + i[0],pos_y + i[1] + i[1],multiple_jump,board,direction,list(move),self_color)
                    move.pop()
                    board.board[pos_x + i[0]][pos_y + i[1]].color = backup
    # def get_valid_moves(self, board):
    #     """
    #
    #     :param board: list of lists (2d array)
    #     :return: list of Moves
    #     """
    #     board_row = len(board)
    #     board_col = len(board[0])
    #     result = []
    #     possible_moves = self.get_possible_moves(board_row,board_col)
    #     print("psm:",possible_moves)
    #     for i in possible_moves:
    #         if board[i[0]][i[1]].color == ".":
    #             result.append(Move((self.row,self.col),(i[0],i[1])))
    #             # if possible positions are all empty then we can go those two
    #         else:
    #             # if those positions are nt empty:
    #             # if the position is occupied by:
    #             #      A) Our pieces: then we can't move it
    #             #      B) Opponent pieces: then we must jump over it and eliminate that piece
    #             if board[i[0]][i[1]].color == self.color:
    #                 continue
    #             else:
    #                 return [Move((self.row, self.col), (i[0],i[1]))]
    # 
    #     return result


    # def make_move(self):
    #     pass

    def become_king(self):
        """
        Changes checker piece to king
        """
        self.is_king = True

    def become_man(self):
        """
        Changes to regular piece
        """
        self.is_king = False

    def get_color(self):
        """
        Returns 'W' or 'B' for the color of this checker piece
        @return self.color: variable with the color of this piece
        """
        return self.color

    def get_location(self):
        """
        Returns a tuple of row and column of this piece
        @return self.row, self.col: row coordinate variable and col coordinate variable
        """
        return self.row, self.col


# class Move():
#     def __init__(self,source, destination):
#         self.source = source
#         self.destination = destination
#         self.passby = []
# 
#     def add_pass_by(self,passby):
#         self.passby.append(passby)
# 
#     def to_string(self):
#         if not self.passby:
#             return "{}{}-{}{}".format(self.source[0], self.source[1], self.destination[0], self.destination[1])
#         else:
#             temp = "{}{}".format(self.source[0],self.source[1])
#             for p in self.passby:
#                 temp += "x{}{}".format(p[0],p[1])
#             temp += "X{}{}".format(self.destination[0], self.destination[1])
#             return temp


