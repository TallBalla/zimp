import unittest
from game import Game
from player import Player
from tile import Tile
from directions import Direction as d


class PlayerTestMethods(unittest.TestCase):
    def setUp(self):
        self.game = Game(Player())
        self.player = self.game.get_player()

    def test_player_health_is_six(self):
        # Act
        actual_health = self.player.get_health()
        expected_health = 6
        # Assert
        self.assertEqual(actual_health, expected_health)

    def test_player_health_decrements(self):
        # Arrange
        self.player.remove_health(int(1))
        # Act
        actual_health = self.player.get_health()
        expected_health = 5
        # Assert
        self.assertEqual(actual_health, expected_health)

    def test_player_health_increments(self):
        # Arrange
        self.player.add_health(int(1))
        # Act
        actual_health = self.player.get_health()
        expected_health = 7
        # Assert
        self.assertEqual(actual_health, expected_health)

    def text_player_attack_is_one(self):
        # Act
        actual_attack = self.player.get_attack()
        expected_attack = 1
        # Assert
        self.assertEqual(actual_attack, expected_attack)

    def test_player_attack_increments(self):
        # Arrange
        self.player.add_attack(int(1))
        # Act
        actual_attack = self.player.get_attack()
        expected_attack = 2
        # Assert
        self.assertEqual(actual_attack, expected_attack)

    def test_player_attack_decrements(self):
        # Arrange
        self.player.remove_attack(int(1))
        # Act
        actual_attack = self.player.get_attack()
        expected_attack = 0
        # Assert
        self.assertEqual(actual_attack, expected_attack)

    def test_player_x_position_is_sixteen(self):
        # Act
        actual_x_position = self.player.get_x()
        expected_x_position = 16
        # Assert
        self.assertEqual(actual_x_position, expected_x_position)

    def test_player_x_position_sets(self):
        # Arrange
        self.player.set_x(17)
        # Act
        actual_x_position = self.player.get_x()
        expected_x_position = 17
        # Assert
        self.assertEqual(actual_x_position, expected_x_position)

    def test_player_y_position_is_sixteen(self):
        # Act
        actual_y_position = self.player.get_y()
        expected_y_position = 16
        # Assert
        self.assertEqual(actual_y_position, expected_y_position)

    def test_player_y_position_sets(self):
        # Arrange
        self.player.set_y(17)
        # Act
        actual_y_position = self.player.get_y()
        expected_y_position = 17
        # Assert
        self.assertEqual(actual_y_position, expected_y_position)

    def text_player_doesnt_have_totem(self):
        # Act
        has_totem = self.player.get_has_totem()
        # Assert
        self.assertFalse(has_totem)

    def test_player_has_totem(self):
        # Arrange
        self.player.found_totem()
        # Act
        has_totem = self.player.get_has_totem()
        # Assert
        self.assertTrue(has_totem)


if __name__ == '__main__':
    unittest.main(verbosity=2)
