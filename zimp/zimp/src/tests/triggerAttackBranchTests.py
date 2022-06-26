import unittest
from parameterized import parameterized
from Commands import Commands


class TriggerAttackBranchTests(unittest.TestCase):
    def setUp(self):
        self.commands = Commands()
        self.commands.do_start()
        self.game = self.commands.get_game()
        self.game.place_tile(16, 16)
        self.player = None

    def tearDown(self) -> None:
        del self.commands
        del self.game

    def set_up_game(self, game_state='Attacking', zombies=0):
        self.game.set_state(game_state)
        self.game.current_zombies = zombies

    def set_up_player(self, attack=0, health=6):
        self.player = self.game.get_player()
        self.player.set_attack(attack)
        self.player.set_health(health)

        # zombie_count, attack, health, expected_health, expected_state
    @parameterized.expand([
        ('Attacking', 2, 0, 6, 4, 'Moving'),
        ('Attacking', 0, 0, 6, 6, 'Moving'),
        ('Attacking', 6, 0, 6, 0, 'Game Over'),
        ('Moving', 0, 0, 6, 6, 'Moving'),
        ('Moving', 3, 5, 6, 6, 'Moving'),
    ])
    def test_trigger_attack_with_no_items(self,
                                          game_state: str,
                                          zombies: int,
                                          attack: int,
                                          health: int,
                                          expected_health: int,
                                          expected_state: str):

        self.set_up_game(game_state, zombies)
        self.set_up_player(attack, health)

        self.commands.do_fight(', ')

        with self.subTest('can_cower_is_true'):
            self.assertTrue(self.game.can_cower)

        with self.subTest(f'player_health_is_{expected_health}'):
            self.assertEqual(self.player.get_health(), expected_health)

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

    @parameterized.expand([
        ('Garden', 'Choosing Door', 7),
        ('Kitchen', 'Choosing Door', 7),
        ('Foyer', 'Moving', 6),
    ])
    def test_trigger_attack_when_healing_room(self,
                                              room_name: str,
                                              expected_state: str,
                                              expected_player_health: int):

        self.set_up_game()
        self.set_up_player()

        current_tile = self.game.get_current_tile()
        current_tile.set_name(room_name)

        self.commands.do_fight(', ')

        with self.subTest('can_cower_is_true'):
            self.assertTrue(self.game.can_cower)

        with self.subTest(f'player_health_is_{expected_player_health}'):
            self.assertEqual(self.player.get_health(), expected_player_health)

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

        with self.subTest('zombie_count_is_0'):
            self.assertEqual(self.game.current_zombies, 0)

    @parameterized.expand([
        (4, 'Machete', 1, 'Moving', 4),
        (4, 'Chainsaw', 1, 'Moving', 5),
        (4, 'Chainsaw', 0, 'Moving', 2),
        (4, 'Golf Club', 1, 'Moving', 3),
        (4, 'Grisly Femur', 1, 'Moving', 3),
        (4, 'Board With Nails', 1, 'Moving', 3),
        (0, 'Can of Soda', 1, 'Moving', 8),
        (0, 'Oil', 1, 'Attacking', 6),
        (0, 'Not an Item', 1, 'Attacking', 6),
    ])
    def test_trigger_attack_with_one_attack_item(self,
                                                 zombie_count: int,
                                                 item_name: str,
                                                 item_charge: int,
                                                 expected_state: str,
                                                 expected_player_health: int):

        self.set_up_game(zombies=zombie_count)
        self.set_up_player()

        self.player.add_item(item_name, item_charge)

        self.commands.do_fight(f'{item_name}, ')

        with self.subTest('can_cower_is_true'):
            self.assertTrue(self.game.can_cower)

        with self.subTest(f'player_health_is_{expected_player_health}'):
            self.assertEqual(self.player.get_health(), expected_player_health)

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

    @parameterized.expand([
        (0, 'Oil', 'Candle', 2, ['Candle'], 'Moving', 6),
        (4, 'Gasoline', 'Candle', 2, ['Candle'], 'Moving', 6),
        (3, 'Gasoline', 'Chainsaw', 2, ['Chainsaw'], 'Moving', 6),
        (3, 'Machete', 'Chainsaw', 2, ['Machete', 'Chainsaw'], 'Attacking', 6),
    ])
    def test_trigger_attack_with_two_attack_items(self,
                                                  zombie_count: int,
                                                  item_one_name: str,
                                                  item_two_name: str,
                                                  item_charge: str,
                                                  expected_item_names,
                                                  expected_state: str,
                                                  expected_player_health: int):

        self.set_up_game(zombies=zombie_count)
        self.set_up_player()

        self.player.add_item(item_one_name, item_charge)
        self.player.add_item(item_two_name, item_charge)

        self.commands.do_fight(f'{item_one_name}, {item_two_name}')

        with self.subTest('can_cower_is_true'):
            self.assertTrue(self.game.can_cower)

        with self.subTest(f'player_health_is_{expected_player_health}'):
            self.assertEqual(self.player.get_health(), expected_player_health)

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

        with self.subTest(f'player_items_equal'):
            self.assertEqual(self.player.get_items_names(),
                             expected_item_names)


if __name__ == '__main__':
    unittest.main()

# coverage run --branch --source=Game triggerAttackBranchTests.py
# coverage report -m
# coverage html -d ../coverage_html/
