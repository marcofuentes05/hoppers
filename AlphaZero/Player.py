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
        if 0 <= j < 10 and 0 <= i < 10 and game.table[j][i].value == '0':
          self.moves.append(Move(self.identifier, position, [(j,i)]))

  def checkHopsRecursive(self, move, game):
    (fila, columna) = move.sequence[len(move.sequence) - 1]
    for i in range(columna-1, columna+2):
      for j in range (fila-1, fila+2):
        if 0<= i < 10 and 0<=j<10 and game.table[j][i].value != '0':
          nuevaFila = j + j - fila
          nuevaColumna = i + i - columna
          if 0 <= nuevaFila <10 and 0 <= nuevaColumna <10 and game.table[nuevaFila][nuevaColumna].value == '0' and (nuevaFila, nuevaColumna) not in move.sequence:
            move0 = copy.deepcopy(move)
            move0 = move
            move0.sequence.append((nuevaFila, nuevaColumna))
            self.moves.append(move0)
            self.checkHopsRecursive(move0, game)
  
  def checkHops(self, position, game):
    (fila, columna) = position
    for i in range(columna-1, columna+2):
      for j in range (fila-1, fila+2):
        if 0<=i <10 and 0<=j<10:
          if game.table[j][i].value != '0':
            nuevaFila = j + j - fila
            nuevaColumna = i + i - columna
            if 0 <= nuevaFila <10 and 0 <= nuevaColumna <10 and game.table[nuevaFila][nuevaColumna].value == '0':
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
