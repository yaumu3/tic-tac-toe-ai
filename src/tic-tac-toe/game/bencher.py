from ..event import Event
from . import Model


class Bencher:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.scores = {player: 0.0 for player in model.players}
        self.bench_done_event = Event()

    def bench(self, n: int):
        for _ in range(n):
            first_player = self.model.current_player
            while not (self.model.state.is_draw() or self.model.state.has_winner()):
                self.model.tick()
            if self.model.state.is_draw():
                for player in self.model.players:
                    self.scores[player] += 1 / len(self.scores)
            if self.model.state.has_winner():
                self.scores[self.model.current_player] += 1

            if self.model.current_player == first_player:
                self.model.switch_player()
            self.model.reset()
        for player in self.model.players:
            self.scores[player] /= n
        self.bench_done_event.trigger(scores=self.scores)
