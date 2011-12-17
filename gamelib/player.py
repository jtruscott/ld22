import pytality
import logging
log = logging.getLogger('player')

class Player(object):
    def __init__(self):
        self.max_hp = 10 + self.strength * 2
        self.max_stamina = 10 + self.dexterity * 2
        self.max_sanity = 80 + self.intelligence * 2

        self.hp = self.max_hp
        self.stamina = self.max_stamina
        self.sanity = self.max_sanity

class Fighter(Player):
    title = "Fighter"
    strength = 18
    dexterity = 14
    intelligence = 12

class Wizard(Player):
    title = "Wizard"
    strength = 12
    dexterity = 14
    intelligence = 18

class Ranger(Player):
    title = "Ranger"
    strength = 12
    dexterity = 18
    intelligence = 14



