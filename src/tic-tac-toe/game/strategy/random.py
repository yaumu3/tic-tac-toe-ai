import random

from ..import Action, Player, State, Strategy


class RandomStrategy(Strategy[Action]):
    def get_action(self, player: Player[Action], state: State[Action]) -> Action:
        actions = state.get_legal_actions(player)
        return random.choice(actions)
