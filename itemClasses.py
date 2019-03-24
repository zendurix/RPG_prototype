

class ITEM:

    def __init__(self, name, atk_buff, armor_buff):
        self.atk_buff = atk_buff
        self.armor_buff = armor_buff
        self.name = name

    def equipping(self, character):
        already_in_eq = False
        if type(self) == Weapon:
            for item in character.equipment:
                if type(item) == Weapon:
                    already_in_eq = True

        elif type(self) == Chest:
               for item in character.equipment:
                   if type(item) == Chest:
                        already_in_eq = True

        if not already_in_eq:
            character.equipment.append(self)
            character.inv.remove(self)
            character.atk += self.atk_buff
            character.armor += self.armor_buff

        else:
            print("You already have that kind of item in equipment")

    def deequipping(self, character, place):
        character.equipment.remove(self)
        character.atk -= self.atk_buff
        character.armor -= self.armor_buff
        if len(character.inv) < character.inv_max:
            character.inv.append(self)
        else:
            print("Inventory is full, you throw away ", self.name)
            place.items_here.append(self)


class Dead_body(ITEM):
    def __init__(self, name, print_format, atk_buff=0, armor_buff=0):
        ITEM.__init__(self, name, atk_buff, armor_buff)
        self.print_format = print_format

class Weapon(ITEM):

    def __init__(self, name, atk_buff=3, armor_buff=0):
        ITEM.__init__(self, name, atk_buff, armor_buff)


dagger = Weapon("rusty dagger", atk_buff=1)
short_sword = Weapon("short sword")

class Chest(ITEM):

    def __init__(self, name, atk_buff=0, armor_buff=5):
        ITEM.__init__(self, name, atk_buff, armor_buff)


shirt = Chest("dirty shirt", armor_buff=0)
mail = Chest("chain_mail", armor_buff=3)
