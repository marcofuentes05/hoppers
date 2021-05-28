from main import Game

def utility(table, player):
    param = player.identifier
    (fila, columna) = player.initialPosition
    utility = 0
    if (fila, columna) == (0,0):
      for i in range(5):
        for j in range(i+1):
          table.table[4-i][j].value = 'N'
          table.table[-1-j][i+5].value = 'O'
          # utility += 1 if table.table[9-j][9-i].value != '.' else 0
          # utility = utility - (1 if table.table[j][i].value != '.' else 0)
    else:
      for i in range(5,10):
        for j in range(5,i+1):
            utility += 1 if table.table[-1-i][j-5].value != '.' else 0
            utility = utility - (1 if table.table[4-j][i].value != '.' else 0)
    return utility

if __name__ == '__main__':
    game = Game()
    p1 = game.player1
    p2 = game.player2
    game.table.table[0][3].value= '.'
    game.table.table[1][4].value='1'
    print(game.table)
    print(utility(game.table, p1))
    print(game.table)
