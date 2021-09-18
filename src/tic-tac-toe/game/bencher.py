from ..event import Event
from . import Model


class Bencher:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.scores = {player: 0.0 for player in model.players}
        self.episode_done_event = Event()
        self.bench_done_event = Event()

    def bench(self, n: int):
        for i in range(n):
            first_player = self.model.current_player
            while not (self.model.state.is_draw() or self.model.state.has_winner()):
                self.model.tick()
            if self.model.state.is_draw():
                for player in self.model.players:
                    self.scores[player] += 1
            if self.model.state.has_winner():
                self.scores[self.model.current_player] += len(self.scores)

            if self.model.current_player == first_player:
                self.model.switch_player()
            self.model.reset()
            self.episode_done_event.trigger(current_episode=i + 1, episodes=n)
        for player in self.model.players:
            self.scores[player] /= n * len(self.scores)
        self.bench_done_event.trigger(scores=self.scores)
