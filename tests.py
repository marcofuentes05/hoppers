import numpy as np
from collections import namedtuple
# import copy
import math

# Move= namedtuple('Move' , 'player initialPosition sequence')
# Result= namedtuple('Result' , 'table')


class Move:
    def __init__(self, identifier, position, sequence):
        self.player = identifier
        self.initialPosition = position
        self.sequence = sequence

    def __str__(self):
        return "Move ({}\t{}\t{})".format(self.player, self.initialPosition, self.sequence)


class Result:
    def __init__(self, table):
        self.table = table


class Player:
    def __init__(self, identifier):
        self.identifier = identifier
        self.positions = []
        self.moves = []
        if identifier == '1':
            self.initialPosition = (0, 0)
        else:
            self.initialPosition = (9, 9)

    # Esta funcion escanea el tablero y me dice las posiciones de mis fichas
    def scan(self, game):
        for i in range(10):
            for j in range(10):
                if game.table.table[i][j].value == self.identifier:
                    self.positions.append((i, j))

    def checkSteps(self, position, game):
        (fila, columna) = position
        for i in range(columna-1, columna + 2):
            for j in range(fila-1, fila+2):
                if 0 <= j < 10 and 0 <= i < 10 and game.table[j][i].value == '.':
                    self.moves.append(
                        Move(self.identifier, position, [(j, i)]))

    def checkHopsRecursive(self, move, game):
        (fila, columna) = move.sequence[len(move.sequence) - 1]
        for i in range(columna-1, columna+2):
            for j in range(fila-1, fila+2):
                if 0 <= i < 10 and 0 <= j < 10 and game.table[j][i].value != '.':
                    nuevaFila = j + j - fila
                    nuevaColumna = i + i - columna
                    if 0 <= nuevaFila < 10 and 0 <= nuevaColumna < 10 and game.table[nuevaFila][nuevaColumna].value == '.' and (nuevaFila, nuevaColumna) not in move.sequence:
                        # move0 = copy.deepcopy(move)
                        move0 = move
                        move0.sequence.append((nuevaFila, nuevaColumna))
                        self.moves.append(move0)
                        self.checkHopsRecursive(move0, game)

    def checkHops(self, position, game):
        (fila, columna) = position
        for i in range(columna-1, columna+2):
            for j in range(fila-1, fila+2):
                if 0 <= i < 10 and 0 <= j < 10:
                    if game.table[j][i].value != '.':
                        nuevaFila = j + j - fila
                        nuevaColumna = i + i - columna
                        if 0 <= nuevaFila < 10 and 0 <= nuevaColumna < 10 and game.table[nuevaFila][nuevaColumna].value == '.':
                            move = Move(self.identifier, position, [
                                        (nuevaFila, nuevaColumna)])
                            self.moves.append(move)
                            self.checkHopsRecursive(move, game)

    def possible_moves(self, gameState):
        for position in self.positions:
            self.checkSteps(position, gameState)
            self.checkHops(position, gameState)

    def madeMove(self):
        self.moves = []
        self.positions = []

    def win(self):
        self.hasWon = True
        print("Que alegria!")

    def __str__(self):
        return str('JUGADOR: {}\nCon coordenadas: {}'.format(self.identifier, self.moves))


class Cell:
    possible_values = ('.', '1', '2')

    def __init__(self):
        self.value = self.possible_values[0]

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

    def fill(self):  # 1 tiene la esquina superior izquierda, 2 tiene la inferior derecha
        inicio = 5
        resta = 0
        for i in range(inicio):
            for j in range(inicio-resta):
                self.table[i][j].value = self.table[i][j].possible_values[1]
                self.table[self.boardSize - 1 - i][self.boardSize -
                                                   1 - j].value = self.table[i][j].possible_values[2]
            resta += 1

    def toString(self):
        for i in range(10):
            strg = ""
            for j in range(10):
                strg += "{} ".format(self.table[i][j])
            print(strg)

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
        self.turn = True  # True para j1, False para j2
        self.player1 = Player('1')
        self.player2 = Player('2')

    def to_move(self, state=None):
        if self.turn:
            return self.player1
        else:
            return self.player2

    def checkGameState(self):
        # Revisa si alguien ya gano, o si sigue el juego
        # Primero revisa si j1 ha ganado
        inicio = 5
        resta = 0
        contador = 0
        contador1 = 0
        for i in range(inicio):
            for j in range(inicio-resta):
                val = self.table.table[self.boardSize -
                                       1 - i][self.boardSize - 1 - j].value
                if (val != '.'):
                    if (val == '1'):
                        contador1 += 1
                    contador += 1
            resta += 1
        if (contador == 15 and contador1 > 0):
            return 'J1 HA GANADO'

        # Luego revisa si j2 ha ganado
        inicio = 5
        resta = 0
        contador = 0
        contador2 = 0
        for i in range(inicio):
            for j in range(inicio-resta):
                val = self.table.table[i][j].value
                if (val != '.'):
                    if (val == '2'):
                        contador2 += 1
                    contador += 1
            resta += 1
        if (contador == 15 and contador2 > 0):
            return 'J2 HA GANADO'
        # Si llega a este punto, el juego sigue
        return 'continue'

    def actions(self, state):
        if self.turn:
            p1.scan(self)
            p1.possible_moves(state)
            return p1.moves
        else:
            p2.scan(self)
            p2.possible_moves(state)
            return p2.moves

    def utility(self, table, player):
        param = player.identifier
        (fila, columna) = player.initialPosition
        utility = 0
        for i in range(10):
            for j in range(10):
                if table.table[i][j].value == param:
                    try:
                        # distancia a la esquina opuesta
                        utility = utility + 1 / \
                            ((i - (10 - fila))**2 + (j - (10-columna))**2)
                    except:
                        utility += 50
        return utility

    # Actualiza el tablero cuando un jugador decide
    # Basicamente es una funcion de transicion, aunque si afecta el juego en tiempo real
    def makeMove(self, move):
        (fila, columna) = move.initialPosition
        (filaFinal, columnaFinal) = move.sequence[len(
            move.sequence)-1]  # la ultima posicion
        self.table.table[fila][columna].value = '.'
        self.table.table[filaFinal][columnaFinal].value = move.player
        self.turn = not self.turn

    def result(self, state, move):  # state sera un snapshot de tablero, turno
        # tablero = copy.deepcopy(self.table)
        tablero = self.table
        (filaI, columnaI) = move.initialPosition
        (filaF, columnaF) = move.sequence[len(move.sequence) - 1]
        identifier = move.player
        tablero.table[filaI][columnaI].value = '.'
        tablero.table[filaF][columnaF].value = identifier
        return tablero

    def terminal_test(self, state, d=1):
        # Revisa si alguien ya gano, o si sigue el juego
        # state es un objeto Table (inicialmente es self.table, pero para minimax es mejor pasarlo como parametro)
        inicio = 5
        resta = 0
        contador = 0
        contador1 = 0
        contador2 = 0
        for i in range(inicio):
            for j in range(inicio-resta):
                val = state.table[self.boardSize - 1 -
                                  i][self.boardSize - 1 - j].value
                valOpuesto = state.table[i][j].value
                if (val != '.'):
                    if (val == '1'):
                        contador1 += 1
                    if (valOpuesto == '2'):
                        contador2 += 1
                    contador += 1
            resta += 1
        if (contador == 15 and (contador1 > 0 or contador2 > 0)):
            return True
        # Si llega a este punto, el juego sigue
        return False


def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None, contador=1):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        global contador
        print(contador)
        contador += 1
        if cutoff_test(state, depth) or depth >= d:
            return eval_fn(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        global contador
        print(contador)
        contador += 1
        if cutoff_test(state, depth) or depth >= d:
            return eval_fn(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth >
                                   d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


if __name__ == '__main__':
    game = Game()
    print(game.table)
    p1 = game.player1
    p2 = game.player2
    p1.scan(game)
    p1.possible_moves(game.table)
    for move in p1.moves:
        print(move)
    depth = 2
    print(game.table)
    contador = 0
    variable = alpha_beta_cutoff_search(
        game.table, game, depth, game.terminal_test, game.utility, contador)
    print('J1 decide jugar: {}'.format(variable))
    # while not game.terminal_test(game.table):
    #   print('TURNO DE {}'.format('J1' if game.turn else 'J2'))
    #   if game.turn:
    #     variable = alpha_beta_cutoff_search(game.table, game)
    #     print('J1 decide jugar: {}'.format(variable))
    #     game.makeMove(variable)
    #     p1.madeMove()
    #     p2.scan(game)
    #     p2.possible_moves(game.table)
    #   else:
    #     variable = alpha_beta_cutoff_search(game.table, game)
    #     print('J2 decide jugar: {}'.format(variable))
    #     game.makeMove(variable)
    #     p2.madeMove()
    #     p1.scan(game)
    #     p1.possible_moves(game.table)
    #   print(game.table)

    print(game.checkGameState())
