# Modified by Willem
import cmd
import pickle
import os
from Game import Game
from Player import Player
from View import View
from directions import Direction as d


class Commands(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.player = Player()
        self.game = Game(self.player)
        self.view = View()

    def display_game_info(self) -> None:
        self.view.display_game(self.game.get_chosen_tile(),
                               self.game.get_state(),
                               self.game.get_availiable_doors(),
                               self.game.get_suggested_command())

    def move(self, direction: d) -> None:
        """\nUse when in moving state
        Directions: north, south, east, west\n"""
        if self.game.state == "Moving":
            self.game.select_move(direction)
            self.display_game_info()
        else:
            self.view.error('Player not ready to move')

    def do_state(self, line: str) -> None:
        """Gets the state of the player"""
        state = self.game.get_state()
        self.view.display_state(state)

    def do_start(self) -> None:
        """Starts or resets game"""
        if self.game.get_state() == "Starting":
            self.view.error('\nGame already started, enter "place"'
                            ' to select tile rotation')
            return

        self.game.start_game()
        self.view.display_start_heading()
        self.game.start_game_play()
        self.display_game_info()

    def do_rotate(self, line: str) -> None:
        """Rotates the current map piece 1 rotation clockwise"""
        if self.game.state == "Rotating":
            self.game.rotate()
            self.display_game_info()
        else:
            self.view.error("Cannot rotate the tile")

    def check_current_tile_dinning_room(self) -> bool:
        return self.game.get_current_tile().name == "Dining Room"

    def check_current_direct_equals_entrance_direct(self) -> bool:
        return (self.game.current_move_direction
                == self.game.get_current_tile().entrance)

    def check_can_go_outside(self) -> bool:
        return (self.check_current_direct_equals_entrance_direct
                and self.check_current_tile_dinning_room())

    def check_doors_align(self) -> bool:
        return self.game.check_doors_align(self.game.current_move_direction)

    def do_place(self, line: str) -> bool:
        """Place the tile when player happy with rotation"""
        if self.game.state == "Rotating":
            if self.game.chosen_tile.name == "Foyer":
                self.game.place_tile(16, 16)

            elif self.game.check_dining_room_has_exit() is False:
                self.view.warning("Dining room entrance must"
                                  " face an empty tile")
            else:
                if self.check_can_go_outside():
                    if self.game.check_entrances_align():
                        self.game.place_tile(self.game.chosen_tile.x,
                                             self.game.chosen_tile.y)
                        self.game.move_player(self.game.chosen_tile.x,
                                              self.game.chosen_tile.y)
                    self.view.warning("Dining room and Patio"
                                      " entrances dont align")
                elif self.check_doors_align():
                    self.game.place_tile(self.game.chosen_tile.x,
                                         self.game.chosen_tile.y)
                    self.game.move_player(self.game.chosen_tile.x,
                                          self.game.chosen_tile.y)
                else:
                    self.view.warning('You must have at least one'
                                      ' door facing the way you came from,'
                                      ' enter "rotate" to line up doors')
        self.display_game_info()

    def do_choose(self, direction: str) -> bool:
        """Availble aftera zombie door attack is completed.
           Use this command to select an exit door with a valid direction"""
        valid_inputs = ["north", "east", "south", "west"]
        if direction not in valid_inputs:
            self.view.error("Input a valid direction.\
                            (Check choose help for more information)")
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
            self.view.warning("Cannot choose a door right now")

    def do_north(self, line: str) -> None:
        """Moves the player North if in moving state"""
        self.move(d.NORTH)

    def do_south(self, line: str) -> None:
        """Moves the player South if in moving state"""
        self.move(d.SOUTH)

    def do_east(self, line: str) -> None:
        """Moves the player East if in moving state"""
        self.move(d.EAST)

    def do_west(self, line: str) -> None:
        """Moves the player West if in moving state"""
        self.move(d.WEST)

    def do_save(self, line: str) -> None:
        """\nSaves a file to the file path of the game
        Useage: save <file name>\n"""
        if not line:
            self.view.warning("Must enter a valid file name")
        else:
            if len(self.game.tiles) == 0:
                self.view.error("Cannot save game with empty tiles")
            file_name = line + '.pickle'
            with open(file_name, 'wb') as f:
                pickle.dump(self.game, f)

    def do_load(self, name: str) -> None:
        """\nLoads a file to the file path of the game
        Useage: load <file name>\n"""
        if not name:
            self.view.warning('Must enter a valid file name')
            return

        file_name = name + '.pickle'
        try:
            with open(file_name, 'rb') as f:
                self.game = pickle.load(f)
                self.game.get_game()
        except FileNotFoundError:
            self.view.error(f'{file_name} file does not exist, '
                            'try another file or create file')

    def do_fight(self, line: str) -> None:
        """Used when encounter zombie and will take damage
        Damage equation is (zombie amount - player attack)"""

        arg1, arg2 = [item for item in line.split(", ")]

        if self.game.state == "Attacking":
            # if arg1 == '':
            if arg1 == '':
                self.game.trigger_attack()
            elif arg1 != '' and arg2 == '':
                self.game.trigger_attack(arg1)
            elif arg1 != '' and arg2 != '':
                self.game.trigger_attack(arg1, arg2)
            self.handle_next_move()
        else:
            self.view.warning("You cannot attack right now")

    def handle_next_move(self):
        if len(self.game.chosen_tile.doors) == 1\
               and self.game.chosen_tile.name != "Foyer":
            self.game.state = "Choosing Door"
            self.display_game_info()
        if self.game.state == "Game Over":
            self.view.error("You lose, game over, you have"
                             "succumbed to the zombie horde")
            self.view.message('To play again, type "start"')
        else:
            self.display_game_info()

    def do_item(self, line: str) -> None:
        """Uses a item that the player has equiped"""
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
            self.view.warning("You cannot do that right now")

    def do_drop(self, item: str) -> None:
        """Drops an item from your hand"""
        if self.game.state != "Game Over":
            self.game.drop_item(item)
            self.display_game_info()

    def do_swap(self, line: str) -> None:
        """Swaps an item that the user holds with new item"""
        if self.game.state == "Swapping Item":
            self.game.drop_item(line)
            self.game.player.add_item(self.game.room_item[0],
                                      self.game.room_item[1])
            self.game.room_item = None
            self.display_game_info()

    def do_draw(self) -> None:
        """Draws a new development card (Must be done after evey move)"""
        if self.game.state == "Drawing Dev Card":
            self.game.trigger_dev_card(self.game.time)
        else:
            self.view.warning("Cannot currently draw a card")

    def do_runaway(self, direction: str) -> None:
        """\nUse when attacked and take only 1 damage
        Directions: north, south, east, west
        Useage: runaway <direction>\n"""
        if direction is None:
            self.view.warning('Must enter a vaild direction')

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
            self.view.error('Cannot runaway currently')

    def do_cower(self, line: str) -> None:
        """When attacked use this command to cower.
        You will take no damage but will advance the time"""
        if self.game.state == "Moving":
            self.game.trigger_cower()
        else:
            self.view.error('Cannot cower while right now')

    def do_search(self, line: str) -> None:
        """Searches for the zombie totem.
        (Player must be in the evil temple
        and will have to resolve a dev card)"""
        if self.game.state == "Moving":
            self.game.search_for_totem()
        else:
            self.view.error('Cannot search for items currently')

    def do_bury(self, line: str) -> None:
        """Buries the totem when in moving state"""
        if self.game.state == "Moving":
            self.game.bury_totem()
        else:
            self.view.error("Cannot currently bury the totem")

    def do_EOF(self, line: str) -> bool:
        """Quits the game, will not save progress"""
        return True

    def do_player(self, line: str) -> None:
        """Shows player and game information"""
        player = self.game.get_player()
        time = self.game.get_time()
        state = self.game.get_state()

        if self.game.state != "Game Over":
            self.view.display_player(player, time, state)

    def get_game(self) -> None:
        return self.game
