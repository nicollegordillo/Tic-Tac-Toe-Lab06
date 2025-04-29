import random

import numpy as np
from tic_tac_toe import TicTacToe
import copy
class Mtc_Node:
    def __init__(self, state, start_player, move):
        self.parent = None
        self.state = state
        self.move = move
        self.moves = self.state.available_moves()
        self.children = []
        self.player = start_player
        # Simulations with wins
        self.wi = 0
        # Total simulations
        self.si = 0
    
    def ucb(self, child, c=1.41):
        return(
            (child.wi/child.si) + c*np.sqrt(np.log(self.si)/child.si)
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
        child = Mtc_Node(new_state, not self.player, move)
        self.children.append(child)
        return child
def mtc(_root, n_sims, player):
    root = Mtc_Node(_root, player, None)
    
    
    for i in range(3):
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

def play_mtc(n_sims):
    game = TicTacToe()
    player = 'X'
    
    while not game.is_terminal():
        if player =='X':
            move = mtc(game, n_sims, True)
        else:
            move = random.choice(game.available_moves())
        game.make_move(move, player)
        player = 'O' if player == 'X' else 'X'
        game.print_board()
        print("\n")
    
    
play_mtc(5)