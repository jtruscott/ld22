import pytality
import state

import logging
import os
log = logging.getLogger("room")

class Room:
    def __init__(self, map):
        self.map = map
        self.sane_buffer = self.load(map)

    def load(self, mapfile):
        full_path = os.path.join('data', mapfile)
        buf = pytality.ansi.read_to_buffer(open(full_path), crop=True)
        return buf

    def draw(self, *args, **kwargs):
        self.sane_buffer.draw(*args, **kwargs)
