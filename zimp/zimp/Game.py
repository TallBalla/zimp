#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import partial, partialmethod
from View import View
import random

class Game:
    current_index = 0
    dev_card_index = 1
    has_totem = False
    is_inside = True
    time = 9
    view = View()

    def __init__(self, player, tiles, dev_cards):
        self.player = player
        self.dev_cards = dev_cards
        self.tiles = tiles

    def get_current_tile_name(self):
        """Returns the tile name of the tile"""

        return self.tiles[self.current_index].tile_name

    def get_total_exit(self):
        return sum(tile.exits for tile in self.tiles
                   if tile.get_is_placed())

    def check_is_inside(self):
        """Checks if the user is inside or outside"""

        return self.is_inside

    def check_aval_tile_count(self):
        """Checks if there are avalible tiles to be placed"""

        return sum(not tile.get_is_placed() for tile in self.tiles) != 0

    def check_total_exits(self):
        """Checks if there are exits new tiles can be placed to"""

        return self.get_total_exit() == 0

    def exterior_door_handler(self):

        # TODO switch list to ouside list

        self.is_inside = not self.is_inside

    # FIX ME
    def health_increase_handler(self):
        """Increases the players health by 1"""
        print("health_increase_handler")
        health = 1
        self.player.add_health(health)

    # TODO add break through method
    def zombie_door(self):
        self.view.zombie_door_warning()
        self.zombie_attack(3, True)
        self.draw_tile_handler()
        self.draw_dev_card(False)


    def item_handler(self):
        """Draws a devcard and see if player wants the time"""

        self.view.draw_devcard_warning()
        if self.view.check_draw_devcard():
            # TODO draw dev card
            # Item will be from devcard
            print("item handler drew dev card")
            self.dev_card_index += 1
            
            dev_card = self.dev_cards[self.dev_card_index]
            item = dev_card.get_card_item()

            if self.view.check_add_item('Item One', item.get_item_name()):

                if not self.player.check_item_one_none():
                    if not self.view.check_replace_item(self.player.item_one.get_item_name(),
                            item):
                        return
                self.player.item_one = item
                return
            elif self.view.check_add_item('Item Two', item.get_item_name()):

                if not self.player.check_item_two_none():
                    if not self.view.check_replace_item(self.player.item_two.get_item_name(),
                            item):
                        return
                self.player.item_two = item
                return

    def totem_handler(self):
        if self.has_totem:
            return

        # TODO check if player wants to collect totem
        # if yes the player will draw a dev card but not collect the items

        self.has_totem = True

    def totem_bural_handler(self):
        if self.has_totem:
            self.complete_game()
            return

        self.view.no_totem_warning()
        # TODO print player doesnt have the totem

    def tile_prop_handler(self, tile):
        """ handles all the checks for the tile properties
        to see if they have any special characterics """

        if tile.get_tile_prop() is None:
            return

        props = {
            'exterior door': self.exterior_door_handler,
            'health increase': self.health_increase_handler,
            'item': self.item_handler,
            'totem': self.totem_handler,
            'totem bural': self.totem_bural_handler,
            }
        props.get(tile.get_tile_prop(), None)()
    
    def zombie_attack(self, zombies, zombie_door):

        player_attack = self.player.get_player_attack()
        damage = player_attack  - zombies
        if zombie_door:
            if damage < 0:
                self.player.remove_health(abs(damage))
            return

        if self.view.check_player_runaway(damage, zombies):
            self.runaway()
            return

        if damage < 0:
            self.player.remove_health(abs(damage))


    def event_prop_handler(self, dev_card):

        event = dev_card.get_card_event(self.time)
        
        if event.get_event_prop() is None:
            return

        props = {
            'zombie 3': partial(self.zombie_attack, 3, False),
            'zombie 4': partial(self.zombie_attack, 4, False),
            'zombie 5': partial(self.zombie_attack, 5, False),
            'zombie 6': partial(self.zombie_attack, 6, False),
            'add health': self.health_increase_handler,
            'remove health': partial(self.player.remove_health, 1),
            'item': self.item_handler, 
            }
        props.get(event.get_event_prop(), None)()

    def find_prev_tile(self, tile_num):
        """Gets the tile the player has just come from"""

        return next(filter(lambda tile: tile.tile_num == tile_num,
                    self.tiles))

    def find_next_aval_tile(self):
        """Finds the next tile that hasnt been played on the board"""

        return next(filter(lambda tile: not tile.get_is_placed(),
                    self.tiles))

    def runaway(self):
        """Player can only run into the previous room when running away"""


        tile = self.tiles[self.current_index]
        prev_tile_num = tile.prev_tile_num
        new_tile = self.find_prev_tile(prev_tile_num)
        self.current_index = self.tiles.index(new_tile)

        self.player.runaway()

    def cower(self):
        """Allows a player to gain health"""
        self.dev_card_index += 1
        self.player.cower()

    def complete_game(self):
        """Performs a sequence of actions when the player completes the game"""

        print('you have won')

    def move_handler(self):
        """Performs a sequence of actions when a player wants to move around the game"""
        current_tile = self.tiles[self.current_index]
        print(f"\nCurrent Tile : {current_tile.get_tile_name()}")
        print(f"Player Health: {self.player.get_player_health()}")
        print(f"Player Attack: {self.player.get_player_attack()}")


        if current_tile.exits != 0 and self.check_aval_tile_count():
            self.draw_tile_handler()
            self.draw_dev_card(False)
            return
        elif self.check_total_exits() \
            and self.check_aval_tile_count():
            self.zombie_door()
            return

        # TODO add and there are no avalible tiles in list

    def draw_dev_card(self, get_item):
        """Draws the next avalible dev card in the pile"""

        self.dev_card_index += 1
        dev_card = self.dev_cards[self.dev_card_index]

        if self.dev_card_index == len(self.dev_cards):
            self.view.shuffle_dev_card_warning()
            self.reshuffle()

        if get_item:
           self.item_handler()
           return

        self.event_prop_handler(dev_card)


    def draw_tile_handler(self):
        """Preforms a sequence of actions when the player want to draw a new tile"""

        current_tile = self.tiles[self.current_index]
        current_tile_num = current_tile.tile_num
        current_tile.exits -= 1

        next_tile = self.find_next_aval_tile()
        next_tile_index = self.tiles.index(next_tile)
        self.current_index = next_tile_index

        new_tile = self.tiles[self.current_index]
        new_tile.prev_tile_num = current_tile_num
        new_tile.set_is_placed()
        new_tile.exits -= 1

        self.tile_prop_handler(new_tile)

    def reshuffle(self):
        self.time += 1
        self.dev_card_index = 1
        random.shuffle(self.dev_cards)

