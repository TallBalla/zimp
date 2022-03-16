class Game():
    def __init__(self, tiles, player):
        self.current_index = 0
        self.has_totem = False
        self.is_inside = True
        self.player = player
        self.tiles = tiles
        self.time = 9


    def check_is_inside(self):
        """Checks if the user is inside or outside"""
        return self.is_inside

    def check_current_tile_name(self):
        """Returns the tile name of the tile"""
        return self.tiles[self.current_index].tile_name

    def exterior_door_handler(self):
        # TODO switch list to ouside list
        self.is_inside = not self.is_inside

    def health_increase_handler(self):
        """Increases the players health by 1"""
        self.player.add_health(1)

    # TODO add item to player
    # Check if player wants to keep item or drop item 
    def item_handler(self):
        print("!!! item_handler")

    def totem_handler(self):
        if self.has_totem:
            return
        # TODO draw devcard to get totem
        self.has_totem = True

    # TODO add functionality
    # Checks if the player has the totem
    # If the player doesnt have totem it throws error
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

    def find_prev_tile(self, tile_num):
        """Gets the tile the player has just come from"""
        return filter(lambda tile: tile.tile_num == tile_num, self.tiles)

    def find_next_aval_tile(self):
        """Finds the next tile that hasnt been played on the board"""
        return filter(lambda tile: tile.get_is_placed() == False, self.tiles)

    def runaway(self):
        """Player can only run into the previous room when running away"""

        # TODO check if there are zombies in the room
        # Can only run away when there are zombies in the room
        self.player.runaway()
                
        tile = self.tiles[self.current_index]
        prev_tile_num = tile.prev_tile_num
        new_tile = next(self.find_prev_tile(prev_tile_num))
        self.current_index = self.tiles.index(new_tile)

    def cower(self):
        """Allows a player to gain health"""
        # TODO discard devcard from the deak for 
        self.player.cower()

 

    def complete_game(self):
        """Performs a sequence of actions when the player completes the game"""
        print("you have won")

    def move_handler(self):
        """Performs a sequence of actions when a player wants to move around the game"""
        current_tile = self.tiles[self.current_index]
        # TODO add and there are avalible tiles in list
        if current_tile.exits != 0:
            # TODO draw tile
            return

        # TODO add and there are avalible tiles in list
        elif current_tile.exits == 0:
            # TODO work out how to handle 
            return

        # TODO add and there are no avalible tiles in list


    def draw_dev_card(self):
        """Draws the next avalible dev card in the pile"""
        print("dev card drawn")

    def draw_tile(self):
        """Draws the next avalible tile in the list"""
        current_tile = self.tiles[self.current_index]
        current_tile_num = current_tile.tile_num

        next_tile = next(self.find_next_aval_tile())
        next_tile_index = self.tiles.index(next_tile)
        self.current_index = next_tile_index

        new_tile = self.tiles[self.current_index]
        new_tile.prev_tile_num = current_tile_num
        new_tile.set_is_placed()

    def reshuffle(self):
        self.time += 1
