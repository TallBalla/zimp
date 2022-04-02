import unittest
from Game import Game
from Player import Player
from directions import Direction as d

class GameTestMethods(unittest.TestCase):
    def setUp(self):
        self.game = Game(Player())

    def move_player_west(self):
        self.game.start_game_play()
        self.game.place_tile(16, 16)
        self.game.select_move(d.WEST)
        self.game.move_player(15,16)

    def rotate_foyer(self):
        self.game.start_game_play()
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
        self.game.place_tile(15,15)
        # Act 
        actual_state = self.game.get_state()
        expected_state = 'Moving'
        # Assert
        self.assertEqual(actual_state, expected_state)

    def test_game_state_dev_card(self):
        # Arrange
        self.game.start_game_play()
        self.game.move_player(16,16)
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

    def test_foyer_not_west_after_rotate(self):
        # Arrange
        self.rotate_foyer()
        current_tile = self.game.get_current_tile()
        # Act 
        has_tile_rotated = self.game.check_tile_rotated(d.WEST)
        # Assert
        self.assertFalse(has_tile_rotated)

    def test_foyer_north_after_rotate(self):
        # Arrange
        self.rotate_foyer()
        current_tile = self.game.get_current_tile()
        # Act 
        has_tile_rotated = self.game.check_tile_rotated(d.NORTH)
        # Assert
        self.assertTrue(has_tile_rotated)

if __name__ == '__main__':
    unittest.main(verbosity=2)
