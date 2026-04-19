import random
from typing import Dict


class SnakeAndLadders:
    def __init__(self) -> None:
        self.board_size = 100
        self.players = ["Player 1", "Player 2"]
        self.positions = {player: 0 for player in self.players}
        self.snakes: Dict[int, int] = {
            99: 54,
            95: 72,
            92: 51,
            83: 19,
            73: 1,
            69: 33,
            64: 36,
            59: 17,
            55: 7,
            48: 9,
            37: 4,
        }
        self.ladders: Dict[int, int] = {
            2: 38,
            8: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100,
        }

    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def move_player(self, player: str, roll: int) -> None:
        current = self.positions[player]
        new_position = current + roll

        if new_position > self.board_size:
            print(f"{player} needs an exact roll to reach 100. Stays at {current}.")
            return

        print(f"{player} moves from {current} to {new_position}")

        if new_position in self.ladders:
            print(f"Yay! {player} climbed a ladder from {new_position} to {self.ladders[new_position]}")
            new_position = self.ladders[new_position]
        elif new_position in self.snakes:
            print(f"Oops! {player} got bitten by a snake from {new_position} to {self.snakes[new_position]}")
            new_position = self.snakes[new_position]

        self.positions[player] = new_position
        print(f"{player} is now at {new_position}\n")

    def display_positions(self) -> None:
        print("Current positions:")
        for player, position in self.positions.items():
            print(f"  {player}: {position}")
        print()

    def play(self) -> None:
        print("Welcome to Snake and Ladders!")
        print("First player to reach 100 wins.\n")

        turn = 0
        while True:
            player = self.players[turn % len(self.players)]
            input(f"{player}, press Enter to roll the dice...")
            roll = self.roll_dice()
            print(f"{player} rolled a {roll}")
            self.move_player(player, roll)
            self.display_positions()

            if self.positions[player] == self.board_size:
                print(f"Congratulations! {player} wins the game!")
                break

            turn += 1


if __name__ == "__main__":
    game = SnakeAndLadders()
    game.play()
