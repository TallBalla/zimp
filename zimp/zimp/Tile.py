from directions import Direction as d


class Tile:
    def __init__(self,
                 name: str,
                 x=16,
                 y=16,
                 effect=None,
                 doors=None,
                 entrance=None):
        if doors is None:
            doors = []
        self.name = name
        self.x = x
        self.y = y
        self.effect = effect
        self.doors = doors
        self.entrance = entrance

    def set_x(self, x: int) -> None:
        self.x = x

    def set_y(self, y: int) -> None:
        self.y = y

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_entrance(self) -> str:
        return self.entrance

    def get_name(self) -> str:
        return self.name

    def change_door_position(self, idx: int, direction: d) -> None:
        self.doors[idx] = direction

    def set_entrance(self, direction: d) -> None:
        self.entrance = direction

    def rotate_entrance(self) -> None:
        if self.entrance == d.NORTH:
            self.set_entrance(d.EAST)
            return
        if self.entrance == d.SOUTH:
            self.set_entrance(d.WEST)
            return
        if self.entrance == d.EAST:
            self.set_entrance(d.SOUTH)
            return
        if self.entrance == d.WEST:
            self.set_entrance(d.NORTH)
            return

    def rotate_tile(self) -> None:
        for door in self.doors:
            if door == d.NORTH:
                self.change_door_position(self.doors.index(door), d.EAST)
            if door == d.EAST:
                self.change_door_position(self.doors.index(door), d.SOUTH)
            if door == d.SOUTH:
                self.change_door_position(self.doors.index(door), d.WEST)
            if door == d.WEST:
                self.change_door_position(self.doors.index(door), d.NORTH)
