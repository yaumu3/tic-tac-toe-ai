import random

from .. import Action, Model, Strategy


class RandomStrategy(Strategy[Action]):
    def get_action(self, model: Model[Action]) -> Action:
        actions = model.get_legal_actions()
        return random.choice(actions)
