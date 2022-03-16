from Game import Game
from Tile import Tile
from Player import Player
import random


class SetUp():
    def __init__(self):
        self.dev_cards = []
        self.tiles = []

    def add_tile(self, exits_aval, is_inside, tile_desc, tile_name, tile_prop):
        """ adds tile to list """
        new_tile = Tile(exits_aval, is_inside, tile_desc, tile_name, tile_prop)
        self.tiles.append(new_tile)

    def insert_tile(self, index, tile):
        """ inserts the tile at any index """
        self.tiles.insert(index, tile)

    def gen_tile_list(self):
        """ creates the tiles for the game """
        # Outside tiles
        #self.add_tile(3, "Garden", "+1 Health if end turn here.", False)
        #self.add_tile(3, "Sitting Area", None, False)
        #self.add_tile(3, "Yard", None, False)
        #self.add_tile(3, "Yard", None, False)
        #self.add_tile(3, "Yard", None, False)
        #self.add_tile(2, "Graveyard",
        #              "Resolve a new card to bury totem", False)
        #self.add_tile(2, "Garage", None, False)

        # Inside tiles
        self.add_tile(1, True, None, "Bathroom", None)
        self.add_tile(3, True,
                      "+1 Health if end turn here.",
                      "Kitchen", "health increase")
        self.add_tile(1, True, 
                      "May draw a new card to find an item.", 
                      "Storage", "item")
        self.add_tile(2, True, 
                      "Resolve a new card to find totem",
                      "Evil Temple", "totem")
        self.add_tile(3, True, None,  "Family Room",  None)
        self.add_tile(4, True,  None, "Dinning Room", "exterior door")

        self.add_tile(2, True, None, "Bed Room", None)

        random.shuffle(self.tiles)

        # These tiles need to be at the start of each list
        start_tile = Tile(1, True,  None, "Foyer", None)
        start_tile.set_is_placed()
        self.insert_tile(0, start_tile)
        #enter_outside_tile = Tile(3, "Patio", None, False)
        #self.insert_tile(1, enter_outside_tile)
        # Generates the ids for the tiles so other tiles can refrance them
        self.gen_tile_index()

    def gen_tile_index(self):
        for i in range(len(self.tiles)):
            self.tiles[i].tile_num = i

    def get_tiles(self):
        """ gets the tile list """
        return self.tiles




if __name__ == "__main__":
    setup = SetUp()
    setup.gen_tile_list()

    player = Player("hello")
    

    game = Game(setup.get_tiles(), player)

    print(f'started in: {game.check_current_tile_name()}')
    

    game.draw_tile()
    print(game.check_current_tile_name())

    game.draw_tile()
    print(game.check_current_tile_name())

    game.runaway()
    print(f'ran away: {game.check_current_tile_name()}')

    game.draw_tile()
    print(f'new room: {game.check_current_tile_name()}')    
    
    game.draw_tile()
    print(game.check_current_tile_name())

    
