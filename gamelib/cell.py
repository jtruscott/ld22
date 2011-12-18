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
    door = False
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

class Item(Cell):
    consumable = True
    item_map = {
        'e': 'eyepatch',
        'f': 'fish',
        'b': 'broom',
        'g': 'rubber gloves',
    }

    def consume(self):
        item = self.item_map[self.char[2]]
        state.inventory.append(item)
        message.add("You found a <WHITE>%s</>." % item)

class Goblin(Cell):
    passable = False
    special = True

    def __init__(self, x, y, room, char):
        Cell.__init__(self, x, y, room, char)
        self.hp = 12
        state.goblin_alive = True

    def on_use(self):
        if not state.goblin_alive:
            return

        damage_taken = random.randint(1, 8) + ((state.player.strength - 10) / 2)
        message.add("Your %s deals <GREEN>%i</> damage to the goblin!" % (state.player.weapon, damage_taken))

        self.hp -= damage_taken
        if self.hp <= 0:
            message.add("<GREEN>The evil goblin falls!")
            message.add("You take a <WHITE>goblin head</> as a trophy.\n")
            state.inventory.append('goblin head')
            message.add("You find a <WHITE>white key</>.")
            state.inventory.append('white key')
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
    special = 'staircase'
    def on_use(self):
        if state.player.san_loss < 5:
            message.add("Those are the stairs out. Your quest is not complete.")
        else:
            self.passable = True
            sanity.no_stairs()
    
    def clear(self):
        self.room.set_at(self.x, self.y, fg=colors.BLACK, bg=colors.BLACK, char=' ')
        self.char[0] = colors.BLACK
        self.char[1] = colors.BLACK
        self.char[2] = ' '
        self.passable = True

class Console(Impassable):
    consoles = {
        colors.BROWN: """
<GREEN>></> i'm a brown console
<GREEN>></> short and stout
        """,
        colors.MAGENTA: """
<GREEN>></> i'm a magenta console
        """,
        colors.GREEN: """
<GREEN>></> i'm a green console
        """
    }
    def on_use(self):
        if self.consumed:
            return
        msg = self.consoles[self.char[0]]
        message.add("\nA message appears on the video console.")
        message.add(msg)
        self.consumed = True


color_map = {
    colors.WHITE: 'white',
    colors.YELLOW: 'yellow',
    colors.RED: 'red',
    colors.BLUE: 'blue',
    colors.BROWN: 'brown',
    colors.GREEN: 'green',
}

class Key(Cell):
    consumable = True
    def consume(self):
        item = '%s key' % color_map[self.char[0]]
        state.inventory.append(item)
        message.add("You found a <WHITE>%s</>." % item)

class Door(Impassable):
    special = True
    def on_use(self):
        item = '%s key' % color_map[self.char[0]]
        if item not in state.inventory:
            message.add("You need a <WHITE>%s</> to unlock this door" % item)
        else:
            message.add("Your <WHITE>%s</> unlocks the door." % item)
            self.door = True
            self.passable = True
            self.clear()

class Shudderpoint(Cell):
    def __init__(self, *args, **kwargs):
        Cell.__init__(self, *args, **kwargs)
        self.clear()

    def on_use(self):
        if self.consumed:
            return
        sanity.shudder(nomsg=True)
        self.consumed = True

cell_types = {
    (colors.RED, 'o'): HealthPickup,
    (colors.GREEN, 'o'): StaminaPickup,
    (colors.DARKGREY, colors.LIGHTGREY, chr(0xDC)): Staircase,
    (colors.LIGHTGREEN, 'G'): Goblin,
    chr(0xDB): Impassable,
    chr(0x9C): Key,
    '/': Door,
    '=': Door,
    'C': Console,
    '$': Shudderpoint,
    'default': Cell
}

cell_types.update(dict([(k, Item) for k in Item.item_map.keys()]))
