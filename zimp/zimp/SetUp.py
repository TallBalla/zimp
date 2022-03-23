#!/usr/bin/python
# -*- coding: utf-8 -*-
from DevCard import DevCard
from Event import Event
from Game import Game
from Item import Item
from Player import Player
from Tile import Tile
import random


class SetUp:

    dev_cards = []
    inside_tiles = []
    outside_tiles = []

    def add_inside_tile(
        self,
        exits_aval,
        tile_desc,
        tile_name,
        tile_prop,
        ):
        """Adds tile to list """

        new_tile = Tile(exits_aval, tile_desc, tile_name, tile_prop)
        self.inside_tiles.append(new_tile)

    def add_outside_tile(
        self,
        exits_aval,
        tile_desc,
        tile_name,
        tile_prop,
        ):
        """Adds tile to list """

        new_tile = Tile(exits_aval, tile_desc, tile_name, tile_prop)
        self.outside_tiles.append(new_tile)

    def add_dev_card(
        self,
        item,
        event_one,
        event_two,
        event_three,
        ):
        """Adds dev card to list"""

        new_dev_card = DevCard(item, event_one, event_two, event_three)
        self.dev_cards.append(new_dev_card)

    def insert_inside_tile(self, index, tile):
        """ inserts the tile at any index """

        self.inside_tiles.insert(index, tile)

    def insert_outside_tile(self, index, tile):
        """ inserts the tile at any index """

        self.outside_tiles.insert(index, tile)

    def gen_outside_tiles(self):

        self.add_outside_tile(3, '+1 Health if end turn here.', 'Garden', 'health increase')
        self.add_outside_tile(3, None, 'Sitting Area', None)
        self.add_outside_tile(3, None, 'Yard', None)
        self.add_outside_tile(3, None, 'Yard', None)
        self.add_outside_tile(3, None, 'Yard', None)
        self.add_outside_tile(2, 'Resolve a new card to bury totem',
                              'Graveyard', 'totem bural')
        self.add_outside_tile(2, None, 'Garage', None)

        random.shuffle(self.outside_tiles)


        enter_outside_tile = Tile(3, None, 'Patio', 'exterior door')
        enter_outside_tile.set_is_placed()
        self.insert_outside_tile(0, enter_outside_tile)
        
        
        for i in self.outside_tiles:
            print(i.get_tile_name())


        # Generates the ids for the tiles so other tiles can refrance them

    def gen_inside_tiles(self):
        """ creates the tiles for the game """

        self.add_inside_tile(1, None, 'Bathroom', None)
        self.add_inside_tile(3, '+1 Health if end turn here.', 'Kitchen'
                             , 'health increase')
        self.add_inside_tile(1, 'May draw a new card to find an item.',
                             'Storage', 'item')
        self.add_inside_tile(2, 'Resolve a new card to find totem',
                             'Evil Temple', 'totem')
        self.add_inside_tile(3, None, 'Family Room', None)
        self.add_inside_tile(4, None, 'Dinning Room', 'exterior door')

        self.add_inside_tile(2, None, 'Bed Room', None)

        random.shuffle(self.inside_tiles)

        start_tile = Tile(1, None, 'Foyer', None)
        start_tile.set_is_placed()
        self.insert_inside_tile(0, start_tile)

    def gen_dev_cards(self):
        self.add_dev_card(Item(True, 'Oil', 'combination', 1),
                          Event(None, 'You try hard not to wet yourself'
                          ), Event('item', 'ITEM'), Event('zombie 6',
                          '6 Zombies'))

        self.add_dev_card(Item(True, 'Gasoline', 'combination', 1),
                          Event('zombie 4', '4 Zombies'),
                          Event('remove health',
                          'You sense your impending doom -1 HEALTH'),
                          Event('item', 'ITEM'))

        self.add_dev_card(Item(False, 'Board with Nails', 'add attack 1'
                          , 100), Event('item', 'ITEM'),
                          Event('zombie 4', '4 Zombies'),
                          Event('remove health',
                          'Something icky in your mouth -1 HEALTH'))

        self.add_dev_card(Item(False, 'Machete', 'add attack 2', 100),
                          Event('zombie 4', '4 Zombies'),
                          Event('remove health',
                          'A bat poops in your eye -1 HEALTH'),
                          Event('zombie 6', '6 Zombies'))

        self.add_dev_card(Item(False, 'Grisly Femur', 'add attack 1',
                          100), Event('item', 'ITEM'), Event('zombie 5'
                          , '5 Zombies'), Event('remove health',
                          'Your soul isnt wanted here -1 HEALTH'))

        self.add_dev_card(Item(False, 'Goal Club', 'add attack 1',
                          100), Event('remove health',
                          'Slip on nasty goo -1 HEALTH'),
                          Event('zombie 4', '4 Zombies'), Event(None,
                          'The smell of blood is in The air'))

        self.add_dev_card(Item(True, 'Chainsaw', 'combination', 2),
                          Event('zombie 3', '3 Zombies'), Event(None,
                          'You hear terrible screams'), Event('zombie 5'
                          , '5 Zombies'))

        self.add_dev_card(Item(False, 'Can of Soda', 'add health', 1),
                          Event('add health',
                          'Candybar in you pocket +1 HEALTH'),
                          Event('item', 'ITEM'), Event('zombie 4',
                          '4 Zombies'))

        self.add_dev_card(Item(True, 'Candle', 'combination', 1),
                          Event(None, 'Your body shivers involuntarily'
                          ), Event('add health',
                          'You feel a spark of hope +1 HEALTH'),
                          Event('zombie 4', '4 Zombies'))
        
        random.shuffle(self.dev_cards)

    def gen_tile_index(self):
        for i in range(len(self.inside_tiles)):
            self.inside_tiles[i].tile_num = i
            self.outside_tiles[i].tile_num = i

    def get_dev_cards(self):
        """Gets the dev card list"""

        return self.dev_cards

    def get_inside_tiles(self):
        """Gets the tile list """

        return self.inside_tiles

    def get_outside_tiles(self):
        return self.outside_tiles


if __name__ == '__main__':
    setup = SetUp()
    setup.gen_inside_tiles()
    setup.gen_outside_tiles()
    setup.gen_dev_cards()

    setup.gen_tile_index()

    player = Player('hello')

    game = Game(player , setup.get_dev_cards(), setup.get_inside_tiles(), setup.get_outside_tiles())

    game.draw_tile_handler()

    game.draw_tile_handler()

    game.cower()

    game.draw_tile_handler()

    game.draw_tile_handler()

