import random
import copy
from hexboard import HexBoard
from hexgui import HexGui
from nextki import HexKI

class Game():
##  creates interface of HexGuitype expected input m, n as int and mode as string
##  Game creates HexGui, HexBoard to get and set information, starter == 1 or 2
    def __init__(self, m, n, mode='inter'):
        self.mode = mode
        self.board = HexBoard(m, n)
        self.starter = None
        self.nonstarter = None
        self.finished = False       
        self.chooseFirst()
        if self.board.zug == 0:
            self.board.starter = self.starter
        self.interface = HexGui(m, n, self)
        self.GameOn(m, n, mode)

##  choose between Players A and B who begins
##  adjust according to game mode the attributes starter and nonstarter
    def chooseFirst(self):
        if self.starter == None:
            self.starter = random.choice(['A','B'])
        if self.starter == 'A':
            if self.mode == 'human':
                self.starter = 'Human A'
                self.nonstarter = 'Human B'
            elif self.mode == 'inter':
                self.starter = 'KI'
                self.nonstarter = 'Human'
            else:
                self.starter = 'KI A'
                self.nonstarter = 'KI B'
        else:
            if self.mode == 'human':
                self.starter = 'Human B'
                self.nonstarter = 'Human A'
            elif self.mode == 'inter':
                self.starter = 'KI'
                self.nonstarter = 'Human'
            else:
                self.starter = 'KI B'
                self.nonstarter = 'KI A'

##  Player 1's turn when no of occupied cells is even
##  Player 2's turn when no of occupied cells is uneven
    def currentPlayer(self):
        if self.board.no_filled%2==0:
            if self.mode == 'inter' and self.board.zug > 0:
                self.KI.currentPlayer = self.starter
            return 1
        else:
            if self.mode == 'inter' and self.board.zug > 0:
                self.KI.currentPlayer = self.nonstarter
            return 2

##  updates HexBoard, asks Gui after turn 1 if 2nd player wants swap using
##  chooseFirst(), checks if game is over after everyturn and forces Gui to finish
##  with finish(winning Player)
    def makeMove(self, move):
        # first check if field is inhabited
        i, j = move
        if self.board.board[i][j] != 0:
            return
        self.board.receiveMove(move)
        self.interface.receiveMove(move)
        if self.board.finished():
            self.finished = True
            self.interface.finish(self.board.winner())
        #  update boards of KI's
        if self.mode == 'inter':
            self.KI.startState = copy.deepcopy(self.board)
            self.KI.lastmove = move
        if self.mode == 'ki':
            self.pc1.startState = copy.deepcopy(self.board)
            self.pc2.startState = copy.deepcopy(self.board)

##  creates HexGui
    def GameOn(self, m, n, mode):
        if mode == 'inter':
            if m != n:
                self.KI = HexKI(m,n, 'inter', 'unsymmetric', self.board)
                self.KI.string = self.starter
            else:
                self.KI = HexKI(m,n, 'inter', 'MCTS', self.board)
                self.KI.string = self.starter
            self.autorun()
        if mode == 'ki':
            if m != n:
                self.pc1 = HexKI(m,n, 'ki', 'unsymmetric', self.board)
                self.pc2 = HexKI(m,n, 'ki', 'unsymmetric', self.board)
                if self.starter == 'KI A':
                    self.pc1.string = self.starter
                    self.pc2.string = self.nonstarter
                else:
                    self.pc2.string = self.starter
                    self.pc1.string = self.nonstarter
            else:
                self.pc1 = HexKI(m,n, 'ki', 'MCTS', self.board)
                self.pc2 = HexKI(m,n, 'ki', 'MCTS', self.board)
                if self.starter == 'KI A':
                    self.pc1.string = self.starter
                    self.pc2.string = self.nonstarter
                else:
                    self.pc2.string = self.starter
                    self.pc1.string = self.nonstarter
            self.autorun2()
        else:
            pass

##  fetch board from hexboard class
    def getBoard(self):
        return list(self.board.board)

##  alternates between human and AI
    def autorun(self):
        if self.starter == 'Human':
            while self.board.win == None:
                self.interface.root.wait_variable(self.interface.uiBoard.waitVar)
                if self.board.win != None:
                    break
                self.KI.startState = self.board
                self.KI.calculateMove()
                if self.board.zug == 1 and self.KI.swap:
                    self.interface.swap_players()
                    continue
                self.makeMove(self.KI.move)
                self.interface.uiBoard.waitVar.set(False)
        else:
            self.KI.begin = True
            while self.board.win == None:
                self.KI.startState = self.board
                self.KI.calculateMove()
                self.makeMove(self.KI.move)
                if self.board.win != None:
                    break
                self.interface.uiBoard.waitVar.set(False)
                self.interface.root.wait_variable(self.interface.uiBoard.waitVar)

    def autorun2(self):
        if self.starter == 'KI A':
            while self.board.win == None:
                self.pc1.calculateMove()
                self.makeMove(self.pc1.move)
                self.interface.root.update()
                if self.board.win != None:
                    break
                self.pc2.calculateMove()
                if self.board.zug == 1 and self.pc2.swap:
                    self.interface.swap_players()
                    continue
                print('hier: '+str(self.pc2.strategy))
                self.makeMove(self.pc2.move)
                self.interface.root.update()
        else:
            while self.board.win == None:
                self.pc2.calculateMove()
                self.makeMove(self.pc2.move)
                self.interface.root.update()
                if self.board.win != None:
                    break
                self.pc1.calculateMove()
                if self.board.zug == 1 and self.pc1.swap:
                    self.interface.swap_players()
                    continue
                self.makeMove(self.pc1.move)
                self.interface.root.update()