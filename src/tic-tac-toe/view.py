from .event import Event
from .model import TicTacToeAction, TicTacToeModel, TicTacToePlayer, TicTacToeState


class TicTacToeView:
    def __init__(self, model: TicTacToeModel) -> None:
        self.model = model
        self.tick_event = Event()
        self.receive_input_event = Event()

    def render(self) -> None:
        self.print_board()
        while not (self.model.state.has_winner() or self.model.state.is_draw()):
            print(f"--- Player {self.model.current_player.color}'s turn ---")
            self.tick_event.trigger()

    def print_board(self) -> None:
        assert isinstance(self.model.state, TicTacToeState)
        board = []
        for i in range(3):
            row = []
            for j in range(3):
                player = self.model.state.board[3 * i + j]
                if player is None:
                    row.append(str(3 * i + j))
                else:
                    row.append(player.color)
            board.append(" ".join(row))
        print("\n".join(board))

    def update_board(self, action: TicTacToeAction, player: TicTacToePlayer):
        print(f"{player.color} chose {action.pos}")
        self.print_board()

    def notify_winner(self) -> None:
        print(f"\n[GAMEOVER] {self.model.current_player.color} is the winner.")

    def notify_draw(self) -> None:
        print("\n[GAMEOVER] Draw.")

    def ask_input(self, actions: list[TicTacToeAction]) -> None:
        action = None
        while action is None:
            pos = input("Choose a position: ")
            cand = [a for a in actions if str(a.pos) == pos]
            if len(cand) == 0:
                continue
            action = cand[0]
            break
        self.receive_input_event.trigger(action=action)
