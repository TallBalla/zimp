from OutdoorTile import OutdoorTile
from IndoorTile import IndoorTile
from Player import Player
from DevCard import DevCard
from Tile import Tile

from directions import Direction as d
import pandas as pd

import pickle
import random

class Game:
    def __init__(self, player, time=9, game_map=None, indoor_tiles=None, outdoor_tiles=None, chosen_tile=None,
                 dev_cards=None, state="Starting", current_move_direction=None, can_cower=True):
        if indoor_tiles is None:
            indoor_tiles = []  # Will contain a list of all available indoor tiles
        if outdoor_tiles is None:
            outdoor_tiles = []  # Will contain a list of all available outdoor tiles
        if dev_cards is None:
            dev_cards = []  # Will contain a list of all available development cards
        if game_map is None:
            game_map = {}  # Tiles dictionary will have the x and y co-ords as the key and the Tile object as the value
        self.player = player
        self.time = time
        self.indoor_tiles = indoor_tiles
        self.outdoor_tiles = outdoor_tiles
        self.dev_cards = dev_cards
        self.tiles = game_map
        self.chosen_tile = chosen_tile
        self.state = state
        self.current_move_direction = current_move_direction
        self.current_zombies = 0
        self.can_cower = can_cower
        self.room_item = None

    # start Willem checks
    def check_tile_name_foyer(self, tile):
        return tile.name == 'Foyer'

    def check_state_is_moving(self):
        return self.state == 'Moving'

    def check_state_is_rotating(self):
        return self.state == 'Rotating'

    def check_state_is_choosing_door(self):
        return self.state == 'Choosing Door'

    def check_state_is_drawing_dev_card(self):
        return self.state == 'Drawing Dev Card'
    
    # end Willem checks

    def start_game(self):  #  Run to initialise the game
        self.load_tiles()
        self.load_dev_cards()
        for tile in self.indoor_tiles:
            if self.check_tile_name_foyer(tile):  # Game always starts in the Foyer at 16,16
                self.chosen_tile = tile
                self.state = "Rotating"
                break

    def get_game(self):
        s = ''
        f = ''
        if self.check_state_is_moving():
            s = "In this state you are able to move the player using the movement commands of n, e, s, w"
        if self.check_state_is_rotating():
            s = "Use the rotate command to rotate tiles and align doors," \
                " Once you are happy with the door position you can place the tile with the place command"
        if self.check_state_is_choosing_door():
            s = "Choose where to place a new door with the choose command + n, e, s, w"
        if self.check_state_is_drawing_dev_card():
            s = "Use the draw command to draw a random development card"
        for door in self.chosen_tile.doors:
            f += door.name + ', '
        return print(f' The chosen tile is {self.chosen_tile.name}, the available doors in this room are {f}\n '
                     f'The state is {self.state}. {s} \n Special Entrances : {self.chosen_tile.entrance}')

    def get_player_status(self):
        return print(f'It is {self.get_time()} pm \n'
                     f'The player currently has {self.player.get_health()} health \n'
                     f'The player currently has {self.player.get_attack()} attack \n'
                     f'The players items are {self.player.get_items()}\n'
                     f'The game state is {self.state}')

    def get_time(self):
        return self.time

    # Loads tiles from excel file
    def load_tiles(self):  # Needs Error handling in this method
        excel_data = pd.read_excel('Tiles.xlsx')
        tiles = []
        for name in excel_data.iterrows():
            tiles.append(name[1].tolist())
        for tile in tiles:
            doors = self.resolve_doors(tile[3], tile[4], tile[5], tile[6])
            if self.check_tile_outdoors_index(2, tile):
                new_tile = OutdoorTile(tile[0], tile[1], doors)
                if self.check_tile_patio(0, tile):
                    new_tile.set_entrance(d.NORTH)
                self.outdoor_tiles.append(new_tile)
            if self.check_tile_indoors_index(2, tile):
                new_tile = IndoorTile(tile[0], tile[1], doors)
                if self.check_tile_dining_room(0, tile):
                    new_tile.set_entrance(d.NORTH)
                self.indoor_tiles.append(new_tile)

    # start willem checks
    def check_tile_outdoors_index(self, index, tile):
        return tile[index] == 'Outdoor'

    def check_tile_indoors_index(self, index, tile):
        return tile[index] == 'Indoor'

    def check_tile_dining_room(self, index, tile):
        return tile[index] == 'Dining Room'

    def check_tile_patio(self, index, tile):
        return tile[index] == 'Patio'
    
    def check_current_tile_type_indoors(self):
        return self.get_current_tile().type == "Indoor"

    def check_current_tile_name_dining_room(self):
        return self.get_current_tile().name == "Dining Room"

    def check_player_facing_exit(self):
        return self.current_move_direction == self.get_current_tile().entrance

    def check_player_can_move_outside(self):
        return self.check_current_tile_name_dining_room() \
            and self.check_player_facing_exit()
    # end willem checks

    def draw_tile(self, x, y):  # Called when the player moves through a door into an un-discovered room to
        if self.check_current_tile_type_indoors():  # get a new tile
            if len(self.indoor_tiles) == 0:
                return print("No more indoor tiles")
            if self.check_player_can_move_outside():
                t = [t for t in self.outdoor_tiles if t.name == "Patio"]
                tile = t[0]
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
            else:
                tile = random.choice(self.indoor_tiles)  # Chooses a random indoor tile and places it
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
        elif self.get_current_tile().type == "Outdoor":
            if len(self.outdoor_tiles) == 0:
                return print("No more outdoor tiles")
            tile = random.choice(self.outdoor_tiles)
            tile.set_x(x)
            tile.set_y(y)
            self.chosen_tile = tile

    # Loads development cards from excel file
    def load_dev_cards(self):
        #TODO complete the exception for try catch
        try:
            card_data = pd.read_excel('DevCards.xlsx')
        except:
            print('cannot load file, check its in the corret')
        for card in card_data.iterrows():
            item = card[1][0]
            event_one = (card[1][1], card[1][2])
            event_two = (card[1][3], card[1][4])
            event_three = (card[1][5], card[1][6])
            charges = card[1][7]
            dev_card = DevCard(item, charges, event_one, event_two, event_three)
            self.dev_cards.append(dev_card)
        random.shuffle(self.dev_cards)
        self.dev_cards.pop(0)
        self.dev_cards.pop(0)

    # start willem checks
    def check_state_is_running(self):
        return self.state == "Running" 

    def check_cant_move_to_room(self, x, y):
        return self.check_for_room(x, y) is False

    # end willem checks

    def move_player(self, x, y):  # Moves the player coordinates to the selected tile, changes game state
        self.player.set_y(y)
        self.player.set_x(x)
        if self.check_state_is_running():
            self.state = "Moving"
        else:
            self.state = "Drawing Dev Card"

    def get_tile_at(self, x, y):  # Returns the tile given x and y coordinates
        return self.tiles[(x, y)]

    def select_move(self, direction):  # Takes the player input and runs all checks to make sure the move is valid
        x, y = self.get_destination_coords(direction)
        if self.check_for_door(direction):  # If there's a door where the player tried to move
            self.current_move_direction = direction
            if self.check_cant_move_to_room(x, y):
                if self.check_state_is_running():
                    return print("Can only run into a discovered room")
                else:
                    self.draw_tile(x, y)
                    self.state = "Rotating"
            if self.check_for_room(x, y):
                if self.check_indoor_outdoor_move(self.get_current_tile().type, self.get_tile_at(x, y).type):
                    return print("Cannot Move this way")
                else:
                    self.move_player(x, y)

    def check_indoor_outdoor_move(self, current_type, move_type):  # Makes sure player can only move outside through
        if current_type != move_type and self.get_current_tile().name != "Patio" or "Dining Room":  # the dining room
            return False

    # start willem checks
    def check_direct_north(self, direction):
        return direction == d.NORTH    
    
    def check_direct_south(self, direction):
        return direction == d.SOUTH

    def check_direct_east(self, direction):
        return direction == d.EAST

    def check_direct_west(self, direction):
        return direction == d.WEST

    def check_for_door(self, direction):
        return direction in self.get_current_tile().doors

    def check_coordinates_in_tiles(self, x, y):
        return (x, y) not in self.tiles

    def check_direct_south_not_in_doors(self):
        return d.SOUTH not in self.chosen_tile.doors

    def check_direct_north_not_in_doors(self):
        return d.NORTH not in self.chosen_tile.doors

    def check_direct_east_not_in_doors(self):
        return d.EAST not in self.chosen_tile.doors

    def check_direct_west_not_in_doors(self):
        return d.WEST not in self.chosen_tile.doors
    # end willem checks

    def get_destination_coords(self, direction):  # Gets the x and y value of the proposed move
        if self.check_direct_north(direction):
            return self.player.get_x(), self.player.get_y() - 1
        if self.check_direct_south(direction):
            return self.player.get_x(), self.player.get_y() + 1
        if self.check_direct_east(direction):
            return self.player.get_x() + 1, self.player.get_y()
        if self.check_direct_west(direction):
            return self.player.get_x() - 1, self.player.get_y()

    def check_for_room(self, x, y):  # Takes a move direction and checks if there is a room there
        if self.check_coordinates_in_tiles(x, y):
            return False
        self.chosen_tile = self.tiles[(x, y)]
        return True

    def check_doors_align(self, direction):  # Makes sure when placing a tile that a door is facing where the player is
        if self.check_tile_name_foyer(self.get_current_tile()):  # Trying to come from
            return True
        if self.check_direct_north(direction):
            if self.check_direct_south_not_in_doors():
                return False
        if self.check_direct_south(direction):
            if self.check_direct_north_not_in_doors():
                return False
        if self.check_direct_west(direction):
            if self.check_direct_east_not_in_doors():
                return False
        elif self.check_direct_east(direction):
            if self.check_direct_west_not_in_doors():
                return False
        return True

    # start willem checks
    def check_current_tile_entrance_north(self):
        return self.get_current_tile().entrance == d.NORTH    
    
    def check_current_tile_entrance_south(self):
        return self.get_current_tile().entrance == d.SOUTH   
    
    def check_current_tile_entrance_west(self):
        return self.get_current_tile().entrance == d.WEST   
    
    def check_current_tile_entrance_east(self):
        return self.get_current_tile().entrance == d.EAST

    def check_choosen_tile_entrance_south(self):
        return self.chosen_tile.entrance == d.SOUTH

    def check_choosen_tile_entrance_north(self):
        return self.chosen_tile.entrance == d.NORTH

    def check_choosen_tile_entrance_east(self):
        return self.chosen_tile.entrance == d.EAST

    def check_choosen_tile_entrance_west(self):
        return self.chosen_tile.entrance == d.WEST

    def check_current_direct_north_and_entrance_south(self, tile):
        return self.current_move_direction == d.NORTH and tile.entrance == d.SOUTH

    def check_current_direct_south_and_entrance_north(self, tile):
        return self.current_move_direction == d.SOUTH and tile.entrance == d.NORTH

    def check_current_direct_east_and_entrance_west(self, tile):
        return self.current_move_direction == d.EAST and tile.entrance == d.WEST

    def check_current_direct_west_and_entrance_east(self, tile):
        return self.current_move_direction == d.WEST and tile.entrance == d.EAST

    # end willem checks

    def check_entrances_align(self):  # Makes sure the dining room and patio entrances align
        if self.check_current_tile_entrance_north():
            if self.check_choosen_tile_entrance_south():
                return True
        if self.check_current_tile_entrance_south():
            if self.check_choosen_tile_entrance_north():
                return True
        if self.check_current_tile_entrance_west():
            if self.check_choosen_tile_entrance_east():
                return True
        if self.check_current_tile_entrance_east():
            if self.check_choosen_tile_entrance_west():
                return True
        return print(" Dining room and Patio entrances dont align")

    def check_dining_room_has_exit(self):  # used to make sure the dining room exit is not facing an existing door
        tile = self.chosen_tile
        if tile.name == "Dining Room":
            if self.check_current_direct_north_and_entrace_south(tile):
                return False
            if self.check_current_direct_south_and_entrance_north(tile):
                return False
            if self.check_current_direct_east_and_entrance_west(tile):
                return False
            if self.check_current_direct_west_and_entrance_east(tile):
                return False
        else:
            return True


    # start willem checks

    def check_tile_outdoors(self, tile):
        return tile.type == "Outdoor"

    def check_current_tile_has_exits(self):
        return self.get_current_tile().name == "Dining Room" or "Patio"

    # end willem checks

    def place_tile(self, x, y):  # Places the tile into the game map dictionary
        tile = self.chosen_tile
        self.tiles[(x, y)] = tile  # The location of the tile is stored as a tuple as the key of the dictionary entry
        self.state = "Moving"  # And the tile is stored as the value
        if self.check_tile_outdoors(tile):
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
            return
        self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self):  # returns the current tile that the player is at
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def rotate(self):  # Rotates a selected tile one position clockwise during the Rotating state
        tile = self.chosen_tile
        tile.rotate_tile()
        if self.check_tile_name_foyer(tile):
            return
        if self.check_current_tile_has_exits():
            tile.rotate_entrance()

    # start willem check

    def check_list_len(self, list, length):
        return len(list) == length

    def check_time_is_up(self):
        return self.get_time == 11

    def check_event_type(self, event, type):
        return event[0] == type

    def check_event_consequence_less_than_one(self, event):
        return event[1] < 1

    def check_event_consequence_greater_than_one(self, event):
        return event[1] > 1

    def check_event_consequence_equal_to_one(self, event):
        return event[1] == 1
    # end willem check

    # Call when player enters a room and draws a dev card
    def trigger_dev_card(self, time):
        if self.check_list_len(self.dev_cards, 0):
            if self.check_time_is_up():
                print("You have run out of time")
                self.lose_game()
                return

            print("Reshuffling The Deck")
            self.load_dev_cards()
            self.time += 1

        dev_card = self.dev_cards[0]
        self.dev_cards.pop(0)
        event = dev_card.get_event_at_time(time)  # Gets the event at the current time
        if self.check_event_type(event, "Nothing"):
            print("There is nothing in this room")
            if len(self.chosen_tile.doors) == 1 and self.chosen_tile.name != "Foyer":
                self.state = "Choosing Door"
                self.get_game()
                return
            else:
                self.state = "Moving"
                self.get_game()
            return
        elif self.check_event_type(event, "Health"):  # Change health of player
            print("There might be something in this room")
            self.player.add_health(event[1])

            if self.check_event_consequence_greater_than_one(event):
                print(f"You gained {event[1]} health")
                self.state = "Moving"
            elif self.check_event_consequence_less_than_one(event):
                print(f"You lost {event[1]} health")
                self.state = "Moving"
                if self.player.get_health() <= 0:
                    self.lose_game()
                    return
            elif self.check_event_consequence_equal_to_one(event):
                print("You didn't gain or lose any health")
            if len(self.chosen_tile.doors) == 1 and self.chosen_tile.name != "Foyer":
                self.state = "Choosing Door"
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
            else:
                self.state = "Moving"
                self.get_game()
        elif self.check_event_type(event, "Item"):  # Add item to player's inventory if there is room
            if len(self.dev_cards) == 0:
                if self.get_time == 11:
                    print("You have run out of time")
                    self.lose_game()
                    return
                else:
                    print("Reshuffling The Deck")
                    self.load_dev_cards()
                    self.time += 1
            next_card = self.dev_cards[0]
            print(f"There is an item in this room: {next_card.get_item()}")
            if len(self.player.get_items()) < 2:
                self.dev_cards.pop(0)
                self.player.add_item(next_card.get_item(), next_card.charges)
                print(f"You picked up the {next_card.get_item()}")
                if len(self.chosen_tile.doors) == 1 and self.chosen_tile.name != "Foyer":
                    self.state = "Choosing Door"
                    self.get_game()
                else:
                    self.state = "Moving"
                    self.get_game()
            else:
                self.room_item = [next_card.get_item(), next_card.charges]
                response = input("You already have two items, do you want to drop one of them? (Y/N) ")
                if response == "Y" or response == "y":
                    self.state = "Swapping Item"
                else: # If player doesn't want to drop item, just move on
                    self.state = "Moving"
                    self.room_item = None
                    self.get_game()
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
        elif event[0] == "Zombies":  # Add zombies to the game, begin combat
            print(f"There are {event[1]} zombies in this room, prepare to fight!")
            self.current_zombies = int(event[1])
            self.state = "Attacking"  # Create CMD for attacking zombies

    # Call in CMD if state is attacking, *items is a list of items the player is going to use
    def trigger_attack(self, *item):
        player_attack = self.player.get_attack()
        zombies = self.current_zombies
        if len(item) == 2:  # If the player is using two items
            if "Oil" in item and "Candle" in item:
                print("You used the oil and the candle to attack the zombies, it kills all of them")
                self.drop_item("Oil")
                self.state = "Moving"
                return
            elif "Gasoline" in item and "Candle" in item:
                print("You used the gasoline and the candle to attack the zombies, it kills all of them")
                self.drop_item("Gasoline")
                self.state = "Moving"
                return
            elif "Gasoline" in item and "Chainsaw" in item:
                chainsaw_charge = self.player.get_item_charges("Chainsaw")
                self.player.set_item_charges("Chainsaw", chainsaw_charge + 2)
                player_attack += 3
                self.drop_item("Gasoline")
                self.player.use_item_charge("Chainsaw")
            else:
                print("These items cannot be used together, try again")
                return
        elif len(item) == 1:
            if "Machete" in item:
                player_attack += 2
            elif "Chainsaw" in item:
                if self.player.get_item_charges("Chainsaw") > 0:
                    player_attack += 3
                    self.player.use_item_charge("Chainsaw")
                else:
                    print("This item has no charges left")            
            elif "Golf Club" in item or "Grisly Femur" in item or "Board With Nails" in item:
                player_attack += 1
            elif "Can of Soda" in item:
                self.player.add_health(2)
                self.drop_item("Can of Soda")
                print("Used Can of Soda, gained 2 health")
                return
            elif "Oil" in item:
                self.trigger_run(0)
                return
            else:
                print("You cannot use this item right now, try again")
                return

        # Calculate damage on the player
        damage = zombies - player_attack
        if damage < 0:
            damage = 0
        print(f"You attacked the zombies, you lost {damage} health")
        self.can_cower = True
        self.player.add_health(-damage)
        if self.player.get_health() <= 0:
            self.lose_game()
            return
        else:
            self.current_zombies = 0
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
            self.state = "Moving"

    # Call if state is attacking and player wants to run away
    def trigger_run(self, direction, health_lost=-1):
        self.state = "Running"
        self.select_move(direction)
        if self.state == "Moving":
            self.player.add_health(health_lost)
            print(f"You run away from the zombies, and lose {health_lost} health")
            self.can_cower = True
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
        else:
            self.state = "Attacking"

    def trigger_room_effect(self, room_name):  # Used for the Garden and Kitchen special room effects
        if room_name == "Garden":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name} you have gained one health")
            self.state ="Moving"
        if room_name == "Kitchen":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name} you have gained one health")
            self.state ="Moving"

    # If player chooses to cower instead of move to a new room
    def trigger_cower(self):
        if self.can_cower:
            self.player.add_health(3)
            self.dev_cards.pop(0)
            self.state = "Moving"
            print("You cower in fear, gaining 3 health, but lose time with the dev card")
        else:
            return print("Cannot cower during a zombie door attack")

    # Call when player wants to drop an item, and state is dropping item
    def drop_item(self, old_item):
        for item in self.player.get_items():
            if item[0] == old_item:
                self.player.remove_item(item)
                print(f"You dropped the {old_item}")
                self.state = "Moving"
                return
        print("That item is not in your inventory")

    # Use an item in the players inventory
    def use_item(self, *item):
        if "Can of Soda" in item:
            self.player.add_health(2)
            self.drop_item("Can of Soda")
            print("Used Can of Soda, gained 2 health")
        elif "Gasoline" in item and "Chainsaw" in item:
            chainsaw_charge = self.player.get_item_charges("Chainsaw")
            self.player.set_item_charges("Chainsaw", chainsaw_charge + 2)
            self.drop_item("Gasoline")
        else:
            print("These items cannot be used right now")
            return

    def choose_door(self, direction):  # used to select where a door will be made during a zombie door attack
        if direction in self.chosen_tile.doors:
            print("Choose a NEW door not an existing one")
            return False
        else:
            self.chosen_tile.doors.append(direction)
            self.current_zombies = 3
            print(f"{self.current_zombies} Zombies have appeared, prepare for battle. Use the attack command to"
                  f" fight or the run command to flee")
            self.state = "Attacking"

    def search_for_totem(self):  # Used to search for a totem in the evil temple, will force the user to draw a dev card
        if self.get_current_tile().name == "Evil Temple":
            if self.player.has_totem:
                print("player already has the totem")
                return
            else:
                self.trigger_dev_card(self.time)
                self.player.found_totem()
        else:
            print("You cannot search for a totem in this room")

    def bury_totem(self):  #
        if self.get_current_tile().name == "Graveyard":
            if self.player.has_totem:
                self.trigger_dev_card(self.time)
                if self.player.health != 0:
                    print("You Won")
                    self.state = "Game Over"
        else:
            print("Cannot bury totem here")

    def check_for_dead_player(self):
        if self.player.health <= 0:
            return True
        else:
            return False

    @staticmethod
    def resolve_doors(n, e, s, w):
        doors = []
        if n == 1:
            doors.append(d.NORTH)
        if e == 1:
            doors.append(d.EAST)
        if s == 1:
            doors.append(d.SOUTH)
        if w == 1:
            doors.append(d.WEST)
        return doors

    def lose_game(self):
        self.state = "Game Over"