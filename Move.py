"""
This module has the Move Class which is the class which handles moves on the board.

We are following the javadoc docstring format which is:
@param tag describes the input parameters of the function
@return tag describes what the function returns
@raise tag describes the errors this function can raise
"""

class Move:
    """
    This class is used to describe the moves being made on the board.
    """
    def __init__(self,l):
        """
        Initializes Move Object
        @param l: a sequence of position that the checker pieces will take during the execution of this move
              |  |
            --------
              | X|
            --------
              |  |
            --------
              | X|
            ________
            O |  |

        In the example above, l should be [(0,0),(2,2),(0,4)]
        """
        self.seq = list(l)

    @classmethod
    def from_str(cls,s:str):
        """
        This class enables the move object to be made from a str
        @param s: string that describes the class. Eg '(0,0)-(2,2)-(0,4)'
        """
        if (s == '-1'):
            return cls([])
        else:
            sequencelist = list(map(lambda x:eval(x),s.split('-')))
            return cls(sequencelist)

    """
    :return self.seq = [(0,0),(2,2),(0,4)] -> '(0,0)-(2,2)-(0,4)'
    """
    def __str__(self):
        result = ''
        if len(self.seq) == 0:
            return '-1'
        for e in self.seq:
            result += str(e)
            result += '-'
        return result[:-1].replace(" ","")

    def __len__(self):
        return len(self.seq)

    def __repr__(self):
        return str(self)

    def __getitem__(self,i):
        return self.seq[i]

    def __setitem__(self, index, value):
        self.seq[index] = value
