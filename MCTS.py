from hexboard import HexBoard
import datetime
from copy import deepcopy
import random
import numpy as np

class Node:
    def __init__(self, Board = None, pa = None, vis=0.0, rew = 0.0):
        self.state = Board
        self.parent = pa
        self.visits = vis
        self.reward = rew
        self.children = []
        self.unusedmoves = getLegalMoves(self.state)

    def addChildren(self, ls, move):
        if ls not in self.children:
            self.children.append(ls)
            self.unusedmoves.remove(move)

    def isLeaf(self):
        if not self.children:
            return True
        else:
            return False

##  Checks if Node in Tree has tried all possible moves atleast once      
    def isExpanded(self):
        if self.unusedmoves == []:
            return True
        else:
            return False

    def isTerminal(self):
        if self.state.finished():
            return True
        else:
            return False
    
##  Handles Exploration vs. Exploitation. Therefore Nodes get selected by
##  already known outcome and C adds a possibility Bonus for unexplored Nodes        
    def UCT(self):
        legalchildren = [child for child in self.children]
        if legalchildren == []:
            return self
        spec_child = sorted(legalchildren, key = lambda x: x.reward/x.visits + np.sqrt(np.log(self.visits)/x.visits))[-1]
        return spec_child

##  Container for Nodes
class SearchTree():
    def __init__(self, r=None):
        self.root = Node(r)
        #self.Tree = [self.root]


def getLegalMoves(board):
    height = len(board.board)
    width = len(board.board[0])
    if board.zug == 0:
        legalmoves = [(i, j) for i in range(height) for j in range(width)]
    else:
        legalmoves = [(i, j) for i in range(height) for j in range(width) if board.board[i][j] == 0]
    return legalmoves

def copy(Board):
    m = len(Board.board[0])
    a, b = Board.zug, Board.no_filled
    newBoard = HexBoard(m, m)
    newBoard.board = deepcopy(Board.board)
    newBoard.starter = Board.starter
    newBoard.win = Board.win
    newBoard.zug = a
    newBoard.lastmove = Board.lastmove
    newBoard.no_filled = b
    newBoard.swap = Board.swap
    return newBoard 

def Expand(node, Board,
           #Tree
          ):
    Board.receiveMove(random.choice(node.unusedmoves))
    newNode = Node(copy(Board), node)
    newNode.state.lastmove = deepcopy(Board.lastmove)
    node.addChildren(newNode, Board.lastmove)
    #Tree.append(newNode)
    return newNode

def Simulate(legalmoves, Board, KI):
    while not Board.finished():
        move = random.choice(legalmoves)
        Board.receiveMove(move)
        legalmoves.remove(move)
    return goalValue(Board, KI)

def goalValue(Board, KI):
    if Board.starter == KI.string:
        if Board.swap:
            if Board.winner() == 1:
                return -1
            else:
                return 1
        else:
            if Board.winner() == 1:
                return 1
            else:
                return -1
    else:
        if Board.swap:
            if Board.winner() == 1:
                return 1
            else:
                return -1
        else:
            if Board.winner() == 1:
                return -1
            else:
                return 1

def Backprop(node, R):
    node.reward += R
    node.visits += 1
    if node.parent != None:
        return node.parent
    else:
        return node

##  Selection till Node that's not terminal and not expanded
##  Expansion of selected Node, it gets expanded by one possible move of
##  untried moves and appended to Tree
##  Simulation of expanded Node
##  Backprop traverses Tree upwards till root, updating simulated outcome
##  on every Node on the trace(root within)
def MCTS(KI):
    #timelimit = datetime.timedelta(seconds = 5)
    #begin = datetime.datetime.now()
    #timelimit >= datetime.datetime.now() - begin
    S = SearchTree(KI.startState)
    cur = S.root
    last = cur
    i = 0
    while i < 10000:
        Board = copy(last.state)

        #Selection
        while last.isExpanded() and not last.isTerminal():
            last = last.UCT()
            Board.receiveMove(last.state.lastmove)
        
        #Expansion
        if last.unusedmoves and not last.isTerminal():
            last = Expand(last, Board
            #, S.Tree
            )
        
        #Simulation
        legalmoves = getLegalMoves(Board)
        R = Simulate(legalmoves, Board, KI)
        
        #Backpropagation
        while last.parent != None:
            last = Backprop(last, R)
        last = Backprop(last, R)
        i += 1
    #print(i) For debugging purpose
    '''dic = {}
    func = lambda x: x.reward/x.visits + np.sqrt(np.log(x.parent.visits)/x.visits)
    for i in S.Tree[0].children:
        dic[str(S.Tree.index(i))] = {'move': i.state.lastmove, 
                               #'children': [child.state.board for child in i.children],
                               'visits': i.visits,
                               'reward': i.reward,
                               'UCT': func(i)
                              }
    print(dic)'''
    return max(S.root.children, key = lambda x: x.visits).state.lastmove, i#, S.Tree