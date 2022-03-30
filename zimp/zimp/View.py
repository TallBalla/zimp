from pyfiglet import Figlet
from termcolor import colored

class View():
    def __init__(self):
        self.figlet = Figlet(font='sblood')

    def heading(self, text):
        print(colored(self.figlet.renderText(text), 'white', 'on_grey'))

    def sub_heading(self, text):
        print(colored(f'\n{text}', 'white', 'on_grey'))

    def message(self, text):
        print(colored(f'\n{text}', 'green'))

    def warning(self, text):
        print(colored(f'\n{text}', 'yellow'))

    def error(self, text):
        print(colored(f'\n{text}', 'red'))

    def display_start_heading(self):
        self.heading('Starting')
        self.sub_heading('Type help or "?" to list the commands or "start" to start the game')

    def display_player(self, player, time, state):
        print(f'It is {time} pm \n'
              f'The player currently has {player.get_health()} health \n'
              f'The player currently has {player.get_attack()} attack \n'
              f'The players items are {player.get_items()}\n'
              f'The game state is {state}\n')
    
    def display_game(self, chosen_tile, state, avail_doors, suggest_cmd):
        print(f'\nCurrent Room: {chosen_tile.name}\n'
              f'Available Doors: {avail_doors}\n'
              f'Special Entrances : {chosen_tile.entrance}\n'
              f'Current Player State: {state}\n'
              f'Suggested Command: {suggest_cmd}\n')

    def warning_dinning_room_exit(self):
        self.warning("Dining room entrance must face an empty tile")

    def warning_enter_valid_file_name(self):
        self.warning('Must enter a valid file name')

    def warning_invalid_run_direction(self):
        self.warning('Must enter a vaild direction')

    def error_player_cannot_move(self):
        self.error('Player not ready to move')

    def error_cannot_cower(self):
        self.error('Cannot cower while right now')

    def error_cannot_runaway(self):
        self.error('Cannot runaway currently')

    def error_cannot_search(self):
        self.error('Cannot search for items currently')

    def error_file_does_not_exist(self, file_name):
        self.error(f'{file_name} file does not exist, '
                   'try another file or create file')