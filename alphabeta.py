import random
from tic_tac_toe import TicTacToe

def alphabeta(game, depth, alpha, beta, maximizing_player, counter):
    counter[0] += 1
    if game.is_terminal() or depth == 0:
        return game.evaluate(), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move, 'X')
            eval, _ = alphabeta(new_game, depth - 1, alpha, beta, False, counter)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Poda beta
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move, 'O')
            eval, _ = alphabeta(new_game, depth - 1, alpha, beta, True, counter)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda alfa
        return min_eval, best_move

def experiment_alphabeta(N, k):
    wins = ties = losses = total_nodes = 0

    for _ in range(N):
        game = TicTacToe()
        player = random.choice(['X', 'O'])
        counter = [0]

        while not game.is_terminal():
            if player == 'X':
                _, move = alphabeta(game, k, float('-inf'), float('inf'), True, counter)
            else:
                move = random.choice(game.available_moves())
            game.make_move(move, player)
            player = 'O' if player == 'X' else 'X'

        result = game.evaluate()
        if result == 1:
            wins += 1
        elif result == 0:
            ties += 1
        else:
            losses += 1
        total_nodes += counter[0]

    print(f"=== Resultados Alfa-Beta después de {N} juegos ===")
    print(f"Victorias: {wins}")
    print(f"Empates: {ties}")
    print(f"Derrotas: {losses}")
    print(f"Promedio de nodos explorados por juego: {total_nodes / N:.2f}")
    
if __name__ == "__main__":
    experiment_alphabeta(N=100, k=3)
