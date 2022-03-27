class Tile():
    def __init__(self, exits_aval, tile_name, tile_desc, tile_prop):
        self._exits_aval = exits_aval
        self._prev_tile_num = 99
        self._tile_num = 0
        self.is_placed = False
        self.tile_name = tile_name
        self.tile_desc = tile_desc
        self.tile_prop = tile_prop



    # Number of exits
    @property
    def exits(self):
        """Gets the amount of exits avalible"""
        return self._exits_aval

    @exits.setter
    def exits(self, new_exit_num):
        """Sets the number of exits avalible"""
        self._exits_aval = new_exit_num

    # Tile number or id,
    # it helps ditermine what the tile.
    @property
    def tile_num(self):
        """Gets the tile number"""
        return self._tile_num

    @tile_num.setter
    def tile_num(self, new_tile_num):
        """Sets the tile number"""
        self._tile_num = int(new_tile_num)

    # Tile previous number of the tile
    # (the tile its linked to).
    @property
    def prev_tile_num(self):
        """Gets the number of the tile that the current tile is linked to"""
        return self._prev_tile_num

    @prev_tile_num.setter
    def prev_tile_num(self, new_prev_tile_num):
        """Sets the number of the tile that the current tile is linked to"""
        self._prev_tile_num = new_prev_tile_num
    
    def set_is_placed(self):
        """Sets a tile to display it has been placed"""
        self.is_placed = True

    # Is placeds methods, couldnt use a property
    # because though it was pointless to pass in true.
    def get_is_placed(self):
        """Gets information about a tile being placed"""
        return self.is_placed

    def get_tile_description(self):
        return self.tile_desc

    def get_tile_name(self):
        """Gets the name of the tile"""
        return self.tile_name

    def get_tile_prop(self):
        """Gets the tile properties so actions can be performed when tile placed"""
        return self.tile_prop

    def check_avail_exits(self):
        return self.exits <= 0
