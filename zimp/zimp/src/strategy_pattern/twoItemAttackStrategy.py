from .attackStrategy import AttackStrategy


class TwoItemAttackStrategy(AttackStrategy):
    def attack(self, item: any) -> None:
        if "Oil" in item and "Candle" in item:
            print("\nYou used the oil and the candle to"
                  " attack the zombies, it kills all of them\n")
            self.context.drop_item("Oil")
            self.context.set_state("Moving")
            raise Exception()

        elif "Gasoline" in item and "Candle" in item:
            print("\nYou used the gasoline and the candle"
                  " to attack the zombies, it kills all of them\n")
            self.context.drop_item("Gasoline")
            self.context.set_state("Moving")
            raise Exception()

        elif "Gasoline" in item and "Chainsaw" in item:
            chainsaw_charge = self.context.player.get_item_charges("Chainsaw")
            self.context.player.set_item_charges("Chainsaw",
                                                 chainsaw_charge + 2)
            self.context.player_attack += 3
            self.context.drop_item("Gasoline")
            self.context.player.use_item_charge("Chainsaw")

        else:
            print("\nThese items cannot be used together, try again\n")
            raise Exception()