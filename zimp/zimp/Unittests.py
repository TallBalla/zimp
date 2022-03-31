import unittest
from Game import Game
from Player import Player

class GameTestMethods(unittest.TestCase):
    def setUp(self):
        self.game = Game(Player())

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

    def test_outside_tile_is_none(self):
        # Arrange
        # Act 
        is_outside_tile_none = self.game.check_outdoor_tiles_is_empty()
        # Assert
        self.assertTrue(is_outside_tile_none)

    def test_outside_tile_is_pop(self):
        # Arrange
        self.game.load_tiles()
        # Act 
        is_outside_tile_none = self.game.check_outdoor_tiles_is_empty()
        # Assert
        self.assertFalse(is_outside_tile_none)
        
    def test_inside_tile_is_none(self):
        # Arrange
        # Act 
        is_inside_tile_none = self.game.check_indoor_tiles_is_empty()
        # Assert
        self.assertTrue(is_inside_tile_none)

    def test_inside_tile_is_pop(self):
        # Arrange
        self.game.load_tiles()
        # Act 
        is_inside_tile_none = self.game.check_indoor_tiles_is_empty()
        # Assert
        self.assertFalse(is_inside_tile_none)

if __name__ == '__main__':
    unittest.main(verbosity=2)
