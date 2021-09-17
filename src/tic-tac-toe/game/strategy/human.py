from typing import Optional

from ...event import Event
from .. import Action, Model, Strategy


class HumanStrategy(Strategy[Action]):
    def __init__(self):
        self.await_input_event = Event()
        self.action: Optional[Action] = None

    def get_action(self, model: Model[Action]) -> Action:
        actions = model.get_legal_actions()
        self.await_input_event.trigger(actions=actions)
        assert self.action is not None
        return self.action

    def set_action(self, action: Action):
        self.action = action
