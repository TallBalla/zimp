class Tile():
    """
        Places where a player can move
    """
    def __init__(
            self,
            num_exits,
            tile_name=None,
            tile_descript=None,
            tile_property=None):
        self.been_placed = False
        self.connected_tiles = []
        self.num_exits = num_exits
        self.tile_name = title_name
        self.tile_property = tile_property

    def get_been_placed(self):
        return self.been_placed

    def set_been_placed(self):
        return self.been_placed = True
