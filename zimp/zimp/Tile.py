class Tile():
    def __init__(self, exits_aval, is_inside, tile_desc, tile_name, tile_prop):
        self._exits_aval = exits_aval
        self._prev_tile_num = 0
        self._tile_num = 0
        self.is_inside = is_inside
        self.is_placed = False
        self.tile_desc = tile_desc
        self.tile_name = tile_name
        self.tile_prop = tile_prop

    # Number of exits
    @property
    def exits(self):
        return self._exits_aval

    @exits.setter
    def exits(self, new_exit_num):
        self.exits = new_exit_num

    # Tile number or id,
    # it helps ditermine what the tile.
    @property
    def tile_num(self):
        return self._tile_num

    @tile_num.setter
    def tile_num(self, new_tile_num):
        self._tile_num = int(new_tile_num)

    # Tile previous number of the tile
    # (the tile its linked to).
    @property
    def prev_tile_num(self):
        return self._prev_tile_num

    @prev_tile_num.setter
    def prev_tile_num(self, new_prev_tile_num):
        self._prev_tile_num = new_prev_tile_num

    # Is placeds methods, couldnt use a property
    # because though it was pointless to pass in true.
    def get_is_placed(self):
        return self.is_placed

    def set_is_placed(self):
        self.is_placed = True

    # Gets tile location in terms of the game.
    def get_is_inside(self):
        return self.is_inside

    def get_tile_prop(self):
        return self.tile_prop