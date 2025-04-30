import random
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
    return max(root.children, key=lambda c: c.si).move

def play_mtc(n_sims, c):
    game = TicTacToe()
    player = random.choice(['X','O'])
    
    while not game.is_terminal():
        if player =='X':
            move = mtc(game, n_sims, True, c)
        else:
            move = random.choice(game.available_moves())
        game.make_move(move, player)
        player = 'O' if player == 'X' else 'X'
    return game.current_winner()
    
def experiment(n_sim, c, N):
    data = {"winner": []}
    for _ in range(N):
        t = play_mtc(n_sim, c)
        if t:
            data["winner"].append(t)
        else: 
            data["winner"].append("tie")
    df = pd.DataFrame(data)
    counts = df["winner"].value_counts()
    return counts

def value_tune():
    N = 300
    sim_opt = [10, 50, 100, 200, 500]
    c_opt = [0.1, 0.5, 1.0, 1.41, 2.0, 3.0, 5.0]
    matrix = np.zeros((len(c_opt),len(sim_opt)))
    for i,c in enumerate(c_opt):
        for j,n in enumerate(sim_opt):
            rslt = experiment(n, c, N)["X"] / N
            matrix[i][j] = rslt
    plt.imshow(matrix, cmap='viridis', vmin=matrix.min(), vmax=matrix.max())
    plt.xticks(ticks=np.arange(len(sim_opt)), labels=sim_opt)
    plt.yticks(ticks=np.arange(len(c_opt)), labels=c_opt)
    plt.xlabel("Number of Simulations")
    plt.ylabel("C Value")
    plt.colorbar(label='Value')
    plt.title("MTC Win Percentage")
    plt.show()

value_tune()