class View():
    '''displays the cli for the game'''

    def check_use_item(self, item_name):
        use_item = input(f"Do you want to use {item_name} (Y/N)? ")
        print()

        if use_item[0].lower() == "y":
            return True
        elif use_item[0].lower() == "n":
            return False
        else: 
            print("Invalid Input")
            print()
            self.check_use_item(item_name)

    def check_draw_devcard(self):
        devcard = input(f"Do you want to collect item (Y/N)? ")
        print()

        if devcard[0].lower() == "y":
            return True
        elif devcard[0].lower() == "n":
            return False 
        else: 
            print("Invalid Input")
            print()
            self.check_draw_devcard()

    def draw_devcard_warning(self):
        print("WARING, INVOLES DRAWING DEVCARD")

    def shuffle_dev_card_warning(self):
        print("NO DEV CARDS AVALIBLE, SHUFFLING DEV CARDS")

    def no_totem_warning(self):
        print("NO TOTEM, FIND TOTEM TO COMPLETE GAME")

    def zombie_door_warning(self):
        print("0 EXITS AVALIBLE, CREATING ZOMBIE DOOR")

    def check_player_runaway(self, damage, zombies):
        if damage >= 0:
            print(f"{zombies} ZOMBIES APPEARS, IF YOU STAY YOU WILL NOT TAKE DAMAGE")
        else:
            print(f"{zombies} ZOMBIES APPEARS, IF YOU STAY YOU WILL TAKE {abs(damage)} DAMAGE")

        runaway = input("Do you want to run away (Y/N)? ")
        if runaway[0].lower() == "y":
            return True
        elif runaway[0].lower() == "n":
            return False
        else: 
            print("Invalid Input")
            print()
            self.check_player_runaway()


    def check_add_item(self, player_item, item_name):
        item = input(f"Do you want to add item {item_name} to {player_item} (Y/N)? ")
        print()
        if item[0].lower() == "y":
            return True
        elif item[0].lower() == "n":
            return False
        else: 
            print("Invalid Input")
            print()
            self.check_add_item(player_item, item_name)

    def check_replace_item(self, player_item, item_name):
        item_replace = input(f"Are you sure you want to replace {player_item} with {item_name} (Y/N)? ")
        print()
        if item_replace[0].lower() == "y":
            return True
        elif item_replace[0].lower() == "n":
            return False
        else: 
            print("Invalid Input")
            self.check_replace_item(player_item, item_name)
        return False