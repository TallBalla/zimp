class Game():
    def __init__(self, tiles, player):
        self.current_index = 0
        self.has_totem = False
        self.is_inside = True
        self.player = player
        self.tiles = tiles
        self.time = 9

    def get_current_tile_name(self):
        return f'''{self.tiles[self.current_index].tile_name}
                    current tile num {self.tiles[self.current_index].tile_num}
                    previous tile num {self.tiles[self.current_index].prev_tile_num}
                '''

    def check_is_inside(self):
        return self.is_inside

    def find_prev_tile(self, tile_num):
        return filter(lambda tile: tile.tile_num == tile_num, self.tiles)

    def runaway(self):
        """Player can only run into the previous room when running away"""

        # TODO check if there are zombies in the room
        self.player.runaway()
                
        tile = self.tiles[self.current_index]
        prev_tile_num = tile.prev_tile_num
        new_tile = next(self.find_prev_tile(prev_tile_num))
        self.current_index = self.tiles.index(new_tile)

    def cower(self):
        # TODO discard devcard from the deak for 
        self.player.cower()

    def exterior_door_handler(self):
        # TODO switch list to ouside list
        self.is_inside = not self.is_inside

    def health_increase_handler(self):
        self.player.add_health(1)

    def item_handler(self):
        print("!!! item_handler")

    def totem_handler(self):
        if self.has_totem:
            return
        # TODO draw devcard to get totem
        self.has_totem = True

    def totem_bural_handler(self):
        print("!!! totem_bural_handler")

    def tile_prop_handler(self, tile):
        """ handles all the checks for the tile properties
        to see if they have any special characterics """
        props = {
            "exterior door": self.exterior_door_handler,
            "health increase": self.health_increase_handler,
            "item": self.item_handler,
            "totem": self.totem_handler,
            "totem bural": self.totem_bural_handler
            }
        props.get(tile.get_tile_prop(), None)()

    def complete_game(self):
        print("you have won")

    def draw_dev_card(self):
        print("dev card drawn")

    # FIXME not getting tile correctly
    # TODO get the last index of placed tile
    def draw_tile(self):
        current_tile = self.tiles[self.current_index]
        current_tile_num = current_tile.tile_num
        self.current_index += 1

        new_tile = self.tiles[self.current_index]
        new_tile.prev_tile_num = current_tile_num
        new_tile.set_is_placed()


    def reshuffle(self):
        self.time += 1
