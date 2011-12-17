import pytality
import state

import logging
import os
import message
import cell
import sanity

log = logging.getLogger("room")
colors = pytality.colors

class Room:
    def __init__(self, config):
        self.map = config['map']
        self.sane_buffer = self.load(self.map)
        self.build_cells()
        self.move_player(state.player.x, state.player.y)
        self.update_bg()

    def load(self, mapfile):
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
        self.sane_buffer.draw(*args, **kwargs)

    def set_at(self, x, y, **kwargs):
        for buf in [self.sane_buffer]:
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

        if not new_cell.passable:
            if not new_cell.special:
                message.error("There is something in the way.")
            return False
        self.move_player(new_x, new_y)

    def move_player(self, new_x, new_y):
        #restore the old graphic where the player was
        fg, bg, char = self.cells[state.player.y][state.player.x].char
        self.set_at(state.player.x, state.player.y, bg=bg, fg=fg, char=char)
        state.player.x = new_x
        state.player.y = new_y

        #draw the player on
        self.set_at(state.player.x, state.player.y, fg=colors.LIGHTMAGENTA, char='@')

    def update_bg(self):
        bg_color = sanity.bg_color()
        for row in self.cells:
            for cell in row:
                if cell.volatile_bg:
                    self.set_at(cell.x,cell.y, bg=bg_color)
