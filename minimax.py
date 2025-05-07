import random
from tic_tac_toe import TicTacToe


def minimax(game, depth, maximizing_player):
    if game.is_terminal() or depth == 0:
        return game.evaluate(), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move, 'X')
            eval, _ = minimax(new_game, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move, 'O')
            eval, _ = minimax(new_game, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def play_game(k):
    game = TicTacToe()
    player = random.choice(['X', 'O'])  # Decide random quien empieza
    nodes_explored = 0

    while not game.is_terminal():
        if player == 'X':
            _, move = minimax(game, k, True)
        else:
            move = random.choice(game.available_moves())
        game.make_move(move, player)
        player = 'O' if player == 'X' else 'X'
    
    return game.evaluate()

def experiment(N, k):
    wins = 0
    ties = 0
    losses = 0

    for _ in range(N):
        result = play_game(k)
        if result == 1:
            wins += 1
        elif result == 0:
            ties += 1
        else:
            losses += 1

    print(f"Wins: {wins}, Ties: {ties}, Losses: {losses}")

def minimax_with_count(game, depth, maximizing_player, counter):
        counter[0] += 1  # Contamos los nodos explorados
        if game.is_terminal() or depth == 0:
            return game.evaluate(), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in game.available_moves():
                new_game = game.copy()
                new_game.make_move(move, 'X')
                eval, _ = minimax_with_count(new_game, depth - 1, False, counter)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in game.available_moves():
                new_game = game.copy()
                new_game.make_move(move, 'O')
                eval, _ = minimax_with_count(new_game, depth - 1, True, counter)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move
if __name__ == "__main__":
    N = 1000  # Número de juegos
    k = 3     # Profundidad de minimax

    wins = 0
    ties = 0
    losses = 0
    total_nodes = 0

    for _ in range(N):
        game = TicTacToe()
        player = random.choice(['X', 'O'])
        nodes_explored_in_game = [0]  # Lo ponemos como lista para ser mutable en minimax_with_count

        while not game.is_terminal():
            if player == 'X':
                _, move = minimax_with_count(game, k, True, nodes_explored_in_game)
            else:
                move = random.choice(game.available_moves())
            game.make_move(move, player)
            player = 'O' if player == 'X' else 'X'

        # Contar el resultado
        result = game.evaluate()
        if result == 1:
            wins += 1
        elif result == 0:
            ties += 1
        else:
            losses += 1

        total_nodes += nodes_explored_in_game[0]

    print("\n=== Resultados después de {} juegos ===".format(N))
    print(f"Victorias: {wins}")
    print(f"Empates: {ties}")
    print(f"Derrotas: {losses}")
    print(f"Promedio de nodos explorados por juego: {total_nodes / N:.2f}")
