import sys
# sys.path.append('..')
from .game import Game
from .Player import Player
import numpy as np

class Cell:
    # vacio, j1, j2
  #possible_values = ('-', 'O', 'X')
  def __init__(self, possible_values):
    self.value=possible_values[0]
  def __str__(self):
    return self.value

class Table():
  def __init__(self, boardSize):
    self.boardSize = boardSize
    matrix = np.full((boardSize, boardSize), Cell())
    for i in range(boardSize):
      for j in range(boardSize):
        cell = Cell()
        matrix[i][j] = cell
    self.table = matrix
  def fill(self, possible_values): #1 tiene la esquina superior izquierda, 2 tiene la inferior derecha
    inicio=5
    resta=0
    for i in range(inicio):
      for j in range(inicio-resta):
        self.table[i][j].value = possible_values[1]
        self.table[self.boardSize - 1 - i][self.boardSize - 1 - j].value = possible_values[-1]
      resta+=1
  
  def toString(self):
    for i in range(10):
      strg = ""
      for j in range(10):
        strg += "{} ".format(self.table[i][j])
      print(strg)
  
  def __str__(self):
    strg = ""
    for i in range(10):
      for j in range(10):
        strg += "{} ".format(self.table[i][j])
      strg += "\n"
    return strg 
  

class HoppersGame(Game):
    square_content = {
        -1: "X",
        0: "-",
        +1: "O"
    }

    def __init__(self, n):
        self.n = n
        self.player1 = Player(self.square_content[1])
        self.player2 = Player(self.square_content[-1])
        self.turn = True #True para j1, False para j2
        self.board = Table(self.n)
        self.board.fill(self.square_content)
    
    def getInitBoard(self):
        return self.board.table
        
    def getBoardSize(self):
        return (self.n, self.n)
    
    def getActionSize(self):
        if self.turn:
            self.player1.scan(self.board)
            self.player1.possible_moves(self.board.table)
            return len(self.player1.moves)
        else:
            self.player2.scan(self.board)
            self.player2.possible_moves(self.board.table)
            return len(self.player2.moves)

    