import unittest
from parameterized import parameterized

from Commands import Commands
from DevCard import DevCard
from directions import Direction as d


class TriggerDevCardBranchTests(unittest.TestCase):
    def setUp(self):
        self.commands = Commands()
        self.commands.do_start()
        self.game = self.commands.get_game()
        self.game.place_tile(16, 16)
        self.game.set_state('Drawing Dev Card')

    def tearDown(self) -> None:
        del self.commands
        del self.game

    def set_up_game_with_dev_cards(self,
                                   event_one,
                                   event_three=('Item', 0)):
        flyweight_factory = self.game.get_flyweight_factory()
        test_dev_cards = []
        test_dev_card = DevCard()
        test_dev_card.set_flyweight_facotry(flyweight_factory)
        test_dev_card.set_item('test', 1)
        test_dev_card.add_event(event_one[0], event_one[1])
        test_dev_card.add_event('test', 1)
        test_dev_card.add_event(event_three[0], event_three[1])

        test_dev_cards.append(test_dev_card)

        self.game.set_dev_cards(test_dev_cards)

    def set_up_player(self, attack=0, health=6):
        self.player = self.game.get_player()
        self.player.set_attack(attack)
        self.player.set_health(health)

    @parameterized.expand([
        (11, 11, 'Game Over'),
    ])
    def test_trigger_dev_card_with_no_dev_cards(self,
                                                time: int,
                                                expected_time: int,
                                                expected_state: str,):
        self.game.set_time(time)
        self.game.set_state('Drawing Dev Card')
        self.game.set_dev_cards([])

        self.commands.do_draw()

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

        with self.subTest(f'time_has_changed_to_{time}'):
            self.assertEqual(self.game.get_time(), expected_time)

    @parameterized.expand([
        (9, 10),
        (10, 11),
    ])
    def test_trigger_dev_card_increments_item(self,
                                              time: int,
                                              expected_time: int):
        self.game.set_time(time)
        self.game.set_state('Drawing Dev Card')
        self.game.set_dev_cards([])

        self.commands.do_draw()

        with self.subTest(f'time_has_changed_to_{time}'):
            self.assertEqual(self.game.get_time(), expected_time)

    @parameterized.expand([
        ('Foyer', [], ('Nothing', None), 'Moving'),
        ('Foyer', [d.NORTH], ('Nothing', None), 'Moving'),
        ('Foyer', [d.NORTH, d.SOUTH], ('Nothing', None), 'Moving'),
        ('Not Foyer', [d.NORTH], ('Nothing', None), 'Choosing Door'),
        ('Not Foyer', [d.NORTH, d.SOUTH], ('Nothing', None), 'Moving'),
    ])
    def test_trigger_dev_card_with_event_nothing(self,
                                                 chosen_tile_name,
                                                 chosen_tile_doors: list,
                                                 event: list,
                                                 expected_state: str):

        self.set_up_game_with_dev_cards(event)
        self.set_up_player()

        self.game.set_chosen_tile_name(chosen_tile_name)
        self.game.set_chosen_tile_doors(chosen_tile_doors)

        self.commands.do_draw()

        with self.subTest(f'dev_card_length_is_0'):
            self.assertEqual(len(self.game.get_dev_cards()), 0)

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

    @parameterized.expand([
        ('Foyer', [], ('Health', 2), 8, 'Moving'),
        ('Foyer', [], ('Health', 0), 6, 'Moving'),
        ('Foyer', [], ('Health', 1), 7, 'Moving'),
        ('Foyer', [], ('Health', -6), 0, 'Game Over'),
        ('Foyer', [], ('Health', -7), -1, 'Game Over'),
        ('Not Foyer', [d.NORTH], ('Health', 1), 7, 'Choosing Door'),
        ('Garden', [d.NORTH, d.SOUTH], ('Health', 1), 8, 'Moving'),
        ('Kitchen', [d.NORTH, d.SOUTH], ('Health', 1), 8, 'Moving'),
    ])
    def test_trigger_dev_card_with_event_health(self,
                                                chosen_tile_name: str,
                                                chosen_tile_doors: list,
                                                event: list,
                                                expected_player_health: int,
                                                expected_state: str):
        self.set_up_game_with_dev_cards(event)
        self.set_up_player()

        self.game.set_chosen_tile_name(chosen_tile_name)
        self.game.set_chosen_tile_doors(chosen_tile_doors)

        self.commands.do_draw()

        with self.subTest(f'dev_card_length_is_0'):
            self.assertEqual(len(self.game.get_dev_cards()), 0)

        with self.subTest(f'player_health_is_{expected_player_health}'):
            self.assertEqual(self.player.get_health(), expected_player_health)

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

    @parameterized.expand([
        ('Foyer', [], 11, [], 'Game Over', 11, ('Item', 1)),
        ('Foyer', [], 9, [], 'Moving', 9, ('Item', 1)),
        ('Not Foyer', [d.NORTH], 9, [], 'Choosing Door', 9, ('Item', 1)),
    ])
    def test_trigger_dev_card_with_event_item(self,
                                              chosen_tile_name: str,
                                              chosen_tile_doors: list,
                                              time: int,
                                              items: list,
                                              expected_state: str,
                                              expected_time: int,
                                              event_one: list,
                                              event_three=('Item', 0)):

        self.set_up_game_with_dev_cards(event_one, event_three)
        self.set_up_player()

        self.game.set_chosen_tile_name(chosen_tile_name)
        self.game.set_chosen_tile_doors(chosen_tile_doors)
        self.game.set_time(time)

        self.player.set_items(items)

        self.commands.do_draw()

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

        with self.subTest(f'time_is_{expected_time}'):
            self.assertEqual(self.game.get_time(), expected_time)

    @parameterized.expand([
        (['Zombies', 2], 'Attacking', 2),
        (['Zombies', 0], 'Attacking', 0)
    ])
    def test_trigger_dev_card_with_event_zombies(self,
                                                 event: list,
                                                 expected_state: str,
                                                 expected_zombies: int):

        self.set_up_game_with_dev_cards(event)

        self.commands.do_draw()

        with self.subTest(f'state_has_changed_to_{expected_state}'):
            self.assertEqual(self.game.get_state(), expected_state)

        with self.subTest(f'zombies_are_{expected_zombies}'):
            self.assertEqual(self.game.get_current_zombies(), expected_zombies)


if __name__ == '__main__':
    unittest.main()

# coverage run --branch --source=Game triggerDevCardBranchTests.py
# coverage report -m
# coverage html -d ../coverage_html/
