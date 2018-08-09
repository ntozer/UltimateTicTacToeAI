from .coord import Coord
from .model import Engine
from .view import View
from .GameAgents import *

import tkinter as tk

class Controller():
    def __init__(self, root, agent=None):
        self.model = Engine()
        self.view = View(root)
        self.view.pack(fill='both', expand=True)
        self.agent = RandomAgent()
    

    def restart(self):
        self.model.reset_game()


    def handle_click(self, event):
        x = ord(event.widget['text'][0]) - 65
        y = int(event.widget['text'][1])
        move = Coord(x, y)
        self.make_move(move)

        
    def make_move(self, move):
        if self.model.check_valid_move(move):
            # movement updates
            self.model.board[move.x][move.y] = self.model.player
            self.model.prev_move = move
            # game state updates
            self.model.update_master_board()
            self.model.update_game_state()
            # update visuals
            self.update_visuals(move)
            # player updates
            self.model.update_player()
            
            if self.agent is not None and self.model.player == 2 and self.model.game_state == 0:
                self.make_move(self.get_agent_move())


    def update_visuals(self, coord):
        
        def get_active_board_tile(coord):
            return self.view.board_spaces[coord.x][coord.y]

        active_tile = get_active_board_tile(coord)

        if active_tile['bg'] not in self.view.p1_colors and active_tile['bg'] not in self.view.p2_colors:
            color_idx = 1
            if active_tile['bg'] == self.view.valid_colors[0]:
                color_idx = 0
            if self.model.player == 1:
                active_tile.configure(bg=self.view.p1_colors[color_idx])
            else:
                active_tile.configure(bg=self.view.p2_colors[color_idx])


    def get_agent_move(self):
        move = self.agent.compute_next_move(self.model.board, self.model.get_valid_moves())
        return move


    def handle_enter(self, event):
        x = ord(event.widget['text'][0]) - 65
        y = int(event.widget['text'][1])
        hover_coord = Coord(x, y)
        
        if self.model.check_valid_move(hover_coord):
            colors_to_use = self.view.valid_colors
        else:
            colors_to_use = self.view.invalid_colors
            
        if event.widget['bg'] == self.view.colors[0]:
            event.widget.configure(bg=colors_to_use[0])
        elif event.widget['bg'] == self.view.colors[1]:
            event.widget.configure(bg=colors_to_use[1])


    def handle_leave(self, event):
        if event.widget['bg'] in [self.view.valid_colors[0], self.view.invalid_colors[0]]:
            event.widget.configure(bg=self.view.colors[0])
        elif event.widget['bg'] in [self.view.valid_colors[1], self.view.invalid_colors[1]]:
            event.widget.configure(bg=self.view.colors[1])


    def bind_actions(self):
        for i in range(9):
            for j in range(9):
                self.view.board_spaces[i][j].bind("<Enter>", self.handle_enter)
                self.view.board_spaces[i][j].bind("<Leave>", self.handle_leave)
                self.view.board_spaces[i][j].bind("<Button-1>", self.handle_click)