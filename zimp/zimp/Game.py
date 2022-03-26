#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import partial
import random


class Game:
    current_index = 0
    dev_card_index = 1
    has_totem = False
    is_inside = True
    is_totem_buried = False
    saved_inside_index = 0
    saved_outside_index = 0
    time = 9

    def __init__(self, player, dev_cards, inside_tiles, outside_tile):
        self.player = player
        self.dev_cards = dev_cards
        self.inside_tiles = inside_tiles
        self.outside_tiles = outside_tile
        self.tiles = inside_tiles

    # ----------------- !!!! Checkers !!!! -----------------

    def check_aval_tile_count(self):
        return sum(not tile.get_is_placed() for tile in self.tiles) != 0

    def check_is_inside(self):
        return self.is_inside

    def check_current_room_evil_temple(self):
        return self.get_current_tile_name == 'totem'

    def check_total_exits(self):
        return self.get_total_exit() == 0

    def check_avail_dev_cards(self):
        return self.dev_card_index == len(self.dev_cards)

    def check_event_prop_is_not_none(self, event):
        return event.get_event_prop() is not None

    def check_tile_prop_is_not_none(self, tile):
        return tile.get_tile_prop() is not None

    def check_for_zombie_door(self):
        return (self.check_total_exits() and
                self.check_aval_tile_count())

    def check_player_has_totem(self):
        return self.has_totem

    def check_player_has_buried_totem(self):
        return self.is_totem_buried

    def check_player_holds_attack_item(self):
        items_props = map(lambda item: item.get_item_prop(),
                          self.player.get_items())

        return any('attack' in item_prop for item_prop in items_props)

    def check_player_holds_health_item(self):
        items_props = map(lambda item: item.get_item_prop(),
                          self.player.get_items())
        return 'health' in items_props    

    def check_player_holds_special_item(self):
        items_props = map(lambda item: item.get_item_prop(),
                          self.player.get_items())
        return 'special' in items_props    
    
    def check_item_one_uses(self):
        item_one = self.player.item_one
        return self.player.check_item_uses(item_one)

    def check_item_two_uses(self):
        item_two = self.player.item_two
        return self.player.check_item_uses(item_two)

    # ----------------- !!!! Setters !!!! -----------------

    def set_player(self, player):
        self.player = player

    def set_location(self):
        self.is_inside = not self.is_inside

    def set_tiles_inside(self):
        self.outside_tiles = self.tiles
        self.tiles = self.inside_tiles
        self.current_index = self.saved_inside_index

    def set_tiles_outside(self):
        self.inside_tiles = self.tiles
        self.tiles = self.outside_tiles
        self.current_index = self.saved_outside_index

    # ----------------- !!!! Getters/Finders !!!! -----------------

    def get_prev_tile(self, tile_num):
        """Gets the tile the player has just come from"""

        return next(filter(lambda tile: tile.tile_num == tile_num,
                    self.tiles))

    def get_next_avail_tile(self):
        """Finds the next tile that hasnt been played on the board"""

        return next(filter(lambda tile: not tile.get_is_placed(),
                           self.tiles))

    def get_current_tile(self):
        return self.tiles[self.current_index]

    #def get_connected_tiles(self):
    #    current_tile = self.get_current_tile()
    #    return filter(lambda tile: 
    #                  current_tile.prev_tile_num == tile.tile_num,
    #                  self.tiles)

    def get_event(self, dev_card):
        return dev_card.get_card_event(self.time)

    def get_player(self):
        return self.player

    def get_remaining_dev_cards(self):
        return (len(self.dev_cards) - self.dev_card_index)

    def get_time(self):
        return self.time

    def get_total_exit(self):
        return sum(tile.exits for tile in self.tiles
                   if tile.get_is_placed())

    def get_tiles(self):
        return self.tiles
    # ----------------- !!!! PLayer Actions !!!! -----------------

    def complete_game(self):
        """Performs a sequence of actions when the player completes the game"""

    def cower(self):
        """Allows a player to gain health"""
        self.dev_card_index += 1
        self.player.cower()

    def draw_dev_card(self):
        return self.dev_cards[self.dev_card_index]

    def increment_dev_card_index(self):
        self.dev_card_index += 1

    def reshuffle(self):
        self.time += 1
        self.dev_card_index = 1
        random.shuffle(self.dev_cards)
        return self.time

    def runaway(self):
        """Player can only run into the previous room when running away"""

        tile = self.tiles[self.current_index]
        prev_tile_num = tile.prev_tile_num
        new_tile = self.get_prev_tile(prev_tile_num)
        self.current_index = self.tiles.index(new_tile)
        self.player.runaway()
        
    def use_item_one(self):
        self.player.remove_item_one_use()

    def use_item_two(self):
        self.player.remove_item_two_use()

    # ----------------- !!!! Handlers !!!! -----------------

    def draw_tile(self):
        """Preforms a sequence of actions when the
        player want to draw a new tile"""
        current_tile = self.tiles[self.current_index]
        current_tile_num = current_tile.tile_num
        current_tile.exits -= 1

        # Finds the next avalible tile and sets tile to it
        next_tile = self.get_next_avail_tile()
        next_tile_index = self.tiles.index(next_tile)
        self.current_index = next_tile_index

        new_tile = self.tiles[self.current_index]
        new_tile.prev_tile_num = current_tile_num
        new_tile.set_is_placed()
        new_tile.exits -= 1
        return new_tile

    def add_health(self, health):
        self.player.add_health(health)

    def collect_item(self):
        """Draws a devcard and see if player wants the time"""

        dev_card = self.dev_cards[self.dev_card_index]
        item = dev_card.get_card_item()
        return item

    def bury_totem(self):
        self.is_totem_buried = True
        # TODO print player doesnt have the totem

    def collect_totem(self):
        if self.has_totem:
            return
        self.has_totem = True

    def zombie_attack_handler(self, zombies, zombie_door):

        player_attack = self.player.get_player_attack()
        damage = player_attack - zombies
        if zombie_door or self.check_current_room_evil_temple():
            if damage < 0:
                self.player.remove_health(abs(damage))
            return zombies

        if self.view.check_player_runaway(damage, zombies):
            self.runaway()
            return

    def remove_health(self, health):
        self.player.remove_health(health)