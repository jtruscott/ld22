import pytality
import state

import logging
import os
import message
import sanity
import random

log = logging.getLogger("cell")
colors = pytality.colors

class Cell:
    passable = True
    consumable = False
    consumed = False
    special = False
    volatile_bg = False

    def __init__(self, x, y, room, char):
        if char[1] == colors.CYAN:
            self.volatile_bg = True

        self.char = char
        self.x = x
        self.y = y
        self.room = room

    def on_use(self):
        if self.consumable and not self.consumed:
            self.consume()
            self.consumed = True
            self.clear()
    
    def clear(self):
        self.room.set_at(self.x, self.y, char=' ')
        self.char[2] = ' '
        self.passable = True

class HealthPickup(Cell):
    consumable = True
    def consume(self):
        message.add("health pickup!")

class StaminaPickup(Cell):
    consumable = True
    def consume(self):
        message.add("stamina pickup!")

class StartingPosition(Cell):
    def __init__(self, x, y, room, char):
        Cell.__init__(self, x, y, room, char)
        state.player.x = x
        state.player.y = y
        self.clear()

class Goblin(Cell):
    passable = False
    special = True

    def __init__(self, x, y, room, char):
        Cell.__init__(self, x, y, room, char)
        self.hp = 12
        state.goblin_alive = True

    def on_use(self):
        damage_taken = random.randint(1, 8) + ((state.player.strength - 10) / 2)
        message.add("Your %s deals <GREEN>%i</> damage to the goblin!" % (state.player.weapon, damage_taken))

        self.hp -= damage_taken
        if self.hp <= 0:
            message.add("<GREEN>The evil goblin falls!")
            message.add("You take it's head as a trophy.\n")
            message.add("<YELLOW>You find a small key.")
            state.goblin_alive = False
            state.goblin_head = True
            state.found_small_key = True
            self.clear()
            return

        damage_dealt = random.randint(1, 4) + 4
        message.add("The evil goblin deals <RED>%i</> damage to you!" % damage_dealt)
        state.player.lose_hp(damage_dealt, "evil goblin")
        message.add('')
        

class Impassable(Cell):
    passable = False

class Staircase(Impassable):
    special = True
    def on_use(self):
        if state.player.san_loss < 5:
            message.add("Those are the stairs out. Your quest is not complete.")
        else:
            self.passable = True
            sanity.no_stairs()

cell_types = {
    (colors.RED, 'o'): HealthPickup,
    (colors.GREEN, 'o'): StaminaPickup,
    (colors.LIGHTMAGENTA, '@'): StartingPosition,
    (colors.DARKGREY, colors.LIGHTGREY, chr(0xDC)): Staircase,
    (colors.LIGHTGREEN, 'G'): Goblin,
    chr(0xDB): Impassable,
    'default': Cell
}
