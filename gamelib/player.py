import pytality

import logging
log = logging.getLogger('player')

class Player(object):
    def __init__(self):
        self.max_hp = self.strength * 2
        self.max_stamina = self.dexterity * 2

        self.hp = self.max_hp
        self.stamina = self.max_stamina
        self.san_loss = 0
        self.steps = 0

    def lose_hp(self, amount, source):
        self.hp -= amount
        if self.hp <= 0:
            self.die(source)

    def lose_san(self, amount):
        self.san_loss += amount

class Fighter(Player):
    title = "Fighter"
    weapon = "sword"
    strength = 18
    dexterity = 14
    intelligence = 12

class Wizard(Player):
    title = "Wizard"
    weapon = "staff"
    strength = 12
    dexterity = 14
    intelligence = 18

class Ranger(Player):
    title = "Ranger"
    weapon = "bow"
    strength = 12
    dexterity = 18
    intelligence = 14



