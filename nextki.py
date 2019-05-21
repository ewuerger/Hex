import random
import datetime
from unsymmetric import unsymmetric
from hexboard import HexBoard
from MCTS import MCTS, getLegalMoves, copy

# AI moves randomly during his turn without swapping, except for 1x1 Game
## Tournamentmode
class HexKI():
    def __init__(self, m, n, mode, strat, board):
        self.height = m
        self.width = n
        self.mode = mode
        self.strategy = strat
        self.startState = board
        self.swap = False
        self.move = None
       
    def calculateMove(self):
        if self.strategy == 'MCTS':
            if self.startState.zug == 1:
                self.swapp()
                print(self.move)
                return self.swap
            else:
                self.move = MCTS(self)[0]
                print(self.move)
                return True
        elif self.strategy == 'random':
            self.move = random.choice(getLegalMoves(self.startState))
            return True
        elif self.strategy == 'unsymmetric':
            self.legalmoves = getLegalMoves(self.startState)
            if self.startState.zug >= 1:
                self.unsymmetricMove()
                if self.move != None:
                    i, j = self.move
                    if self.startState.board[i][j] != 0:
                        self.move = random.choice(self.legalmoves)
                    return True
                else:
                    self.move = random.choice(self.legalmoves)
                    return False
            else:
                self.move = random.choice(self.legalmoves)
                return True
            self.move = random.choice(self.legalmoves)
            return False

    def swapp(self):
        curBoard = copy(self.startState)
        self.startState = HexBoard(self.height, self.width)
        self.move = MCTS(self)[0]
        i, j = self.move
        if curBoard.board[i][j] != 0:
            self.swap = True
        self.startState = curBoard

    def nextMove(self):
        return self.move

    def receiveMove(self, move):
        self.startState.receiveMove(move)

    def unsymmetricMove(self):
        self.move = unsymmetric(self.height, self.width, self.startState.lastmove)