import numpy as np
from collections import namedtuple
import copy

Move= namedtuple('Move' , 'player initialPosition sequence')
class Player:
  def __init__(self, identifier, game):
    self.identifier = identifier
    self.game = game
    self.positions = []
    self.moves=[]
  
  # Esta funcion escanea el tablero y me dice las posiciones de mis fichas
  def populate(self):
    for i in range(10):
      for j in range(10):
        if self.game.table.table[i][j].value == self.identifier:
          self.positions.append((i,j))

  def checkSteps(self, position):
    (fila, columna) = position
    for i in range(columna-1, columna + 2):
      for j in range (fila-1, fila+2):
        if 0 <= j < 10 and 0 <= i < 10 and self.game.table.table[j][i].value == '0':
          self.moves.append(Move(self.identifier, position, [(j,i)]))

  def checkHopsRecursive(self, move):
    (fila, columna) = move.sequence[len(move.sequence) - 1]
    for i in range(columna-1, columna+2):
      for j in range (fila-1, fila+2):
        if 0<= i < 10 and 0<=j<10 and self.game.table.table[j][i].value != '0':
          nuevaFila = j + j - fila
          nuevaColumna = i + i - columna
          if 0 <= nuevaFila <10 and 0 <= nuevaColumna <10 and self.game.table.table[nuevaFila][nuevaColumna].value == '0' and (nuevaFila, nuevaColumna) not in move.sequence:
            move0 = copy.deepcopy(move)
            move0.sequence.append((nuevaFila, nuevaColumna))
            self.moves.append(move0)
            self.checkHopsRecursive(move0)
  
  def checkHops(self, position):
    (fila, columna) = position
    for i in range(columna-1, columna+2):
      for j in range (fila-1, fila+2):
        if self.game.table.table[j][i].value != '0':
          nuevaFila = j + j - fila
          nuevaColumna = i + i - columna
          if 0 <= nuevaFila <10 and 0 <= nuevaColumna <10 and self.game.table.table[nuevaFila][nuevaColumna].value == '0':
            move = Move(self.identifier, position, [(nuevaFila,nuevaColumna)])
            self.moves.append(move)
            self.checkHopsRecursive(move)

  def possible_moves(self):
    for position in self.positions:
      self.checkSteps(position)
      self.checkHops(position)
  
  def madeMove(self):
    self.moves = []
    self.positions=[]

  def win(self):
    self.hasWon = True
    print("Que alegria!")

  def __str__(self):
    return str(self.positions)

class Cell:
  possible_values = ('0', '1', '2')
  def __init__(self):
    self.value=self.possible_values[0]
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
  def fill(self): #1 tiene la esquina superior izquierda, 2 tiene la inferior derecha
    inicio=5
    resta=0
    for i in range(inicio):
      for j in range(inicio-resta):
        self.table[i][j].value = self.table[i][j].possible_values[1]
        self.table[self.boardSize - 1 - i][self.boardSize - 1 - j].value = self.table[i][j].possible_values[2]
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
  

class Game:
  boardSize = 10
  def __init__(self):
    self.table = Table(self.boardSize)
    self.table.fill()
    self.player1 = Player("Jugador 1", "1")
    self.player2 = Player("Jugador 2", "2")
    self.turn = True #True para j1, False para j2
  def checkGameState(self): 
    # Revisa si alguien ya gano, o si sigue el juego
    # Primero revisa si j1 ha ganado
    inicio=5
    resta=0
    contador = 0
    contador1 = 0
    for i in range(inicio):
      for j in range(inicio-resta):
        val = self.table.table[self.boardSize - 1 - i][self.boardSize - 1 - j].value
        if (val != '0'):
          if (val == '1'):
            contador1 += 1
          contador +=1
      resta+=1
    if (contador == 15 and contador1 >0):
      return 'J1'

    # Luego revisa si j2 ha ganado
    inicio=5
    resta=0
    contador = 0
    contador2 = 0
    for i in range(inicio):
      for j in range(inicio-resta):
        val = self.table.table[i][j].value
        if (val != '0'):
          if (val == '2'):
            contador2 += 1
          contador +=1
      resta+=1
    if (contador == 15 and contador2 >0):
      return 'J2'
    # Si llega a este punto, el juego sigue
    return 'continue'

  # Actualiza el tablero cuando un jugador decide 
  def makeMove(self, move):
    (fila, columna) = move.initialPosition
    (filaFinal, columnaFinal) = move.sequence[len(move.sequence)-1] #la ultima posicion
    self.table.table[fila][columna].value='0'
    self.table.table[filaFinal][columnaFinal].value=move.player
    self.turn = not self.turn

if __name__ == '__main__':

  game = Game()
  # game.table.table[4][5].value='1'
  # game.table.table[3][4].value='2'
  # game.table.table[5][4].value='2'
  # game.table.table[3][4].value='2'
  # game.table.table[3][6].value='2'
  # game.table.table[3][8].value='2'
  # game.table.table[5][8].value='2'
  # game.table.table[1][6].value='2'

  p1 = Player('1', game)
  p2 = Player('2', game)
  p1.populate()
  p1.possible_moves()

  while game.checkGameState() == 'continue':
    print(game.table)
    if game.turn:
      print('\nP1 POSSIBLE MOVES:\n')
      for (index, i) in enumerate(p1.moves):
        print(index, i)
    else:
      print('\nP2 POSSIBLE MOVES:\n')
      for (index, i) in enumerate(p2.moves):
        print(index, i)
    moveIndex = input('ingresa el indice del movimiento:\n')
    if game.turn:
      game.makeMove(p1.moves[int(moveIndex)])
      p1.madeMove()
      p2.populate()
      p2.possible_moves()
    else:
      game.makeMove(p2.moves[int(moveIndex)])
      p2.madeMove()
      p1.populate()
      p1.possible_moves()


    # print(game.checkGameState())