import cmd
import pickle
from Player import Player
import os

from Game import Game
from directions import Direction as d

from View import View

class Commands(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.player = Player()
        self.game = Game(self.player)
        self.view = View()

    def display_game_info(self):
        self.view.display_game(self.game.get_chosen_tile(),
                               self.game.get_state(),
                               self.game.get_availiable_doors(),
                               self.game.get_suggested_command())

    def move(self, direction):
        if self.game.state == "Moving":
            self.game.select_move(direction)
            self.display_game_info()
        else:
            self.view.error_player_cannot_move()

    def do_state(self, linke):
        """Gets the state of the Game"""
        state = self.game.get_state()
        self.view.display_state(state)

    def do_start(self, line):
        """Starts a new game or rests old game"""
        if self.game.get_state() == "Starting":
            print('\nGame already started, enter "place" to select tile rotation')
            return

        self.game.start_game()

        self.view.display_start_heading()

        self.game.start_game_play()
        self.display_game_info()

    def do_rotate(self, line):
        """Rotates the current map piece 1 rotation clockwise"""
        if self.game.state == "Rotating":
            self.game.rotate()
            self.display_game_info()
        else:
            print("warning")

    def do_place(self, line):
        """Places the current map tile"""
        if self.game.state == "Rotating":
            if self.game.chosen_tile.name == "Foyer":
                self.game.place_tile(16, 16)

            elif self.game.check_dining_room_has_exit() is False:
                self.view.warning_dinning_room_exit()
            else:
                if self.game.get_current_tile().name == "Dining Room" \
                    and self.game.current_move_direction == self.game.get_current_tile().entrance:
                    if self.game.check_entrances_align():
                        self.game.place_tile(self.game.chosen_tile.x,
                                             self.game.chosen_tile.y)
                        self.game.move_player(self.game.chosen_tile.x,
                                              self.game.chosen_tile.y)
                    print("Dining room and Patio entrances dont align")
                elif self.game.check_doors_align(self.game.current_move_direction):
                    self.game.place_tile(self.game.chosen_tile.x, self.game.chosen_tile.y)
                    self.game.move_player(self.game.chosen_tile.x, self.game.chosen_tile.y)
                else:
                    print('You must have at least one door facing the way you came from,'
                          ' enter "rotate" to line up doors')
        self.display_game_info()

        

    def do_choose(self, direction):
        """When a zombie door attack is completed. Use this command to select an exit door with a valid direction"""
        valid_inputs = ["north", "east", "south", "west"]
        if direction not in valid_inputs:
            return print("Input a valid direction. (Check choose help for more information)")
        if direction == 'north':
            direction = d.NORTH
        if direction == "east":
            direction = d.EAST
        if direction == "south":
            direction = d.SOUTH
        if direction == "west":
            direction = d.WEST
        if self.game.state == "Choosing Door":
            self.game.can_cower = False
            self.game.choose_door(direction)
        else:
            print("Cannot choose a door right now")

    def do_north(self, line):
        """Moves the player North if in moving state"""
        self.move(d.NORTH)

    def do_south(self, line):
        """Moves the player South if in moving state"""
        self.move(d.SOUTH)

    def do_east(self, line):
        """Moves the player East if in moving state"""
        self.move(d.EAST)

    def do_west(self, line):
        """Moves the player West if in moving state"""
        self.move(d.WEST)

    def do_save(self, line):
        """Takes a filepath and saves the game to a file"""
        if not line:
            return print("Must enter a valid file name")
        else:
            if len(self.game.tiles) == 0:
                return print("Cannot save game with empty map")
            file_name = line + '.pickle'
            with open(file_name, 'wb') as f:
                pickle.dump(self.game, f)

    def do_load(self, name):
        """\nTakes a filepath and loads the game from a file 
        Useage: load <file name>\n"""
        if not name:
            self.view.warning_enter_valid_file_name()
            return

        file_name = name + '.pickle'
        try:
            with open(file_name, 'rb') as f:
                self.game = pickle.load(f)
                self.game.get_game()
        except FileNotFoundError:
            self.view.error_file_does_not_exist(file_name)

    def do_fight(self, line):
        """Player attacks the zombies"""
        arg1 = ''
        arg2 = 0
        if "," in line:
            arg1, arg2 = [item for item in line.split(", ")]
        else:
            arg1 = line

        if self.game.state == "Attacking":
            if arg1 == '':
                self.game.trigger_attack()
            elif arg2 == 0:
                self.game.trigger_attack(arg1)
            elif arg1 != '' and arg2 != 0:
                self.game.trigger_attack(arg1, arg2)

            if len(self.game.chosen_tile.doors) == 1\
               and self.game.chosen_tile.name != "Foyer":
                self.game.state = "Choosing Door"
                self.display_game_info()
            if self.game.state == "Game Over":
                print("You lose, game over, you have succumbed to the zombie horde")
                print('To play again, type "start"')
            else:
                self.display_game_info()
        else:
            print("You cannot attack right now")

    def do_item(self, line):
        """Player uses item if item equiped"""
        arg1 = ''
        arg2 = 0
        if "," in line:
            arg1, arg2 = [item for item in line.split(", ")]
        else:
            arg1 = line

        if self.game.state == "Moving":
            if arg1 == '':
                return
            if arg2 == 0:
                self.game.use_item(arg1)
            elif arg1 != '' and arg2 != 0:
                self.game.use_item(arg1, arg2)
        else:
            print("You cannot do that right now")

    # Not finished yet, needs testing for spelling
    def do_drop(self, item):
        """Drops an item from your hand"""
        if self.game.state != "Game Over":
            self.game.drop_item(item)
            self.display_game_info()
    
    def do_swap(self, line):
        """Swaps an item in you hand with the one in the room"""
        if self.game.state == "Swapping Item":
            self.game.drop_item(line)
            self.game.player.add_item(self.game.room_item[0],
                                     self.game.room_item[1])
            self.game.room_item = None
            self.display_game_info()

    def do_draw(self, line):
        """Draws a new development card (Must be done after evey move)"""
        if self.game.state == "Drawing Dev Card":
            self.game.trigger_dev_card(self.game.time)
        else:
            print("Cannot currently draw a card")

    # DELETE LATER, DEV COMMANDS FOR TESTING
    def do_give(self, line):
        self.game.player.add_item("Oil", 2)
    def do_give2(self, line):
        self.game.player.add_item("Candle", 1)

    def do_runaway(self, direction):
        """\nUse when attacked and take only 1 damage
        Directions: north, south, east, west
        Useage: runaway <direction>\n"""
        if direction is None:
             self.view.warning_invalid_run_direction()

        if self.game.state == "Attacking":
            if direction == 'north':
                self.game.trigger_run(d.NORTH)
            elif direction == 'east':
                self.game.trigger_run(d.EAST)
            elif direction == 'south':
                self.game.trigger_run(d.SOUTH)
            elif direction == 'west':
                self.game.trigger_run(d.WEST)
               
            if len(self.game.get_current_tile().doors) == 1 \
               and self.game.chosen_tile.name != "Foyer":
                self.game.state = "Choosing Door"
                self.display_game_info()
        else:
            self.view.error_cannot_runaway()

    def do_cower(self, line):
        """When attacked use this command to cower. You will take no damage but will advance the time"""
        if self.game.state == "Moving":
            self.game.trigger_cower()
        else:
            self.view.error_cannot_cower()

    def do_search(self, line):
        """Searches for the zombie totem. (Player must be in the evil temple and will have to resolve a dev card)"""
        if self.game.state == "Moving":
            self.game.search_for_totem()
        else:
            self.view.error_cannot_search()

    def do_bury(self, line):
        """Buries the totem when in moving state"""
        if self.game.state == "Moving":
            self.game.bury_totem()
        else:
            print("Cannot currently bury the totem")

    def do_prompt(self, line):
        """Change the interactive prompt"""
        self.prompt = line + '# '

    def do_EOF(self, line):
        """Exits the game without saving"""
        return True

    def do_player(self, line):
        """Shows the status of the player"""
        player = self.game.get_player()
        time = self.game.get_time()
        state = self.game.get_state()

        if self.game.state != "Game Over":
            self.view.display_player(player, time, state)

    def get_game(self):
        return self.game