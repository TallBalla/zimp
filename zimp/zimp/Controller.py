from Game import Game
from Player import Player
from SetUp import SetUp
from View import View


class Controller():
    game = None
    setup = SetUp()
    view = View()

    def setup_game(self):
        self.setup.gen_inside_tiles()
        self.setup.gen_outside_tiles()
        self.setup.gen_dev_cards()
        self.setup.gen_tile_index()

        player = Player(self.view.get_user_name())

        self.game = Game(player,
                         self.setup.get_dev_cards(),
                         self.setup.get_inside_tiles(),
                         self.setup.get_outside_tiles())

    def start_game(self):

        #while not self.game.get_is_totem_buried():
        # view player stats

        # draw tile
        tile = self.game.draw_tile_handler()
        # view tile
        self.view.tile_display(tile)
        # handle tile

        # draw dev card

        # view dev card

        # handle devcard

        self.game.complete_game()
