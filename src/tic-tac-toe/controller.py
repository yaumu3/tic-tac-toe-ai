from .game.strategy.human import HumanStrategy
from .game.strategy.random import RandomStrategy
from .model import TicTacToeModel, TicTacToePlayer
from .view import TicTacToeView


class TicTacToeController:
    def __init__(self):
        players = (
            TicTacToePlayer("x", RandomStrategy()),
            TicTacToePlayer("o", RandomStrategy()),
        )
        self.model = TicTacToeModel(players)
        self.view = TicTacToeView(self.model)

        self.model.update_state_event.add_listener(self.view.update_board)
        self.model.has_winner_event.add_listener(self.view.notify_winner)
        self.model.is_draw_event.add_listener(self.view.notify_draw)
        self.view.tick_event.add_listener(self.model.tick)

        for player in players:
            if isinstance(player.strategy, HumanStrategy):
                player.strategy.await_input_event.add_listener(self.view.ask_input)
                self.view.receive_input_event.add_listener(player.strategy.set_action)

    def run(self):
        self.view.render()
