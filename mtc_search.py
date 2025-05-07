import random
import time
import numpy as np
import pandas as pd
from tic_tac_toe import TicTacToe
import matplotlib.pyplot as plt
class Mtc_Node:
    def __init__(self, state, start_player, move, c):
        self.parent = None
        self.state = state
        self.move = move
        self.moves = self.state.available_moves()
        self.children = []
        self.player = start_player
        
        self.c = c
        # Simulations with wins
        self.wi = 0
        # Total simulations
        self.si = 0
    
    def ucb(self, child):
        if child.si == 0:
            return float("inf")
        else:
            return(
                (child.wi/child.si) + self.c*np.sqrt(np.log(self.si)/child.si)
            )
    def best_child(self):
        q = float("-inf")
        best = None
        for c in self.children:
            utility = self.ucb(c)
            if utility > q:
                q = utility
                best = c
        return best

    def expand(self):
        move = self.moves.pop()
        new_state = self.state.copy()
        new_state.make_move(move, 
            'X' if not self.player else 'O'
        )
        child = Mtc_Node(new_state, not self.player, move, self.c)
        self.children.append(child)
        return child
def mtc(_root, n_sims, player, c):
    root = Mtc_Node(_root, player, None, c)
    root.si = 1
    nodes_explored = 0
    for _ in range(n_sims):
        node: Mtc_Node = root
        # 1. Selection
        while(
            (len(node.moves) == 0) and
            node.children
            ):
            node = node.best_child()
        
        # 2. Expansion
        if len(node.moves) != 0:
            node = node.expand()
            nodes_explored+=1
            
        # 3. Simulation
        current: TicTacToe = node.state
        player = node.player
        while not current.is_terminal():
            move = random.choice(current.available_moves())
            current.make_move(
                move,
                'X' if player else '0'              
                )
            player = not player

        # 4. Backpropagation
        w = current.evaluate()
        while node is not None:
            node.si+=1
            if player and w==1:
                node.wi+=1
            elif not player and w==-1:
                node.wi+=1
            node = node.parent
        # 5. Return most visited
        
    rslt =  max(root.children, key=lambda c: c.si)
    return (rslt.move, nodes_explored)

def play_mtc(n_sims, c, oponent):
    game = TicTacToe()
    init_player = random.choice(['X','O'])
    player = init_player
    subtree_visits = []
    while not game.is_terminal():
        if player =='X':
            move, visits = mtc(game, n_sims, True, c)
            subtree_visits.append(visits)
        else:
            if oponent == 'rand':
                move = random.choice(game.available_moves())
            else: ## Mtc
                move = mtc(game, n_sims, False, c)

        game.make_move(move, player)
        player = 'O' if player == 'X' else 'X'
    winner = game.current_winner()
    avg_visits = np.mean(subtree_visits)
    return (winner, init_player, avg_visits)
    
def experiment(n_sim, c, N, oponent):
    data = {"winner": [], "init_player": [], "visits": []}
    for _ in range(N):
        w, p, v = play_mtc(n_sim, c, oponent)
        if w:
            data["winner"].append(w)
        else: 
            data["winner"].append("tie")
        data["init_player"].append(p)
        data["visits"].append(v)
    df = pd.DataFrame(data)
    return df

# Best values: {n_sims = 300, c=0.5}
# oponent can be 'random', 'mtc' and 'minmax'
def print_experiment():
    start = time.time()
    result = experiment(100,2, 300, 'rand')
    end = time.time()
    wins = result[result["winner"] == 'X']['winner'].count()
    loss = result[result["winner"] == 'O']['winner'].count()
    ties = result[result["winner"] == 'tie']['winner'].count()
    nodes_explored = result["visits"].mean()
    avg_time = (end-start)/1000
    print("Cantidad de Victorias: ",wins)
    print("Cantidad de Perdidas: ",loss)
    print("Cantidad de Empates: ",ties)
    print("Nodos Visitados Promedio: ", nodes_explored)
    print("Tiempo Promedio (s): ", avg_time)
    
    

print_experiment()

# def value_tune():
#     N = 300
#     sim_opt = [10, 50, 100, 200, 500]
#     c_opt = [0.1, 0.5, 1.0, 1.41, 2.0, 3.0, 5.0]
#     matrix = np.zeros((len(c_opt),len(sim_opt)))
#     for i,c in enumerate(c_opt):
#         for j,n in enumerate(sim_opt):
#             rslt = experiment(n, c, N)["X"] / N
#             matrix[i][j] = rslt
#     plt.imshow(matrix, cmap='viridis', vmin=matrix.min(), vmax=matrix.max())
#     plt.xticks(ticks=np.arange(len(sim_opt)), labels=sim_opt)
#     plt.yticks(ticks=np.arange(len(c_opt)), labels=c_opt)
#     plt.xlabel("Number of Simulations")
#     plt.ylabel("C Value")
#     plt.colorbar(label='Value')
#     plt.title("MTC Win Percentage")
#     plt.show()
