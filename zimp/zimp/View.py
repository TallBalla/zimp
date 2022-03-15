class View():
    '''displays the cli for the game'''

    def check_use_item(self, item_name):
        use_item = input(f"Do you want to use {item_name} (Y/N)? ")
        if use_item[0].lower() == "y":
            return True
        elif use_item[0].lower() == "n":
            return False
        else: 
            print("Invalid Input")
            self.check_use_item(item_name)
