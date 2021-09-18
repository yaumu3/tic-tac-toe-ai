import math
import random
from copy import deepcopy
from typing import Generic, Optional

from .. import Action, Model, Strategy

INF = 1 << 60


class MCTSStrategy(Strategy[Action]):
    def get_action(self, model: Model[Action]) -> Action:
        root = ModelNode[Action](model, leading_action=None)
        root.expand()
        for _ in range(100):
            root.evaluate()
        assert root.children is not None
        root.children.sort(key=lambda c: c.n)
        best_action = root.children[-1].leading_action
        assert best_action is not None
        return best_action


class ModelNode(Generic[Action]):
    def __init__(self, model: Model[Action], leading_action: Optional[Action]) -> None:
        self.model = model
        self.leading_action: Optional[Action] = leading_action
        self.w: int = 0
        self.n: int = 0
        self.children: Optional[list[ModelNode[Action]]] = None

    def expand(self) -> None:
        self.children = []
        for action in self.model.get_legal_actions():
            child_model = deepcopy(self.model)
            self.tick_model(child_model, action)
            self.children.append(ModelNode(child_model, leading_action=action))

    def evaluate(self) -> int:
        has_winner = self.model.state.has_winner()
        is_draw = self.model.state.is_draw()
        if has_winner or is_draw:
            value = -1 if has_winner else 0
            self.w += value
            self.n += 1
            return value
        if self.children is None:
            playout_model = deepcopy(self.model)
            value = self.playout(playout_model)
            self.w += value
            self.n += 1
            if self.n == 10:
                self.expand()
            return value
        value = -self.next_child().evaluate()
        self.w += value
        self.n += 1
        return value

    def next_child(self) -> "ModelNode[Action]":
        assert self.children is not None
        for child in self.children:
            if child.n == 0:
                return child

        # UCB1
        t = sum(c.n for c in self.children)
        ucb1s = [-c.w / c.n + math.sqrt(2 * math.log(t) / c.n) for c in self.children]
        return self.children[ucb1s.index(max(ucb1s))]

    @staticmethod
    def tick_model(model: Model[Action], action: Action) -> None:
        model.state.operate(model.current_player, action)
        model.switch_player()

    def playout(self, model: Model[Action]) -> int:
        if model.state.has_winner():
            return -1
        if model.state.is_draw():
            return 0
        actions = model.get_legal_actions()
        self.tick_model(model, random.choice(actions))
        return -self.playout(model)
