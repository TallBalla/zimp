class Game():
    def __init__(self, tiles, player):
        self.current_index = 0
        self.has_totem = False
        self.is_inside = True
        self.player = player
        self.tiles = tiles
        self.time = 9

    def check_is_inside(self):
        return self.is_inside

    def runaway(self):
        # TODO ask what room a player wants to run into
        self.player.runaway()

    def cower(self):
        # TODO discard devcard from the deak for the round
        self.player.cower()

    def exterior_door_handler(self):
        # TODO switch list to ouside 
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

    def draw_tile(self):
        current_tile = tile_list[self.current_index]

        new_tile = tile_list[self.current_index + 1]

        new_tile.prev_tile_num = current_tile.tile_num
        print(new_tile.tile_name, new_tile.prev_tile_num)

        self.tile_prop_handler(new_tile)
        self.current_index += 1

    def reshuffle(self):
        self.time += 1

