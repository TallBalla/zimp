from Game import Game
from Player import Player
from SetUp import SetUp
from View import View
from functools import partial


class Controller():
    def __init__(self):
        self.game = None
        self.setup = SetUp()
        self.runaway = False
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
                'remove health': partial(self.remove_health, 1),
                'item': self.collect_item,
                }
        self.item_props = {
                'attack 1': 1,
                'attack 2': 2,
                'attack 3': 3,
                'health': 2,
                'combination': self.use_item_combination,
                'combination special': self.use_item_combination_special,
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
        # while not self.game.check_player_has_buried_totem():
        while i < 3:
            self.runaway = False

            # view player stats
            self.view.display_drawing_tile()
            #print()
            #for ti in self.game.get_tiles():
            #    print(ti.get_tile_name())

            tile = self.draw_tile()

            self.view.display_tile(tile)

            #for tile in self.game.get_connected_tiles():
            #    print(tile.get_tile_name())

            self.view.display_player(self.game.get_player())



            self.view.display_drawing_dev_card()

            dev_card = self.draw_dev_card()
            event = self.game.get_event(dev_card)

            self.view.display_event(self.game.get_time(), event)

            #if self.game.check_event_prop_is_not_none(event):
            #    self.event_props.get(event.get_event_prop())()

            if self.game.check_tile_prop_is_not_none(tile):
                print("tile prop is not none")
                self.tile_props.get(tile.get_tile_prop())()

    def draw_tile(self):

        if self.game.check_for_zombie_door():
            self.zombie_door_attack()
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

        if self.game.check_avail_dev_cards():
            self.view.warning_shuffle_dev_card()
            self.game.reshuffle()
        self.view.display_drawing_dev_card()

        if self.view.check_draw_devcard():
            self.game.increment_dev_card_index()
            item = self.game.collect_item()

            if self.view.check_add_item('Item One', item.get_item_name()):
                player.set_item_one(item)

            elif self.view.check_add_item('Item Two', item.get_item_name()):
                player.set_item_two(item)
        self.game.set_player(player)

        if self.game.check_player_holds_health_item():
            health = int(self.item_props.get(item.get_item_prop()))
            self.use_item_health(health)

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

    def get_player_damage(self):
        player = self.game.get_player()
        damage = player.get_player_attack()

        if self.game.check_player_holds_attack_item():
            damage += self.use_item_attack()
        return damage

    def zombie_attack(self, zombies):
        player_damage = self.get_player_damage()
        damage_taken = zombies - player_damage

        if self.view.check_player_runaway(zombies, damage_taken):
            self.runaway = True

            if self.game.check_player_holds_special_item():

                if self.view.check_player_use_special_item():
                    self.use_item_combination_special()
                    return
            self.remove_health(int(1))
            return
        self.remove_health(damage_taken)
    
    def zombie_door_attack(self):
        self.view.warning_zombie_door()


    def add_health(self):
        self.game.add_health(int(1))

    def remove_health(self, health):
        self.game.remove_health(health)

    def move_to_previous_tile(self):
        return

    def use_item_attack(self):
        player = self.game.get_player()

        for item in player.get_attack_items():

            if self.view.check_player_use_item(item):
                item.use_item()
                return self.item_props.get(item.get_item_prop())
        return 0
    
    def use_item_health(self, health):
        self.game.add_health(health)

    def use_item_combination(self):
        return    
    
    def use_item_combination_special(self):
        player = self.game.get_player()

        for item in player.get_special_items():

            if self.view.check_use_item(item):
                item.use_item()
                break
