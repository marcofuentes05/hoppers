from IPython.display import HTML, display
import time

def tableState(value):
  strg = "    0 1 2 3 4 5 6 7 8 9 <br />  ------------------------<br />"
  for i in range(10):
    strg += "{} | ".format(i)
    for j in range(10):
      strg += "{} ".format(value.table[i][j])
    strg += " | <br />"
  strg += '  ________________________'
  return HTML("""
      <p>
          {value}
      </p>
  """.format(value=strg, max=max))

def turno(value):
  return HTML("""
    <p>Turnos jugados: <strong>{}</strong> </p>
  """.format(value))

def lenActions(value):
  return HTML("""
    <p>Cantidad de acciones evaluadas: {}
    """.format(value))

def progress(value, max):
    return HTML("""
        <progress
          value={value}
          max={max}
        >
        {value}/{max}
        </progress>
    """.format(value=value, max=max))

def move2xml(move):
  #TYPE move es namedtuple('Move' , 'player initialPosition sequence')
  string = ""
  string +="<move>\n"
  string += "<from row={rowi} col={coli} />\n<to row={rowf} col={colf}/>\n".format(
      rowi=move.initialPosition[0],
      coli=move.initialPosition[1],
      rowf=move.sequence[len(move.sequence)-1][0],
      colf=move.sequence[len(move.sequence)-1][1]
      )
  string += "<path>"
  for (row, col) in move.sequence:
    string += "<pos row={row} col={col} />\n".format(row=row, col=col)
  string += "</path>\n"
  string += "</move>\n"
  return string


import numpy as np
from collections import namedtuple
import copy
import math

Move= namedtuple('Move' , 'player initialPosition sequence')
Result= namedtuple('Result' , 'table')
class Player:
  def __init__(self, identifier):
    self.identifier = identifier
    self.positions = []
    self.moves=[]
    if identifier == '1':
      self.initialPosition=(0,0)
    else:
      self.initialPosition=(9,9)

  # Esta funcion escanea el tablero y me dice las posiciones de mis fichas
  def scan(self, game):
    for i in range(10):
      for j in range(10):
        if game.table.table[i][j].value == self.identifier:
          self.positions.append((i,j))

  def checkSteps(self, position, game):
    (fila, columna) = position
    for i in range(columna-1, columna + 2):
      for j in range (fila-1, fila+2):
        if 0 <= j < 10 and 0 <= i < 10 and game.table[j][i].value == '.':
          self.moves.append(Move(self.identifier, position, [(j,i)]))

  def checkHopsRecursive(self, move, game):
    (fila, columna) = move.sequence[len(move.sequence) - 1]
    for i in range(columna-1, columna+2):
      for j in range (fila-1, fila+2):
        if 0<= i < 10 and 0<=j<10 and game.table[j][i].value != '.':
          nuevaFila = j + j - fila
          nuevaColumna = i + i - columna
          if 0 <= nuevaFila <10 and 0 <= nuevaColumna <10 and game.table[nuevaFila][nuevaColumna].value == '.' and (nuevaFila, nuevaColumna) not in move.sequence:
            move0 = copy.deepcopy(move)
            move0.sequence.append((nuevaFila, nuevaColumna))
            self.moves.append(move0)
            self.checkHopsRecursive(move0, game)
  
  def checkHops(self, position, game):
    (fila, columna) = position
    for i in range(columna-1, columna+2):
      for j in range (fila-1, fila+2):
        if 0<=i <10 and 0<=j<10:
          if game.table[j][i].value != '.':
            nuevaFila = j + j - fila
            nuevaColumna = i + i - columna
            if 0 <= nuevaFila <10 and 0 <= nuevaColumna <10 and game.table[nuevaFila][nuevaColumna].value == '.':
              move = Move(self.identifier, position, [(nuevaFila,nuevaColumna)])
              self.moves.append(move)
              self.checkHopsRecursive(move, game)

  def possible_moves(self, gameState):
    for position in self.positions:
      self.checkSteps(position, gameState)
      self.checkHops(position, gameState)
  
  def madeMove(self):
    self.moves = []
    self.positions=[]

  def win(self):
    self.hasWon = True
    print("Que alegria!")

  def __str__(self):
    return str('JUGADOR: {}\nCon coordenadas: {}'.format(self.identifier, self.moves))

class Cell:
  possible_values = ('.', '1', '2')
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
    self.is_terminal = False
  def fill(self): #1 tiene la esquina superior izquierda, 2 tiene la inferior derecha
    inicio=5
    resta=0
    for i in range(inicio):
      for j in range(inicio-resta):
        self.table[i][j].value = self.table[i][j].possible_values[1]
        self.table[self.boardSize - 1 - i][self.boardSize - 1 - j].value = self.table[i][j].possible_values[2]
      resta+=1
  
  def is_terminal(self):
    inicio = 5
    resta = 0
    contador = 0
    contador1 = 0
    contador2 = 0
    for i in range(inicio):
      for j in range(inicio-resta):
        val = self.table[self.boardSize - 1 - i][self.boardSize - 1 - j].value
        valOpuesto = self.table[i][j].value
        if (val != '.'):
          if (val == '1'):
            contador1 += 1
          if (valOpuesto == '2'):
            contador2 += 1
          contador += 1
      resta += 1
    if (contador == 15 and (contador1 > 0 or contador2 > 0)):
      self.is_terminal = True
    # Si llega a este punto, el juego sigue
    self.is_terminal = False

  def toString(self):
    for i in range(10):
      strg = ""
      for j in range(10):
        strg += "{} ".format(self.table[i][j])
      print(strg)
  
  def toDisplay(self):
    strg = "    0 1 2 3 4 5 6 7 8 9 \n  ------------------------\n"
    for i in range(10):
      strg += "{} | ".format(i)
      for j in range(10):
        strg += "{} ".format(self.table[i][j])
      strg += " | \n"
    strg += '  ________________________'
    return strg 

  def __str__(self):
    strg = "    0 1 2 3 4 5 6 7 8 9 \n  ------------------------\n"
    for i in range(10):
      strg += "{} | ".format(i)
      for j in range(10):
        strg += "{} ".format(self.table[i][j])
      strg += " | \n"
    strg += '  ________________________'
    return strg 
  
class Game:
  boardSize = 10
  def __init__(self):
    self.table = Table(self.boardSize)
    self.table.fill()
    self.turn = True #True para j1, False para j2
    self.player1 = Player('1')
    self.player2 = Player('2')
    self.winner = None

  def to_move(self):
    if self.turn:
      return self.player1
    else:
      return self.player2
  
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
        if (val != '.'):
          if (val == '1'):
            contador1 += 1
          contador +=1
      resta+=1
    if (contador == 15 and contador1 >0):
      return 'J1 HA GANADO'

    # Luego revisa si j2 ha ganado
    inicio=5
    resta=0
    contador = 0
    contador2 = 0
    for i in range(inicio):
      for j in range(inicio-resta):
        val = self.table.table[i][j].value
        if (val != '.'):
          if (val == '2'):
            contador2 += 1
          contador +=1
      resta+=1
    if (contador == 15 and contador2 >0):
      return 'J2 HA GANADO'
    # Si llega a este punto, el juego sigue
    return 'continue'

  def actions(self, state):
    if self.turn:
      p1.moves = []
      p1.scan(self)
      p1.possible_moves(state)
      return p1.moves
    else:
      p2.moves = []
      p2.scan(self)
      p2.possible_moves(state)
      return p2.moves

  def utility(self, table, player):
      param = player.identifier
      (fila, columna) = player.initialPosition
      utility = 0
      if (fila, columna) == (0,0):
        for i in range(5):
          for j in range(i):
            utility = utility + (1 if table.table[-1-j][i+5].value != '.' else 0) + (2 if table.table[-1-j][i+5].value == param else 0 )
            utility = utility - (1 if table.table[4-i][j].value != '.' else 0)
      else:
        for i in range(5,10):
          for j in range(5,i+1):
              utility = utility + (1 if table.table[-1-i][j-5].value != '.' else 0) + (2 if table.table[-1-i][j-5].value==param else 0 )
              utility = utility - (1 if table.table[4-j][i].value != '.' else 0)
      return utility

  # Actualiza el tablero cuando un jugador decide 
  # Basicamente es una funcion de transicion, aunque si afecta el juego en tiempo real
  def makeMove(self, move):
    (fila, columna) = move.initialPosition
    (filaFinal, columnaFinal) = move.sequence[len(move.sequence)-1] #la ultima posicion
    self.table.table[fila][columna].value='.'
    self.table.table[filaFinal][columnaFinal].value=move.player
    self.turn = not self.turn

  def result(self,state, move): #state sera un snapshot de tablero, turno
    tablero = copy.deepcopy(self.table)
    # tablero = self.table
    (filaI, columnaI) = move.initialPosition
    (filaF, columnaF) = move.sequence[len(move.sequence) - 1]
    identifier = move.player
    tablero.table[filaI][columnaI].value = '.'
    tablero.table[filaF][columnaF].value = identifier
    return tablero

  def terminal_test(self, state): 
    # Revisa si alguien ya gano, o si sigue el juego
    # state es un objeto Table (inicialmente es self.table, pero para minimax es mejor pasarlo como parametro)
    inicio=5
    resta=0
    contador = 0
    contador1 = 0
    contador2 = 0
    for i in range(inicio):
      for j in range(inicio-resta):
        val = state.table[self.boardSize - 1 - i][self.boardSize - 1 - j].value
        valOpuesto = state.table[i][j].value
        if (val != '.'):
          if (val == '1'):
            contador1 += 1
          if (valOpuesto == '2'):
            contador2 += 1
          contador +=1
      resta+=1
    if (contador == 15 and (contador1 > 0 or contador2 > 0)):
      if contador1 == 15:
        self.winner = self.player1
      elif contador2 == 15:
        self.winner = self.player2
      return True
    # Si llega a este punto, el juego sigue
    return False

def alpha_beta_cutoff_search(state, game, d=1, cutoff_test=None, eval_fn=None):

  player = game.to_move()
  def max_value(state, alpha, beta, depth):
    v = -np.inf
    variable = game.actions(state)
    # out3.update(lenActions(len(variable)))
    if cutoff_test(state, depth, variable):
      return eval_fn(state)
    # print('depth: {}'.format(depth))
    # print('LEN: ',len(variable))
    for a in variable:
      v2 = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
      if v2 <= beta:
        v = v2
        return v
      alpha = max(alpha, v)
    return v

  def min_value(state, alpha, beta, depth):
    v = np.inf
    variable = game.actions(state)
    # out3.update(lenActions(len(variable)))
    if cutoff_test(state, depth, variable):
      return eval_fn(state)
    # print('depth: {}'.format(depth))
    # print('LEN: ',len(variable))
    for a in variable:
      v2 = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
      if v2 >= alpha:
        v= v2
        return v
      beta = min(beta, v)
    return v

  def cutoff_test(state, depth, actions):
    return depth > d or game.terminal_test(state) or len(actions) > 50
  
  eval_fn = eval_fn or (lambda state: game.utility(state, player))
  best_score = -np.inf
  beta = np.inf
  best_action = None
  gameActions = game.actions(state)
  # for action in gameActions:
  #   print(action)
  i = 0 
  for a in gameActions:
    #out2.update(progress(i + 1, len(gameActions)))
    i+=1
    v = min_value(game.result(state, a), best_score, beta, 1)
    if v > best_score:
      best_score = v
      best_action = a
  # out.update(tableState(game.table))
  # print("Best score: ",best_score)
  return best_action

if __name__ == '__main__':
  game = Game()
  print(game.table)
  p1 = game.player1
  p2 = game.player2
  game.table.table[0][3].value= '.'
  game.table.table[1][4].value='1'
  # out = display(tableState(game.table), display_id=True)
  # out1 = display(turno(0), display_id=True)
  #out2 = display(progress(1, 100) ,display_id=True)
  # out3 = display(lenActions(1), display_id=True)
  # p1.scan(game)
  # p1.possible_moves(game.table)
  # for move in p1.moves:
  #   print(move)

  # print(game.table)
  turnos = 0
  while not game.terminal_test(game.table):
    # out1.update(turno(turnos))
    # print('TURNO DE {}'.format('J1' if game.turn else 'J2'))
    if game.turn:
      variable = alpha_beta_cutoff_search(game.table, game)
      # print('J1 decide jugar: {}'.format(variable))
      game.makeMove(variable)
      p1.madeMove()
    else:
      # print(p2.moves)
      # variable = input('Ingresa el indice del movimiento:\n')#alpha_beta_cutoff_search(game.table, game)
      # game.makeMove(p2.moves[int(variable)])
      variable = alpha_beta_cutoff_search(game.table, game)
      # print('J2 decide jugar: {}'.format(variable))
      game.makeMove(variable)
      p2.madeMove()
    print(game.table)
    turnos+=1

  
  print(game.checkGameState())    
