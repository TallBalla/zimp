from .attackStrategy import AttackStrategy


class OneItemAttackStrategy(AttackStrategy):
    def attack(self, item_names: list[str]) -> None:
        if "Machete" in item_names:
            self.context.player_attack += 2

        elif "Chainsaw" in item_names:
            if self.context.player.get_item_charges("Chainsaw") > 0:
                self.context.player_attack += 3
                self.context.player.use_item_charge("Chainsaw")
            else:
                print("\nThis item has no charges left\n")

        elif "Golf Club" in item_names \
            or "Grisly Femur" in item_names \
                or "Board With Nails" in item_names:
            self.context.player_attack += 1

        elif "Can of Soda" in item_names:
            self.context.player.add_health(2)
            self.context.drop_item("Can of Soda")
            print("\nUsed Can of Soda, gained 2 health\n")

        elif "Oil" in item_names:
            self.context.trigger_run(self.context.choose_avalible_door(), 0)
            raise Exception()

        else:
            print("\nYou cannot use this item right now, try again\n")
            raise Exception()
