from typing import Optional

from ...event import Event
from ..import Action, Player, State, Strategy


class HumanStrategy(Strategy[Action]):
    def __init__(self):
        self.await_input_event = Event()
        self.action: Optional[Action] = None

    def get_action(self, player: Player[Action], state: State[Action]) -> Action:
        actions = state.get_legal_actions(player)
        self.await_input_event.trigger(actions=actions)
        assert self.action is not None
        return self.action

    def set_action(self, action: Action):
        self.action = action
