from .game import bencher, strategy
from .model import TicTacToeModel, TicTacToePlayer
from .view import TicTacToeBencherView, TicTacToeView


class TicTacToeController:
    def __init__(self):
        players = (
            TicTacToePlayer("x", strategy.RandomStrategy()),
            TicTacToePlayer("o", strategy.AlphaBetaStrategy()),
        )
        self.model = TicTacToeModel(players)
        self.view = TicTacToeView(self.model)

        self.model.update_state_event.add_listener(self.view.update_board)
        self.model.has_winner_event.add_listener(self.view.notify_winner)
        self.model.is_draw_event.add_listener(self.view.notify_draw)
        self.view.tick_event.add_listener(self.model.tick)

        for player in players:
            if isinstance(player.strategy, strategy.HumanStrategy):
                player.strategy.await_input_event.add_listener(self.view.ask_input)
                self.view.receive_input_event.add_listener(player.strategy.set_action)

    def run(self):
        self.view.render()


class TicTacToeBencherController:
    def __init__(self):
        players = (
            TicTacToePlayer("x", strategy.MCTSStrategy()),
            TicTacToePlayer("o", strategy.AlphaBetaStrategy()),
        )
        self.model = TicTacToeModel(players)
        self.bencher = bencher.Bencher(self.model)
        self.view = TicTacToeBencherView(self.model)

        self.view.start_bench_event.add_listener(self.bencher.bench)
        self.bencher.episode_done_event.add_listener(self.view.notify_progress)
        self.bencher.bench_done_event.add_listener(self.view.notify_result)

    def run(self):
        self.view.bench()
