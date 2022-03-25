from Game import Game
from Player import Player
from SetUp import SetUp
from View import View

from functools import partial

class Controller():

    def __init__(self):
        self.game = None
        self.setup = SetUp()
        self.view = View()
        self.tile_props = {
                'exterior door inside': self.exterior_door_inside,
                'exterior door outside': self.exterior_door_outside,
                'health increase': self.add_health,
                'item': self.collect_item,
                'totem': self.collect_totem,
                'totem bural': self.bury_totem,
                }
        self.event_props = {
                'zombie 3': partial(self.zombie_attack, 3),
                'zombie 4': partial(self.zombie_attack, 4),
                'zombie 5': partial(self.zombie_attack, 5),
                'zombie 6': partial(self.zombie_attack, 6),
                'add health': self.add_health,
                'remove health': self.remove_health,
                'item': self.collect_item,
                }

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

    def run(self):
        # display the first room
        current_tile = self.game.get_current_tile()
        self.view.display_tile(current_tile)

        i = 0
        #while not self.game.check_player_has_buried_totem():
        while i < 3:
        # view player stats
            self.view.display_player(self.game.get_player())
            self.view.display_drawing_tile()

            tile = self.draw_tile()
            self.view.display_tile(tile)

            self.view.display_drawing_dev_card()
            #This is done so a dev card has to be handled before the tile
            dev_card = self.draw_dev_card()

            event = self.game.get_event(dev_card)
            self.view.display_event(self.game.get_time(), event)

            if self.game.check_event_prop_is_not_none(event):
                self.event_props.get(event.get_event_prop())()

            if self.game.check_tile_prop_is_not_none(tile):
                self.tile_props.get(tile.get_tile_prop())()


    def draw_tile(self):
        if self.game.check_for_zombie_door():
            self.view.warning_zombie_door()
            self.zombie_attack(int(3))

        new_tile = self.game.draw_tile()
        
        return new_tile


    def draw_dev_card(self):
        self.game.increment_dev_card_index()

        if self.game.check_avail_dev_cards():
            self.view.warning_shuffle_dev_card()
            self.game.reshuffle()

        new_dev_card = self.game.draw_dev_card()

        return new_dev_card


    def exterior_door_inside(self):
        if self.view.check_go_outside():
            self.game.set_tiles_outside()
            self.game.set_location()  


    def exterior_door_outside(self):
        if self.view.check_go_inside():
            self.game.set_tiles_inside()
            self.game.set_location()

    def collect_item(self):
        player = self.game.get_player()

        self.view.display_drawing_dev_card()

        if self.view.check_draw_devcard():
            item = self.game.collect_item()

            if self.view.check_add_item('Item One', item.get_item_name()):
                player.item_one = item

            elif self.view.check_add_item('Item Two', item.get_item_name()):
                player.item_two = item

        self.game.set_player(player)

    def collect_totem(self): 
        dev_card = self.draw_dev_card()
        event = self.game.get_event(dev_card)

        self.view.display_drawing_dev_card()
        self.view.display_event(self.game.get_time(), event)

        if self.game.check_event_prop_is_not_none(event):
            self.event_props.get(event.get_event_prop())()

        self.view.dsiplay_totem_collected()


    def bury_totem(self):
        if self.game.check_player_has_totem():
            # To win the game you need to draw dev card
            print("complete game")

        self.view.warning_no_totem()
        

    def zombie_attack(self, zombie_damage):
        print("there was a zombie attack")

    def add_health(self):
        self.game.add_health(int(1))

    def remove_health(self):
        print("health removed") 
        
    def move_to_previous_tile(self):
        return
        