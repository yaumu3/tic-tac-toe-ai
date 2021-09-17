from copy import deepcopy
from .. import Action, Model, Strategy


INF = 1 << 60


class AlphaBetaStrategy(Strategy[Action]):
    def get_action(self, model: Model[Action]) -> Action:
        actions = model.get_legal_actions()
        best_action = None
        alpha = -INF
        for action in actions:
            score = -self.alpha_beta(self._simulate(model, action), -INF, -alpha)
            if score > alpha:
                best_action = action
                alpha = score
        assert best_action is not None
        return best_action

    def _simulate(self, model: Model[Action], action: Action) -> Model[Action]:
        next_model = deepcopy(model)
        next_model.state.operate(next_model.current_player, action)
        next_model.switch_player()
        return next_model

    def alpha_beta(self, model: Model[Action], alpha: int, beta: int) -> int:
        if model.state.has_winner():
            return -1
        if model.state.is_draw():
            return 0

        for action in model.get_legal_actions():
            score = -self.alpha_beta(self._simulate(model, action), -beta, -alpha)
            if score > alpha:
                alpha = score
            if score >= beta:
                return alpha
        return alpha
