#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk
import math


# # CONFIG SECTION
CANVAS_WIDTH = 1024
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 780
CANVAS_HEIGHT = 600
LARGE_FONT = ("Droid", 14)
NORM_FONT = ("Droid", 10)
SMALL_FONT = ("Droid", 8)
PLAYER1_COLOR = 'green'
PLAYER2_COLOR = '#ef9210'
TILE_GAP = 3



class HexCanvas(tk.Canvas):
    '''inherits Canvas class (all Canvas methodes, attributes will be accessible)
       You can add your customized methods here.
    '''
    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master=master, *args, **kwargs)

    def create_hexagon(self, center, radius, name='1,1'):
        # center (x, y)
        # create list of points
        points = []
        points.extend((center[0], center[1]+radius))
        points.extend((center[0]+math.sqrt(3)*radius/2, center[1]+radius/2))
        points.extend((center[0]+math.sqrt(3)*radius/2, center[1]-radius/2))
        points.extend((center[0], center[1]-radius))
        points.extend((center[0]-math.sqrt(3)*radius/2, center[1]-radius/2))
        points.extend((center[0]-math.sqrt(3)*radius/2, center[1]+radius/2))

        self.create_polygon(points,
                            outline='white',
                            width=0,
                            fill='white',
                            activefill='grey',
                            activeoutline=PLAYER1_COLOR,
                            activewidth=2,
                            tags=('hexagon', name),
                            smooth=0)


class GameFrame():
    def __init__(self, parent, m, n, game):
        self.fieldsize = (m, n)
        self.game = game
        # r = 25  # make this depend on geometry of window and board size? TODO
        r = CANVAS_WIDTH/(2/3 + m*3)
        r = min(CANVAS_WIDTH/(2/3 + m*3), CANVAS_HEIGHT/(2/3 + n*3))
        h = math.sqrt(3)/2*r
        x_gap = r/3
        y_gap = r/3
        x = h + x_gap
        y = r + y_gap
        gap = TILE_GAP
        xd = h + gap
        yd = 3/2*r + gap
        self.waitVar = tk.BooleanVar()
        self.waitVar.set(False)

        # DONE calculate Frame size
        self.canvas_h = y_gap + r + (yd)*self.fieldsize[0]
        self.canvas_w = 2*x_gap + 2 * xd + 2*xd*(self.fieldsize[1]-1) + (self.fieldsize[0]-1)*xd

        # DONE create canvas
        self.canvas = HexCanvas(parent,
                                width=self.canvas_w,
                                height=self.canvas_h,
                                background='#988878')  # to see the canvas..

        self.draw_decorations(r, gap)

        # DONE Draw Tiles
        for i in range(self.fieldsize[0]):
            for j in range(self.fieldsize[1]):
                # name = str(i)+','+str(j)
                name = ','.join(map(str, (i, j)))
                #self.canvas.create_hexagon((x+2*i*xd+j*xd, y + j*yd), r,
                self.canvas.create_hexagon((x+2*j*xd+i*xd, y + i*yd), r,
                                           name=name)
                self.canvas.tag_bind(name, "<Button-1>", self.callback)

        self.canvas.itemconfig('hexagon',
                               activeoutline=self.getWaitingColor(),
                               activewidth=2)

        # DONE add canvas to Frame
        self.canvas.grid(row=1,
                         rowspan=4,
                         column=0,
                         columnspan=2)
        self.canvas.grid_columnconfigure(0, weight=1)

    def draw_decorations(self, r, gap):
        h = math.sqrt(3)/2*r
        x_gap = r/3
        y_gap = r/3
        x = h + x_gap
        y = r + y_gap
        xd = h + gap
        yd = 3/2*r + gap
        # DONE calculate coordinates for decorations
        j_max = self.fieldsize[1]-1
        i_max = self.fieldsize[0]-1
        a = (x, y)
        b = (x+xd*i_max, y+yd*i_max)
        c = (x+xd*i_max+2*xd*j_max, y+yd*i_max)
        d = (x+2*xd*j_max, y)
        northls = [a, d, (d[0], d[1]-r), (a[0], a[1]-r)]
        southls = [b, c, (c[0], c[1]+r), (b[0], b[1]+r)]
        eastls = [a, b, (b[0]-h, b[1]+r/2), (a[0]-h, a[1]+r/2)]
        westls = [d, c, (c[0]+h, c[1]-r/2), (d[0]+h, d[1]-r/2)]

        # DONE Draw decorations
        self.canvas.create_polygon(northls,
                                   fill=PLAYER2_COLOR)
        self.canvas.create_polygon(southls,
                                   fill=PLAYER2_COLOR)
        self.canvas.create_polygon(eastls,
                                   fill=PLAYER1_COLOR)
        self.canvas.create_polygon(westls,
                                   fill=PLAYER1_COLOR)

    def callback(self, event):
        # Store last event for updating of tile
        self.latestEvent = event

        # pass move over to Game
        tags = event.widget.gettags(tk.CURRENT)
        tile = tags[1]
        tile = [int(x) for x in tile.split(',')]
        move = (tile[0], tile[1])
        self.game.makeMove(move)
        self.waitVar.set(True)

    def recieveMove(self, move):
        '''
        input: move
        Updates tile on the board
        '''
        # translate move to tag:
        tag = ','.join(map(str, move))

        # set colors with data from game
        # potential bug source: change player before receive move
#         if self.game.currentPlayer() == 1:  # check the values
#             player_color = PLAYER1_COLOR
#             other_color = PLAYER2_COLOR
#         else:
#             player_color = PLAYER2_COLOR
#             other_color = PLAYER1_COLOR

        # Update Filling of Tile
        self.canvas.itemconfig(tag, fill=self.getCurrentColor())
        # Update Outline for next Player
        self.canvas.itemconfig('hexagon',
                               activeoutline=self.getWaitingColor(),
                               activewidth=2)

    def reset(self):
        # TODO Game method to reset whole game. also undo etc?
        self.canvas.itemconfig('hexagon', fill='white')

    def getCurrentColor(self):
        if self.game.currentPlayer() == 2:
            return PLAYER1_COLOR
        else:
            return PLAYER2_COLOR

    def getWaitingColor(self):
        if self.game.currentPlayer() == 2:
            return PLAYER2_COLOR
        else:
            return PLAYER1_COLOR


class HexGui():
    def __init__(self, m, n, game):
        self.game = game
        self.swap = False
        self.root = tk.Tk()
        #print('start Player', self.game.currentPlayer())
        msg = 'Player ' + str(self.game.currentPlayer()) + ' begins!'
        self.label_start = tk.Label(self.root,
                                    text=msg,
                                    font=LARGE_FONT)
        self.label_start.grid(row=3, column=2)

        # Labels players
        self.label_player1 = tk.Label(self.root,
                                      bg=PLAYER1_COLOR,
                                      text='Player 1 is '+self.game.starter)
        self.label_player2 = tk.Label(self.root,
                                      bg=PLAYER2_COLOR,
                                      text='Player 2 is '+self.game.nonstarter)
        self.label_player1.grid(row=0, column=0)
        self.label_player2.grid(row=0, column=1)

        # Label numberOfMoves
        self.numberOfMoves = tk.StringVar(master=self.root,
                                          value='Number of moves: 0')
        self.label_moves = tk.Label(self.root, textvariable=self.numberOfMoves)
        self.label_moves.grid(row=2, column=2)

        # Board
        self.uiBoard = GameFrame(self.root, m, n, game)

        # Buttons
        button_swap = ttk.Button(self.root, text="SWAP",
                                 command=self.swap_players)
        button_quit = ttk.Button(self.root, text="QUIT",
                                 command=self.root.quit)
        button_swap.grid(row=0, column=2)
        button_quit.grid(row=5, column=2)

        

    def start(self):
        self.root.mainloop()

    def receiveMove(self, move):
        print('ui recieved move',
              move,
              'not from',
              self.game.currentPlayer())
        self.uiBoard.recieveMove(move)
        self.numberOfMoves.set('Number of moves: ' + str(self.game.board.zug))

    def swap_players(self):
        if self.game.board.zug == 1:
            print('swap!')
            self.game.board.swap = True
            self.label_player1['text'] = 'Player 1 is '+self.game.nonstarter
            self.label_player2['text'] = 'Player 2 is '+self.game.starter
            move = self.game.board.getLastMove()
            self.game.board.receiveMove(move)
            self.uiBoard.waitVar.set(True)
            self.numberOfMoves.set('Number of moves: 2')
            if self.game.board.finished():
                self.game.finished = True
                self.finish(self.game.board.winner())
        else:
            return

    def finish(self, playerID):
        playerdict = {}
        if self.swap:
            playerdict[1] = '2'
            playerdict[2] = '1'
        else:
            playerdict[1] = '1'
            playerdict[2] = '2'
        winner = playerdict[playerID]
        # Print the Winner:
        msg = 'Player ' + winner + ' wins!'
        self.label_winner = tk.Label(self.root,
                                     text=msg,
                                     font=LARGE_FONT)
        self.label_winner.grid(row=4, column=2)
        self.showVictoryPath()

    #  Highlight winning path in black
    def showVictoryPath(self):
        for i in self.game.board.getVictoryPath():
            tag = ','.join(map(str, i))
            self.uiBoard.canvas.itemconfig(tag, fill='black')

        # DONE deactivate all fields:
        self.uiBoard.canvas.itemconfig('hexagon', state='disabled')
        print(self.game.board.board)
