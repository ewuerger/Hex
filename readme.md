# Hex Game with Monte Carlo Tree Search and Unsymmetric play



Welcome to our summer project for closing computational mathematics in 2016. Credits for Nakhi and Martin who both worked with me on the board and GUI.

![alt text](https://github.com/ewuerger/Hex/raw/master/pictures/Win.png?raw=True)

Over 2 sprints, each 2 weeks long, we developped this Hex Game script. 
In the first: The core of the game, i.e. all functionality such that 2 humans can play against each other.
And in the last one we tried ourselves on implementing a solver/ai. The ai needed to be unbeatable on atleast 3x3 playfields to be able to take the final exam. With a simple implementation of the Monte Carlo Tree Search algorithm this ai is unbeatable on 5x5 playfields. Bigger ones start to need heuristics or a machine learning approach coupled with MCTS to improve play.

## Usage
To use this script you can download the repository and simply run test.py to play a 6x6 game against the ai. If you want to play a game on mxn size import Game.py and create a Game(m, n, 'mode') object. 

Avaiable modes include:

* 'human' for human vs human
* 'inter' for human vs ai
* 'ki' for ai vs ai

## Performance
At the moment it has poor performance for original measured boards aka 11x11. For performance analysis of AI you can look at the Improve.ipynb notebook. Quick summary:
Obviously the simulationphase of the MCTS is very expensive and takes nearly 80% of the time, because we do it so often. But it's mainly behaving so poor because of the naive implementation of the board. Therefore the functions defined in this class are taking too much time since we are using BFS for finding a victory path. I played a bit with numba/cuda and it's a next goal to make this much faster.

You are welcome to contribute to this project in any shape or form
(improving the software, doing data analysis, improving the GUI (based on tkinter)).