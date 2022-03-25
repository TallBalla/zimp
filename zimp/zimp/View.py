class View():
    '''displays the cli for the game'''

    def get_user_name(self):
        return input("Please enter user name: ")

    def display_drawing_dev_card(self):
        print("\nDrawing Dev Card...\n")

    def display_drawing_tile(self):
        print("\nDrawing Tile...\n")

    def display_player(self, player):
        print(f"h {player.get_player_health()}", end=" | ")
        print(f"d {player.get_player_attack()}")

    def display_event(self, time ,event):
        print(f"{time}:00 PM")
        print(event.get_event_desc())

    def display_tile(self, tile):
        print(tile.get_tile_name())
        print(tile.get_tile_description())

    def dsiplay_totem_collected(self):
        print("\nTOTEM COLLECTED\n")

    def warning_draw_devcard(self, ):
        print(f"WARNING, INVOLES DRAWING DEVCARD\n")

    def warning_shuffle_dev_card(self):
        print("NO DEV CARDS AVALIBLE, SHUFFLING DEV CARDS\n")

    def warning_no_totem(self):
        print("NO TOTEM, FIND TOTEM TO COMPLETE GAME\n")

    def warning_zombie_door(self):
        print("0 EXITS AVALIBLE, CREATING ZOMBIE DOOR\n")

    def check_use_item(self, item_name):
        use_item = input(f"Do you want to use {item_name} (Y/N)? ")

        if use_item[0].lower() == "y":
            return True
        elif use_item[0].lower() == "n":
            return False
        else: 
            print("Invalid input, please enter y or n\n")
            self.check_use_item(item_name)

    def check_draw_devcard(self):
        devcard = input(f"Do you want to collect item (Y/N)? ")

        if devcard[0].lower() == "y":
            return True
        elif devcard[0].lower() == "n":
            return False 
        else: 
            print("Invalid input, please enter y or n\n")
            self.check_draw_devcard()

    def check_add_item(self, player_item, item_name):
        item = input(f"\nDo you want to add item {item_name} to {player_item} (y/n)? ")
        if item[0].lower() == "y":
            return True
        elif item[0].lower() == "n":
            return False
        else: 
            print("Invalid input, please enter y or n\n")
            self.check_add_item(player_item, item_name)

    def check_go_outside(self):
        go_outside = input("\nWould you like to go outside (y/n)? ")
        if go_outside[0] == "y":
            print("going outside")
            return True
        elif go_outside[0] == "n":
            return False
        else:
            print("Invalid input, please enter y or n\n")
            self.check_go_outside()

    def check_go_inside(self):
        go_inside = input("\nWould you like to go back inside (y/n)? ")
        if go_inside[0].lower == "y":
            print("going inside")
            return True
        elif go_inside[0] == "n":
            return False
        else:
            print("Invalid input, please enter y or n\n")
            self.check_go_inside()

    def check_player_runaway(self, damage, zombies):
            if damage >= 0:
                print(f"{zombies} ZOMBIES APPEARS, IF YOU STAY YOU WILL NOT TAKE DAMAGE")
            else:
                print(f"{zombies} ZOMBIES APPEARS, IF YOU STAY YOU WILL TAKE {abs(damage)} DAMAGE")

            runaway = input("Do you want to run away (y/n)? ")
            if runaway[0].lower() == "y":
                return True
            elif runaway[0].lower() == "n":
                return False
            else: 
                print("Invalid input, please enter y or n\n")
                self.check_player_runaway()