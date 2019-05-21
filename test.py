import numpy as np
import random
import datetime
import unsymmetric
from hexboard import HexBoard
from MCTS import MCTS, getLegalMoves, copy, goalValue
from nextki import HexKI
from Game import Game


Game(6,6,'inter')

'''
i = 0
while i < 10000:
      i += 1
      KI = HexKI(3,3,'MCTS',HexBoard(3,3))
      legalmoves = getLegalMoves(KI.startState)
      while not KI.startState.finished():
            move = random.choice(legalmoves)
            KI.startState.receiveMove(move)
            legalmoves.remove(move)
            print(KI.startState.board)
      
      print(KI.startState.winner(),
            goalValue(KI.startState))

move, i, Tree = MCTS(KI)
dic = {}
func = lambda x: x.reward/x.visits + np.sqrt(np.log(x.parent.visits)/x.visits)
for i in Tree[0].children:
    dic[str(Tree.index(i))] = {'board': i.state.board, 
                               #'children': [child.state.board for child in i.children],
                               'visits': i.visits,
                               'reward': i.reward,
                               'UCT': func(i)
                              }
print(dic)
print(move)'''