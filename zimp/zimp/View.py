from pyfiglet import Figlet
from termcolor import colored
from tile import Tile
from player import Player


class View():
    def __init__(self):
        self.figlet = Figlet(font='sblood')

    def heading(self, text: str) -> None:
        print(colored(self.figlet.renderText(text), 'white', 'on_grey'))

    def sub_heading(self, text: str) -> None:
        print(colored(f'\n{text}', 'white', 'on_grey'))

    def message(self, text: str) -> None:
        print(colored(f'\n{text}', 'green'))

    def warning(self, text: str) -> None:
        print(colored(f'\n{text}', 'yellow'))

    def error(self, text: str) -> None:
        print(colored(f'\n{text}', 'red'))

    def display_start_heading(self) -> None:
        self.heading('Starting')
        self.sub_heading('Type help or "?" to list the commands or "start"'
                         ' to start the game')

    def display_player(self, player: Player, time: int, state: str) -> None:
        print(f'It is {time} pm \n'
              f'The player currently has {player.get_health()} health \n'
              f'The player currently has {player.get_attack()} attack \n'
              f'The players items are {player.get_items()}\n'
              f'The game state is {state}\n')

    def display_game(self,
                     chosen_tile: Tile,
                     state: str,
                     avail_doors: str,
                     suggest_cmd: str) -> None:
        print(f'\nCurrent Room: {chosen_tile.name}\n'
              f'Available Doors: {avail_doors}\n'
              f'Special Entrances : {chosen_tile.entrance}\n'
              f'Current State: {state}\n'
              f'Suggested Command: {suggest_cmd}\n')

    def display_state(self, state: str) -> None:
        print(f'Current State: {state}')
