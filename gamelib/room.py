import pytality
import state

import logging
import os, time
import message
import cell
import sanity

log = logging.getLogger("room")
colors = pytality.colors

class Room:
    def __init__(self, config, prev_room=None):
        self.map = config['map']
        self.sane_buffer = self.load(self.map)
        self.shudder_buffer = self.load(config.get('shudder_map', None))
        self.mode = 'sane'
        self.on_activate = config.get('on_activate', None)

        self.build_cells()

        self.prev_room = prev_room
        if 'next' in config:
            self.next_room = Room(config['next'], prev_room=self)

    def load(self, mapfile):
        if not mapfile:
            return
        full_path = os.path.join('data', mapfile)
        buf = pytality.ansi.read_to_buffer(open(full_path), crop=False, max_height=54)
        return buf

    def build_cells(self):
        def get_cell(c, x, y):
            fg, bg, ch = c
            for key in [(fg, bg, ch), (fg, ch), ch, 'default']:
                if key in cell.cell_types:
                    return cell.cell_types[key](x, y, self, c)

        self.cells = []
        y = 0
        for row in self.sane_buffer._data:
            new_row = []
            x = 0
            for c in row:
                new_row.append(get_cell(c, x, y))
                x += 1
            y += 1
            self.cells.append(new_row)

        self.width = self.sane_buffer.width
        self.height = self.sane_buffer.height

    def draw(self, *args, **kwargs):
        if self.mode == 'shudder':
            buf = self.shudder_buffer
        else:
            buf = self.sane_buffer
        buf.draw(*args, **kwargs)

    def set_at(self, x, y, **kwargs):
        for buf in [self.sane_buffer, self.shudder_buffer]:
            if buf:
                buf.set_at(x, y, **kwargs)

    def try_to_move(self, dx=0, dy=0):
        player_x = state.player.x
        player_y = state.player.y
        new_x = player_x + dx
        new_y = player_y + dy
        if new_x < 0 or new_y < 0 or new_x >= self.width or new_y >= self.height:
            message.error("How'd you get over there? You cannot exit the map!", flip=True)
            return False
        
        new_cell = self.cells[new_y][new_x]
        new_cell.on_use()
        
        if new_cell.passable and (new_y == 0 or new_y >= self.height-1):
            #room warp time
            self.clear_player()
            if new_y <= 0:
                state.player.y = self.prev_room.height - 2
                explore.set_room(self.prev_room)
            else:
                state.player.y = 1
                explore.set_room(self.next_room)
            return


        if not new_cell.passable:
            if not new_cell.special:
                message.error("There is something in the way.")
            return False
        self.move_player(new_x, new_y)
        sanity.step()

    def clear_player(self):
        #restore the old graphic where the player was
        fg, bg, char = self.cells[state.player.y][state.player.x].char
        self.set_at(state.player.x, state.player.y, bg=bg, fg=fg, char=char)
        
    def move_player(self, new_x, new_y):
        self.clear_player()

        #move the player
        state.player.x = new_x
        state.player.y = new_y

        #draw the player on
        self.set_at(state.player.x, state.player.y, fg=colors.LIGHTMAGENTA, char='@')

    def update_bg(self):
        bg_color = sanity.bg_color(self.mode)
        for cell in self.each_cell():
            if cell.volatile_bg:
                    self.set_at(cell.x,cell.y, bg=bg_color)

    def each_cell(self):
        for row in self.cells:
            for cell in row:
                yield cell

    def activate(self):
        self.move_player(state.player.x, state.player.y)
        self.update_bg()
        if self.on_activate:
            self.on_activate(self)

found_blue = False
def tutorial_onactivate(self):
    global found_blue
    if 'red key' in state.inventory:
        state.enable_shudder = True

    if 'blue key' in state.inventory and not found_blue:
        found_blue = True
        state.enable_shudder = True
        for cell in self.each_cell():
            if cell.special == 'staircase':
                cell.clear()
                sanity.shudder(nomsg=True)
                time.sleep(0.02)
                log.debug("blam")
        message.add('The stairs out have disappeared!\nYou are trapped!\n')
        state.player.lose_san(5)


layout = dict(
    map='tutorial',
    shudder_map='tutorial_shudder',
    on_activate=tutorial_onactivate,
    next=dict(
        map='room1'
    )
)

import explore
