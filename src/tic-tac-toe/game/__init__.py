from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from ..event import Event

Action = TypeVar("Action")


@dataclass(frozen=True)
class Player(Generic[Action]):
    color: str
    strategy: "Strategy[Action]"

    def pick_action(self, model: "Model[Action]") -> Action:
        return self.strategy.get_action(model)


class State(Generic[Action], metaclass=ABCMeta):
    @abstractmethod
    def is_draw(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def has_winner(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def operate(self, player: Player[Action], action: Action) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_legal_actions(self, player: Player[Action]) -> list[Action]:
        raise NotImplementedError


class Model(Generic[Action]):
    def __init__(
        self,
        state_factory: Callable[[], State[Action]],
        players: tuple[Player[Action], Player[Action]],
    ) -> None:
        self.state_factory = state_factory
        self.reset()

        self.players = players
        self._current_player_idx = 0
        self.current_player = players[0]

        self.update_state_event = Event()
        self.has_winner_event = Event()
        self.is_draw_event = Event()

    def tick(self) -> None:
        action = self.current_player.pick_action(self)
        self.state.operate(self.current_player, action)
        self.update_state_event.trigger(action=action, player=self.current_player)

        is_over = False
        if self.state.has_winner():
            self.has_winner_event.trigger()
            is_over = True
        if self.state.is_draw():
            self.is_draw_event.trigger()
            is_over = True
        if not is_over:
            self.switch_player()

    def switch_player(self) -> None:
        self._current_player_idx ^= 1
        self.current_player = self.players[self._current_player_idx]

    def get_legal_actions(self) -> list[Action]:
        return self.state.get_legal_actions(self.current_player)

    def reset(self) -> None:
        self.state = self.state_factory()


class Strategy(Generic[Action], metaclass=ABCMeta):
    @abstractmethod
    def get_action(self, model: Model[Action]) -> Action:
        raise NotImplementedError
