# Willems Implementation
import unittest
from game import Game
from player import Player
from tile import Tile
from directions import Direction as d

class GameTestMethods(unittest.TestCase):
    def setUp(self):
        self.game = Game(Player())
        self.player = self.game.get_player()

    def move_player_west(self):
        self.game.start_game_play()
        self.game.place_tile(16, 16)
        self.game.select_move(d.WEST)
        self.game.move_player(15, 16)

    def rotate_foyer(self, amount):
        self.game.start_game_play()
        for i in range(0, amount):
            self.game.rotate()

        self.game.place_tile(16, 16)

    def test_game_state_none(self):
        # Act
        actual_state = self.game.get_state()
        expected_state = None
        # Assert
        self.assertEqual(actual_state, expected_state)

    def test_game_state_starting(self):
        # Arrange
        self.game.start_game()
        # Act
        actual_state = self.game.get_state()
        expected_state = 'Starting'
        # Assert
        self.assertEqual(actual_state, expected_state)

    def test_game_state_rotating(self):
        # Arrange
        self.game.start_game_play()
        # Act
        actual_state = self.game.get_state()
        expected_state = 'Rotating'
        # Assert
        self.assertEqual(actual_state, expected_state)

    def test_game_state_moving(self):
        # Arrange
        self.game.start_game_play()
        self.game.place_tile(15, 15)
        # Act
        actual_state = self.game.get_state()
        expected_state = 'Moving'
        # Assert
        self.assertEqual(actual_state, expected_state)

    def test_game_state_dev_card(self):
        # Arrange
        self.game.start_game_play()
        self.game.move_player(16, 16)
        # Act
        actual_state = self.game.get_state()
        expected_state = 'Drawing Dev Card'
        # Assert
        self.assertEqual(actual_state, expected_state)

    def test_game_state_drawing_dev_card(self):
        # Arrange
        self.move_player_west()
        # Act
        actual_state = self.game.get_state()
        expected_state = 'Drawing Dev Card'
        # Assert
        self.assertEqual(expected_state, actual_state)

    def test_check_load_inside_tiles(self):
        # Arrange
        # Act
        is_outside_tile_none = self.game.check_outdoor_tiles_is_empty()
        # Assert
        self.assertTrue(is_outside_tile_none)

    def test_can_load_inside_tiles(self):
        # Arrange
        self.game.load_tiles()
        # Act
        is_outside_tile_none = self.game.check_outdoor_tiles_is_empty()
        # Assert
        self.assertFalse(is_outside_tile_none)

    def test_check_load_outside_tiles(self):
        # Arrange
        # Act
        is_inside_tile_none = self.game.check_indoor_tiles_is_empty()
        # Assert
        self.assertTrue(is_inside_tile_none)

    def test_can_load_outside_tiles(self):
        # Arrange
        self.game.load_tiles()
        # Act
        is_inside_tile_none = self.game.check_indoor_tiles_is_empty()
        # Assert
        self.assertFalse(is_inside_tile_none)

    def test_can_load_dev_cards(self):
        # Arrange
        self.game.load_dev_cards()
        # Act
        is_dev_cards_none = self.game.check_dev_cards_is_empty()
        # Assert
        self.assertFalse(is_dev_cards_none)

    def test_can_load_tiles(self):
        # Arrange
        self.game.start_game_play()
        self.game.place_tile(16, 16)
        # Act
        is_game_map_none = self.game.check_tiles_is_empty()
        # Assert
        self.assertFalse(is_game_map_none)

    def test_first_tile_foyer(self):
        # Arrange
        self.game.start_game_play()
        self.game.place_tile(16, 16)
        current_tile = self.game.get_current_tile()
        # Act
        actual_tile_name = current_tile.name
        expected_tile_name = 'Foyer'
        # Assert
        self.assertEqual(actual_tile_name, expected_tile_name)

    def test_south_not_in_chosen_tile_door(self):
        # Arrange
        self.game.start_game_play()
        # Act
        is_south_in_tile_door = self.game.check_direct_south_not_in_doors()
        # Assert
        self.assertTrue(is_south_in_tile_door)

    def test_north_not_in_chosen_tile_door(self):
        # Arrange
        self.game.start_game_play()
        # Act
        is_north_in_tile_door = self.game.check_direct_north_not_in_doors()
        # Assert
        self.assertTrue(is_north_in_tile_door)

    def test_east_not_in_chosen_tile_door(self):
        # Arrange
        self.game.start_game_play()
        # Act
        is_east_in_tile_door = self.game.check_direct_east_not_in_doors()
        # Assert
        self.assertTrue(is_east_in_tile_door)

    def test_west_not_in_chosen_tile_door(self):
        # Arrange
        self.game.start_game_play()
        # Act
        is_west_in_tile_door = self.game.check_direct_west_not_in_doors()
        # Assert
        self.assertFalse(is_west_in_tile_door)


if __name__ == '__main__':
    unittest.main(verbosity=2)
