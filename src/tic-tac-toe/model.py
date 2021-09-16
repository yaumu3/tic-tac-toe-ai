from dataclasses import dataclass
from typing import Optional

from .game import Model, Player, State, Strategy


@dataclass
class TicTacToeAction:
    pos: int


class TicTacToePlayer(Player[TicTacToeAction]):
    def __init__(self, color: str, strategy: Strategy):
        super().__init__(color, strategy)


class TicTacToeState(State[TicTacToeAction]):
    def __init__(self) -> None:
        self.reset()

    def is_draw(self) -> bool:
        return all(self.board) and not self.has_winner()

    def has_winner(self) -> bool:
        return self._h_winner() or self._v_winner() or self._d_winner()

    def _h_winner(self) -> bool:
        return any(
            self.board[3 * i]
            and self.board[3 * i] == self.board[3 * i + 1] == self.board[3 * i + 2]
            for i in range(3)
        )

    def _v_winner(self) -> bool:
        return any(
            self.board[i] and self.board[i] == self.board[i + 3] == self.board[i + 6]
            for i in range(3)
        )

    def _d_winner(self) -> bool:
        return (
            self.board[0] is not None
            and self.board[0] == self.board[4] == self.board[8]
        ) or (
            self.board[2] is not None
            and self.board[2] == self.board[4] == self.board[6]
        )

    def operate(self, player: TicTacToePlayer, action: TicTacToeAction) -> None:
        assert self.board[action.pos] is None
        self.board[action.pos] = player

    def get_legal_actions(self, _: Player) -> list[TicTacToeAction]:
        return [TicTacToeAction(i) for i in range(9) if self.board[i] is None]

    def reset(self) -> None:
        self.board: list[Optional[Player]] = [None] * 9


class TicTacToeModel(Model[TicTacToeAction]):
    def __init__(
        self, players: tuple[Player[TicTacToeAction], Player[TicTacToeAction]]
    ) -> None:
        super().__init__(TicTacToeState, players)
