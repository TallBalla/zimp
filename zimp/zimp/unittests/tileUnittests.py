import unittest
from Game import Game
from player import Player
from Tile import Tile
from directions import Direction as d


class TileTestMethods(unittest.TestCase):
    def setUp(self):
        self.tile = Tile('Tester', 16, 16, None, None, None)        
    
    def test_tile_can_get_name(self):
        # Act
        actual_tile_name = self.tile.get_name()
        expected_tile_name = 'Tester'
        # Assert
        self.assertEqual(actual_tile_name, expected_tile_name)

    def test_tile_can_get_x_position(self):
        # Act
        actual_x_position = self.tile.get_x()
        expected_x_position = 16
        # Assert 
        self.assertEqual(actual_x_position, expected_x_position)

    def test_tile_can_set_x_position(self):
        # Arrange
        self.tile.set_x(17)
        # Act
        actual_x_position = self.tile.get_x()
        expected_x_position = 17
        # Assert 
        self.assertEqual(actual_x_position, expected_x_position)

    def test_tile_can_get_y_position(self):
        # Act
        actual_y_position = self.tile.get_y()
        expected_y_position = 16
        # Assert
        self.assertEqual(actual_y_position, expected_y_position)
        
    def test_tile_can_set_y_position(self):
        # Arrange
        self.tile.set_y(17)
        # Act
        actual_y_position = self.tile.get_y()
        expected_y_position = 17
        # Assert
        self.assertEqual(actual_y_position, expected_y_position)
        
    def test_tile_entrance_is_none(self):
        # Act
        actual_entrance = self.tile.get_entrance()
        expected_entrance = None
        # Assert
        self.assertEqual(actual_entrance, expected_entrance)

    def test_tile_entrance_is_west_after_being_set(self):
        # Arrange
        self.tile.set_entrance(d.WEST)
        # Act
        actual_entrance = self.tile.get_entrance()
        expected_entrance = d.WEST
        # Assert
        self.assertEqual(actual_entrance, expected_entrance)
        
    def test_tile_entrance_is_north_after_being_rotated(self):
        # Arrange
        self.tile.set_entrance(d.WEST)
        self.tile.rotate_entrance()
        # Act
        actual_entrance = self.tile.get_entrance()
        expected_entrance = d.NORTH
        # Assert
        self.assertEqual(actual_entrance, expected_entrance)

if __name__ == '__main__':
    unittest.main(verbosity=2)