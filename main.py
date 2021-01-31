import numpy as np

class Cell:
  possible_values = ('0', '1', '2')
  def __init__(self):
    self.value=self.possible_values[0]
  def __str__(self):
    return self.value
  def toStr(self):
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

class Player():
  def __init__(self, name, coins):
    self.name = name
    self.turn = False
    self.hasWon = False
    self.coins = coins
  def __str__(self):
    return self.name
  def win(self):
    self.hasWon = True
    print("Que alegria!")

class Game:
  boardSize = 10
  def __init__(self):
    self.table = Table(self.boardSize)
    self.table.fill()
    self.player1 = Player("Jugador 1", "1")
    self.player2 = Player("Jugador 2", "2")
    self.turn = True #True para j1, False para j2
    # print(self.table)
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
    print(contador)
    # Si llega a este punto, el juego sigue
    return 'continue'
game = Game()
# game.table.table[0][0].value = '2'

print(game.table)
print(game.checkGameState())
# game.fill()
# game.toString()