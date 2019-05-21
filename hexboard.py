from collections import deque
import numpy as np

# Player 1 connects left and right sides
# Player 2 connects top and bottom sides


class HexBoard:
    def __init__(self, m, n):
        self.starter = None
        self.board = self.matrix(m,n)
        self.zug = 0
        self.no_filled = 0
        self.lastmove = None
        self.goal_21 = [(i, 0) for i in range(m)]    # Column '0'
        self.goal_22 = [(i, n-1) for i in range(m)]  # Column 'n-1'
        self.goal_11 = [(0, i) for i in range(n)]    # Row '0'
        self.goal_12 = [(m-1, i) for i in range(n)]  # Row 'm-1'
        self.swap = False
        self.win = None
        self.endknoten = None

    # n x m zero Matrix
    # The matrix represents the board
    def matrix(self, m, n):
        M = np.zeros((m, n), dtype=int)
        return M

    # move as Tuple (i,j)
    # 1st IF: Swap Case. Do nothing
    # The other IF is used to determine whose turn it was
    def receiveMove(self, move):
        i,j = move
        if self.zug==2 and self.swap:
            self.zug += 1
            return
        if self.board[i][j] == 0:
            self.zug += 1
            if self.no_filled%2==0:
                self.board[i][j] = 1
            else:
                self.board[i][j] = 2
            self.lastmove = move
            self.no_filled += 1
        return

    def getLastMove(self):
        return self.lastmove

    # Bestimme, ob Spiel zu Ende ist.
    # Mit BFS wird untersucht, ob das letzte belegte Feld einen Weg zu den 'richtigen' Seiten hat
    # Mit p wird der moegliche Gewinner bezeichnet
    # Falls Spiel zu Ende ist, dann ist p Gewinner
    def finished(self):
        if self.lastmove is not None:
            if len(self.board)==1 and len(self.board[0])==1 and self.zug==1:
                return False
            p = None
            if self.no_filled%2==0:
                    p = 2
                    goal_1 = self.goal_11
                    goal_2 = self.goal_12
            else:
                    p = 1
                    goal_1 = self.goal_21
                    goal_2 = self.goal_22
            visited = []
            q = deque()
            found = 0
            for i in range(len(self.board)):
                visited.append([False]*len(self.board[0]))
            q.appendleft(self.lastmove)
            s, t = self.lastmove
            visited[s][t] = True
            while q:
                Knoten = q.pop()
                if Knoten in goal_1:
                    if found != 1:
                        found += 1
                if Knoten in goal_2:
                    if found != 2 and found != 3:
                        found += 2
                if found==3:
                    self.endknoten = Knoten
                    self.win = p
                    return True
                for k in self.adjazenz(Knoten):
                    i, j = k
                    if visited[i][j] is False:
                        q.appendleft((i, j))
                        visited[i][j] = True
        return False

    
    # Methode findet 'richtige'(blau oder rot) benachbarten Felder
    # 6 Moeglichkeiten, somit 6 Faelle/IF Bedingungen
    def adjazenz(self, move):
        k, l = move
        n, m = len(self.board), len(self.board[0])
        value = self.board[k][l]
        adj_list = []
        if k != 0 and self.board[k-1][l] == value:
                adj_list.append((k-1, l))
        if k != n-1 and self.board[k+1][l] == value:
                adj_list.append((k+1, l))
        if l != 0 and self.board[k][l-1] == value:
                adj_list.append((k, l-1))
        if l != m-1 and self.board[k][l+1] == value:
                adj_list.append((k, l+1))
        if k != 0 and l != m-1 and self.board[k-1][l+1] == value:
                adj_list.append((k-1, l+1))
        if k != n-1 and l != 0 and self.board[k+1][l-1] == value:
                adj_list.append((k+1, l-1))
        return adj_list

    def winner(self):
        return self.win

    def getVictoryPath(self):
        start = self.endknoten
        if self.win == 2:
            if start in self.goal_11:
                end = self.goal_12
            else:
                end = self.goal_11
        else:
            if start in self.goal_21:
                end = self.goal_22
            else:
                end = self.goal_21
        return self.find_shortest_path(start, end, path=[])
        

    def find_shortest_path(self, node, end, path):
        path = path + [node]
        if node in end:
            return path
        shortest = None
        for k in self.adjazenz(node):
            if k not in path:
                newpath = self.find_shortest_path(k, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
