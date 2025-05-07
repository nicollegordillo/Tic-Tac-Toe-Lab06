import time
import csv
import random

from minimax import minimax_with_count
from tic_tac_toe import TicTacToe
from alphabeta import alphabeta
from mtc_search import mtc


def run_minimax(N, k, x_starts):
    wins, ties, losses, total_nodes = 0, 0, 0, 0
    for _ in range(N):
        game = TicTacToe()
        player = 'X' if x_starts else 'O'
        counter = [0]
        while not game.is_terminal():
            if player == 'X':
                _, move = minimax_with_count(game, k, True, counter)
            else:
                move = random.choice(game.available_moves())
            game.make_move(move, player)
            player = 'O' if player == 'X' else 'X'
        result = game.evaluate()
        wins += result == 1
        ties += result == 0
        losses += result == -1
        total_nodes += counter[0]
    return wins, ties, losses, total_nodes / N


def run_alphabeta(N, k, x_starts):
    wins, ties, losses, total_nodes = 0, 0, 0, 0
    for _ in range(N):
        game = TicTacToe()
        player = 'X' if x_starts else 'O'
        counter = [0]
        while not game.is_terminal():
            if player == 'X':
                _, move = alphabeta(game, k, float('-inf'), float('inf'), True, counter)
            else:
                move = random.choice(game.available_moves())
            game.make_move(move, player)
            player = 'O' if player == 'X' else 'X'
        result = game.evaluate()
        wins += result == 1
        ties += result == 0
        losses += result == -1
        total_nodes += counter[0]
    return wins, ties, losses, total_nodes / N


def run_mcts(N, n_sims, c, x_starts):
    wins, ties, losses = 0, 0, 0
    for _ in range(N):
        game = TicTacToe()
        player = 'X' if x_starts else 'O'
        while not game.is_terminal():
            if player == 'X':
                move = mtc(game, n_sims, True, c)
            else:
                move = random.choice(game.available_moves())
            game.make_move(move, player)
            player = 'O' if player == 'X' else 'X'
        result = game.evaluate()
        wins += result == 1
        ties += result == 0
        losses += result == -1
    return wins, ties, losses, "N/A"


def main():
    N = 300  # juegos por configuración
    results = []
    header = ['Algoritmo', 'Parámetros', '¿Empieza X?', 'X Gana', 'Empates', 'O Gana', 'Prom. Nodos', 'Tiempo (s)']

    minimax_ks = [2, 3]
    alphabeta_ks = [3, 4]
    mcts_params = [(100, 1.0), (200, 1.41)]

    for k in minimax_ks:
        for x_first in [True, False]:
            start = time.time()
            wins, ties, losses, avg_nodes = run_minimax(N, k, x_first)
            duration = time.time() - start
            results.append(['Minimax', f'k={k}', x_first, wins, ties, losses, avg_nodes, round(duration, 2)])

    for k in alphabeta_ks:
        for x_first in [True, False]:
            start = time.time()
            wins, ties, losses, avg_nodes = run_alphabeta(N, k, x_first)
            duration = time.time() - start
            results.append(['Alpha-Beta', f'k={k}', x_first, wins, ties, losses, avg_nodes, round(duration, 2)])

    for sims, c in mcts_params:
        for x_first in [True, False]:
            start = time.time()
            wins, ties, losses, avg_nodes = run_mcts(N, sims, c, x_first)
            duration = time.time() - start
            results.append(['MCTS', f'sims={sims}, c={c}', x_first, wins, ties, losses, avg_nodes, round(duration, 2)])

    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(results)

    for row in results:
        print(row)


if __name__ == "__main__":
    main()
