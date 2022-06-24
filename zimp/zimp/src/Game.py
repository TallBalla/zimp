import random
import doctest
from Tile import Tile
from OutdoorTile import OutdoorTile
from IndoorTile import IndoorTile
from DevCard import DevCard
from Player import Player
from Database import Database
from directions import Direction as d

from strategy_pattern.oneItemAttackStrategy import OneItemAttackStrategy
from strategy_pattern.twoItemAttackStrategy import TwoItemAttackStrategy
from strategy_pattern.attackContext import AttackContext

from flyweight_pattern.flyweightFactory import FlyweightFactory


class Game():
    def __init__(self,
                 player: Player,
                 time=9,
                 game_map=None,
                 indoor_tiles=None,
                 outdoor_tiles=None,
                 chosen_tile=None,
                 dev_cards=None,
                 state=None,
                 current_move_direction=None,
                 can_cower=True):
        if indoor_tiles is None:
            indoor_tiles = []
        if outdoor_tiles is None:
            outdoor_tiles = []
        if dev_cards is None:
            dev_cards = []
        if game_map is None:
            game_map = {}
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
        self.db = Database("zimp")
        self.player_attack = 0

        self.flywieght_factory = FlyweightFactory()

    # Start Willems Implementation
    def check_tile_name_foyer(self, tile: Tile) -> bool:
        return tile.name == 'Foyer'

    def check_state_is_moving(self):
        '''
        Checks current state is moving

        >>> g.check_state_is_moving()
        False

        >>> g.set_state('Moving')
        >>> g.check_state_is_moving()
        True
        '''
        return self.state == 'Moving'

    def check_state_is_rotating(self) -> bool:
        '''
        Check state is rotating

        >>> g.check_state_is_rotating()
        False

        >>> g.set_state('Rotating')
        >>> g.check_state_is_rotating()
        True
        '''
        return self.state == 'Rotating'

    def check_state_is_choosing_door(self) -> bool:
        '''
        Check state is choosing door

        >>> g.check_state_is_choosing_door()
        False

        >>> g.set_state('Choosing Door')
        >>> g.check_state_is_choosing_door()
        True
        '''
        return self.state == 'Choosing Door'

    def check_state_is_drawing_dev_card(self) -> bool:
        '''
        Check state is drawing dev card

        >>> g.check_state_is_drawing_dev_card()
        False

        >>> g.set_state('Drawing Dev Card')
        >>> g.check_state_is_drawing_dev_card()
        True
        '''
        return self.state == 'Drawing Dev Card'

    def check_state_is_starting(self) -> bool:
        '''
        Check state is starting

        >>> g.check_state_is_starting()
        False

        >>> g.start_game()
        >>> g.check_state_is_starting()
        True
        '''
        return self.state == 'Starting'

    def check_state_game_over(self) -> bool:
        '''
        Check state is Game over

        >>> g.check_state_game_over()
        False

        >>> g.lose_game()
        >>> g.check_state_game_over()
        True
        '''
        return self.state == 'Game Over'

    def check_dev_cards_is_empty(self) -> bool:
        '''
        Check draw card is empty

        >>> g.check_dev_cards_is_empty()
        True

        >>> g.load_dev_cards()
        >>> g.check_dev_cards_is_empty()
        False
        '''
        return len(self.dev_cards) == 0

    def check_tiles_is_empty(self) -> bool:
        '''
        Check tiles is empty

        >>> g.check_tiles_is_empty()
        True

        '''
        return len(self.tiles) == 0

    def check_indoor_tiles_is_empty(self) -> bool:
        '''
        Check indoor tile populated
        >>> g = Game(Player())
        >>> g.check_indoor_tiles_is_empty()
        True

        >>> g.load_tiles()
        >>> g.check_indoor_tiles_is_empty()
        False
        '''
        return len(self.indoor_tiles) == 0

    def check_outdoor_tiles_is_empty(self) -> bool:
        '''
        Check outdoor tile populated
        >>> g = Game(Player())
        >>> g.check_outdoor_tiles_is_empty()
        True

        >>> g.load_tiles()
        >>> g.check_outdoor_tiles_is_empty()
        False
        '''
        return len(self.outdoor_tiles) == 0

    def get_flyweight_factory(self) -> FlyweightFactory:
        return self.flywieght_factory

    def get_state(self) -> str:
        return self.state

    def set_state(self, state: str) -> None:
        self.state = state

    def get_dev_cards(self) -> list:
        return self.dev_cards

    def set_dev_cards(self, dev_cards: list) -> None:
        self.dev_cards = dev_cards

    def start_game(self) -> None:
        self.set_state('Starting')

    def set_time(self, time: int) -> None:
        self.time = time

    def set_chosen_tile_name(self, name: str) -> None:
        self.chosen_tile.name = name

    def get_chosen_tile_name(self) -> str:
        return self.chosen_tile.name

    def set_chosen_tile_doors(self, door: list) -> None:
        self.chosen_tile.doors = door

    def get_chosen_tile_door(self) -> list:
        return self.chosen_tile.doors

    def get_current_zombies(self) -> int:
        return self.current_zombies

    def check_tile_outdoors_index(self, index: int, tile: Tile) -> bool:
        return tile[index] == 'Outdoor'

    def check_tile_indoors_index(self, index: int, tile: Tile) -> bool:
        return tile[index] == 'Indoor'

    def check_tile_dining_room(self, index: int, tile: Tile) -> bool:
        return tile[index] == 'Dining Room'

    def check_tile_patio(self, index: int, tile: Tile) -> bool:
        return tile[index] == 'Patio'

    def check_current_tile_type_indoors(self) -> bool:
        return self.get_current_tile().type == "Indoor"

    def check_current_tile_name_dining_room(self) -> bool:
        return self.get_current_tile().name == "Dining Room"

    def check_player_facing_exit(self) -> bool:
        return self.current_move_direction == self.get_current_tile().entrance

    def check_player_can_move_outside(self) -> bool:
        return self.check_current_tile_name_dining_room() \
            and self.check_player_facing_exit()

    def check_state_is_running(self) -> bool:
        return self.state == "Running"

    def check_cant_move_to_room(self, x: int, y: int) -> bool:
        return self.check_for_room(x, y) is False

    def check_direct_north(self, direction: d) -> bool:
        '''
        Checks the direction is north

        >>> g.check_direct_north(d.SOUTH)
        False

        >>> g.check_direct_north(d.NORTH)
        True
        '''
        return direction == d.NORTH

    def check_direct_south(self, direction: d) -> bool:
        '''
        Checks the direction is south

        >>> g.check_direct_south(d.NORTH)
        False

        >>> g.check_direct_south(d.SOUTH)
        True
        '''
        return direction == d.SOUTH

    def check_direct_east(self, direction: d) -> bool:
        '''
        Checks the direction is east

        >>> g.check_direct_east(d.WEST)
        False

        >>> g.check_direct_east(d.EAST)
        True
        '''
        return direction == d.EAST

    def check_direct_west(self, direction: d) -> bool:
        '''
        Checks the direction is west

        >>> g.check_direct_west(d.EAST)
        False

        >>> g.check_direct_west(d.WEST)
        True
        '''
        return direction == d.WEST

    def check_for_door(self, direction: d) -> bool:
        return direction in self.get_current_tile().doors

    def check_coordinates_in_tiles(self, x: int, y: int) -> bool:
        return (x, y) not in self.tiles

    def check_direct_south_not_in_doors(self) -> bool:
        return d.SOUTH not in self.chosen_tile.doors

    def check_direct_north_not_in_doors(self) -> bool:
        return d.NORTH not in self.chosen_tile.doors

    def check_direct_east_not_in_doors(self) -> bool:
        return d.EAST not in self.chosen_tile.doors

    def check_direct_west_not_in_doors(self) -> bool:
        return d.WEST not in self.chosen_tile.doors

    def check_current_tile_entrance_north(self) -> bool:
        return self.get_current_tile().entrance == d.NORTH

    def check_current_tile_entrance_south(self) -> bool:
        return self.get_current_tile().entrance == d.SOUTH

    def check_current_tile_entrance_west(self) -> bool:
        return self.get_current_tile().entrance == d.WEST

    def check_current_tile_entrance_east(self) -> bool:
        return self.get_current_tile().entrance == d.EAST

    def check_choosen_tile_entrance_south(self) -> bool:
        return self.chosen_tile.entrance == d.SOUTH

    def check_choosen_tile_entrance_north(self) -> bool:
        return self.chosen_tile.entrance == d.NORTH

    def check_choosen_tile_entrance_east(self) -> bool:
        return self.chosen_tile.entrance == d.EAST

    def check_choosen_tile_entrance_west(self) -> bool:
        return self.chosen_tile.entrance == d.WEST

    def check_current_direct_north_and_entrance_south(self,
                                                      tile: Tile) -> bool:
        return self.current_move_direction == d.NORTH \
            and tile.entrance == d.SOUTH

    def check_current_direct_south_and_entrance_north(self,
                                                      tile: Tile) -> bool:
        return self.current_move_direction == d.SOUTH \
            and tile.entrance == d.NORTH

    def check_current_direct_east_and_entrance_west(self,
                                                    tile: Tile) -> bool:
        return self.current_move_direction == d.EAST \
            and tile.entrance == d.WEST

    def check_current_direct_west_and_entrance_east(self,
                                                    tile: Tile) -> bool:
        return self.current_move_direction == d.WEST \
            and tile.entrance == d.EAST

    def check_tile_outdoors(self, tile: Tile) -> bool:
        return tile.type == "Outdoor"

    def check_current_tile_has_exits(self) -> bool:
        return self.get_current_tile().name == "Dining Room" or "Patio"

    def check_list_len(self, list: list[any], length: int) -> bool:
        '''
        Checks if the list has the correct length

        >>> g.check_list_len([], 4)
        False

        >>> g.check_list_len([1, 2, 3], 3)
        True
        '''
        return len(list) == length

    def check_time_is_up(self) -> bool:
        '''
        Checks if the time is up

        >>> g.check_time_is_up()
        False

        >>> g.set_time(int(11))
        >>> g.check_time_is_up()
        True
        '''
        return self.time >= 11

    def check_event_type(self, event: list[any], type: str) -> bool:
        return event.type == type

    def check_event_consequence_less_than_one(self,
                                              event: list[any]) -> bool:
        return event.get_consquence() < 1

    def check_event_consequence_greater_than_one(self,
                                                 event: list[any]) -> bool:
        return event.get_consquence() > 1

    def check_event_consequence_equal_to_one(self,
                                             event: list[any]) -> bool:
        return event.get_consquence() == 1

    def get_suggested_command(self) -> str:
        if self.check_state_is_moving():
            return self.get_availiable_doors().lower()
        if self.check_state_is_rotating():
            return "rotate place"
        if self.check_state_is_choosing_door():
            return self.get_availiable_doors().lower()
        if self.check_state_is_drawing_dev_card():
            return "draw"
        if self.check_state_is_choosing_door():
            return "choose <direction>"
    # End Willems Implementation

    def start_game_play(self) -> None:
        self.load_tiles()
        self.load_dev_cards()
        for tile in self.indoor_tiles:
            if self.check_tile_name_foyer(tile):
                self.chosen_tile = tile
                self.set_state("Rotating")
                break

    def get_availiable_doors(self) -> str:
        return ' '.join(str(i.name) for i in self.chosen_tile.doors)

    def get_player(self) -> Player:
        return self.player

    def get_time(self) -> int:
        return self.time

    def get_chosen_tile(self) -> None:
        return self.chosen_tile

    # edited by Willem
    def load_tiles(self) -> None:
        self.db.create_tiles()
        self.db.insert_table_data("tiles")
        for tile in self.db.select_data('tiles'):
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

    def draw_tile(self, x: int, y: int) -> None:
        if self.check_current_tile_type_indoors():  # get a new tile
            if len(self.indoor_tiles) == 0:
                print("No more indoor tiles")
            if self.check_player_can_move_outside():
                t = [t for t in self.outdoor_tiles if t.name == "Patio"]
                tile = t[0]
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
            else:
                tile = random.choice(self.indoor_tiles)
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
            return
        if len(self.outdoor_tiles) == 0:
            print("No more outdoor tiles")
        tile = random.choice(self.outdoor_tiles)
        tile.set_x(x)
        tile.set_y(y)
        self.chosen_tile = tile

    # Edited by Willem
    def load_dev_cards(self) -> None:
        self.db.create_devcards()
        self.db.insert_table_data("devcards")
        for card in self.db.select_data("devcards"):
            dev_card = DevCard(self.flywieght_factory)
            dev_card.set_item(card[0], card[7])
            dev_card.add_event(card[1], card[2])
            dev_card.add_event(card[3], card[4])
            dev_card.add_event(card[5], card[6])
            self.dev_cards.append(dev_card)
        random.shuffle(self.dev_cards)
        self.dev_cards.pop(0)
        self.dev_cards.pop(0)

    def move_player(self, x: int, y: int) -> None:
        self.player.set_y(y)
        self.player.set_x(x)
        if self.check_state_is_running():
            self.set_state("Moving")
        else:
            self.set_state("Drawing Dev Card")

    def get_tile_at(self, x: int, y: int) -> Tile:
        return self.tiles[(x, y)]

    def select_move(self, direction: d) -> None:
        x, y = self.get_destination_coords(direction)
        if self.check_for_door(direction):
            self.current_move_direction = direction
            if self.check_cant_move_to_room(x, y):
                if self.check_state_is_running():
                    print("Can only run into a discovered room")
                else:
                    self.draw_tile(x, y)
                    self.set_state("Rotating")
            if self.check_for_room(x, y):
                if self.check_indoor_outdoor_move(self.get_current_tile().type,
                                                  self.get_tile_at(x, y).type):
                    print("Cannot Move this way")
                else:
                    self.move_player(x, y)

    def check_indoor_outdoor_move(self,
                                  current_type: str,
                                  move_type: str) -> bool:
        if current_type != move_type \
           and self.get_current_tile().name != "Patio" or "Dining Room":
            return False

    def get_destination_coords(self, direction: d) -> list[int, int]:
        if self.check_direct_north(direction):
            return [self.player.get_x(), self.player.get_y() - 1]
        if self.check_direct_south(direction):
            return [self.player.get_x(), self.player.get_y() + 1]
        if self.check_direct_east(direction):
            return [self.player.get_x() + 1, self.player.get_y()]
        if self.check_direct_west(direction):
            return [self.player.get_x() - 1, self.player.get_y()]

    def check_for_room(self, x: int, y: int) -> bool:
        if self.check_coordinates_in_tiles(x, y):
            return False
        self.chosen_tile = self.tiles[(x, y)]
        return True

    def check_doors_align(self, direction: d) -> bool:
        if self.check_tile_name_foyer(self.get_current_tile()):
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

    def check_entrances_align(self) -> bool:
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
        return False

    def check_dining_room_has_exit(self) -> bool:
        tile = self.chosen_tile
        if tile.name == "Dining Room":
            if self.check_current_direct_north_and_entrance_south(tile):
                return False
            if self.check_current_direct_south_and_entrance_north(tile):
                return False
            if self.check_current_direct_east_and_entrance_west(tile):
                return False
            if self.check_current_direct_west_and_entrance_east(tile):
                return False
        return True

    def place_tile(self, x: int, y: int) -> None:
        tile = self.chosen_tile
        self.tiles[(x, y)] = tile

        self.set_state("Moving")
        if self.check_tile_outdoors(tile):
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
            return
        self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self) -> Tile:
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def rotate(self) -> None:
        tile = self.chosen_tile
        tile.rotate_tile()
        if self.check_tile_name_foyer(tile):
            return
        if self.check_current_tile_has_exits():
            tile.rotate_entrance()

    def trigger_dev_card(self, time: int) -> None:
        if self.check_time_is_up():
            print("\nYou have run out of time\n")
            self.lose_game()
            return

        if self.check_list_len(self.dev_cards, 0):
            print("\nReshuffling The Deck\n")
            self.load_dev_cards()
            self.time += 1

        dev_card = self.dev_cards[0]
        self.dev_cards.pop(0)
        event = dev_card.get_event_at_time(time)
        if self.check_event_type(event, "Nothing"):
            print("\nThere is nothing in this room\n")
            if len(self.chosen_tile.doors) == 1 \
               and self.chosen_tile.get_name() != "Foyer":
                self.set_state("Choosing Door")
                self.get_suggested_command()
            else:
                self.set_state("Moving")
                self.get_suggested_command()
            return
        elif self.check_event_type(event, "Health"):  # Change health of player
            print("\nThere might be something in this room")
            self.player.add_health(event.get_consquence())

            if self.check_event_consequence_greater_than_one(event):
                print(f"You gained {event.get_consquence()} health\n")
                self.set_state("Moving")
            elif self.check_event_consequence_less_than_one(event):
                print(f"You lost {event.get_consquence()} health\n")
                self.set_state("Moving")
                if self.player.get_health() <= 0:
                    self.lose_game()
                    return
            else:
                print("You didn't gain or lose any health\n")
                self.set_state("Moving")

            if len(self.chosen_tile.doors) == 1 \
               and self.chosen_tile.get_name() != "Foyer":
                self.set_state("Choosing Door")
            if self.get_current_tile().get_name() == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().get_name())

        elif self.check_event_type(event, "Item"):
            if self.check_list_len(self.dev_cards, 0):
                if self.get_time() == 11:
                    print("\nYou have run out of time")
                    self.lose_game()
                    return
                else:
                    print("\nReshuffling The Deck")
                    self.load_dev_cards()
                    self.time += 1
            next_card = self.dev_cards[0]
            print(f"\nThere is an item in this room: {next_card.get_item()}")
            if len(self.player.get_items()) < 2:
                self.dev_cards.pop(0)
                self.player.add_item(next_card.get_item(), next_card.charges)
                print(f"You picked up the {next_card.get_item()}\n")
                if len(self.chosen_tile.get_avaliable_doors()) == 1 \
                   and self.chosen_tile.get_name() != "Foyer":
                    self.set_state("Choosing Door")
                    self.get_suggested_command()
                else:
                    self.set_state("Moving")
                    self.get_suggested_command()
            else:
                self.room_item = [next_card.get_item(), next_card.charges]
                response = input("\nYou already have two items, do you want"
                                 " to drop one of them? (Y/N) ")
                if response == "Y" or response == "y":
                    self.set_state("Swapping Item")
                else:
                    self.set_state("Moving")
                    self.room_item = None
                    self.get_suggested_command()
            if self.get_current_tile().get_name() == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().get_name())
        elif self.check_event_type(event, "Zombies"):
            print(f"\nThere are {event.get_consquence()} zombies in this room,"
                  "prepare to fight!\n")
            self.current_zombies = int(event.get_consquence())
            self.set_state("Attacking")

    def trigger_attack(self, *item_names: list[str]) -> None:
        self.player_attack = self.player.get_attack()

        one_item_attack_strategy = OneItemAttackStrategy(self)
        two_item_attack_strategy = TwoItemAttackStrategy(self)
        
        try:
            if len(item_names) == 2:
                attack_strategy = AttackContext(two_item_attack_strategy)
                attack_strategy.attack(item_names)
            elif len(item_names) == 1:
                attack_strategy = AttackContext(one_item_attack_strategy)
                attack_strategy.attack(item_names)
        except Exception as e:
            return

        damage = self.current_zombies - self.player_attack
        if damage < 0:
            damage = 0
        print(f"\nYou attacked the zombies, you lost {damage} health")
        self.can_cower = True
        self.player.add_health(-damage)
        if self.player.get_health() <= 0:
            self.lose_game()
            return
        else:
            self.current_zombies = 0
            self.player_attack = 0
            if self.get_current_tile().get_name() == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().get_name())
            self.set_state("Moving")

    def choose_avalible_door(self) -> d:
        current_tile = self.get_current_tile()
        # get first avalibe doors
        avaliable_door = current_tile.get_avaliable_doors()
        return avaliable_door[0]

    def trigger_run(self,
                    direction: d,
                    health_lost: int) -> None:
        self.set_state("Running")
        self.select_move(direction)
        if self.state == "Moving":
            self.player.add_health(health_lost)
            print(f"\nYou run away from the zombies, and"
                  " lose {health_lost} health\n")
            self.can_cower = True
            if self.get_current_tile().get_name() == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().get_name())
        else:
            self.set_state("Attacking")

    def trigger_room_effect(self, room_name: str) -> None:
        if room_name == "Garden":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name}"
                  " you have gained one health\n")
            self.set_state("Moving")
        if room_name == "Kitchen":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name}"
                  " you have gained one health\n")
            self.set_state("Moving")

    def trigger_cower(self) -> None:
        if self.can_cower:
            self.player.add_health(3)
            self.dev_cards.pop(0)
            self.set_state("Moving")
            print("\nYou cower in fear, gaining 3 health,"
                  " but lose time with the dev card\n")
        else:
            return print("\nCannot cower during a zombie door attack\n")

    def drop_item(self, old_item_name: str) -> None:
        for item_name in self.player.get_items_names():
            if item_name == old_item_name:
                self.player.remove_item(old_item_name)
                print(f"You dropped the {old_item_name}")
                self.set_state("Moving")
                return
        print("\nThat item is not in your inventory\n")

    def use_item(self, *item_names: any) -> None:
        if "Can of Soda" in item_names:
            self.player.add_health(2)
            self.drop_item("Can of Soda")
            print("Used Can of Soda, gained 2 health")
        elif "Gasoline" in item_names and "Chainsaw" in item_names:
            chainsaw_charge = self.player.get_item_charges("Chainsaw")
            self.player.set_item_charges("Chainsaw", chainsaw_charge + 2)
            self.drop_item("Gasoline")
        else:
            print("\nThese items cannot be used right now\n")
            return

    def choose_door(self, direction: d) -> bool:
        if direction in self.chosen_tile.doors:
            print("Choose a NEW door not an existing one")
            return False
        self.chosen_tile.doors.append(direction)
        self.current_zombies = 3
        print(f'\n{self.current_zombies} Zombies have appeared,'
              ' prepare for battle. '
              f'Use "fight"" or the "runaway" command to flee\n')
        self.set_state("Attacking")
        return True

    def search_for_totem(self) -> None:
        if self.get_current_tile().name == "Evil Temple":
            if self.player.has_totem:
                print("\nplayer already has the totem\n")
                return
            else:
                self.trigger_dev_card(self.time)
                self.player.found_totem()
        else:
            print("\nYou cannot search for a totem in this room\n")

    def bury_totem(self) -> None:
        if self.get_current_tile().name == "Graveyard":
            if self.player.has_totem:
                self.trigger_dev_card(self.time)
                if self.player.health != 0:
                    print("You Won")
                    self.set_state("Game Over")
        else:
            print("\nCannot bury totem here\n")

    def check_for_dead_player(self) -> bool:
        if self.player.health <= 0:
            return True
        else:
            return False

    @staticmethod
    def resolve_doors(n: int, e: int, s: int, w: int) -> list[int]:
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

    def lose_game(self) -> None:
        self.set_state("Game Over")


if __name__ == "__main__":
    doctest.testmod(extraglobs={'g': Game(Player())}, verbose=True)
