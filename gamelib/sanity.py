import message
import pytality
import state
colors = pytality.colors
import itertools

import time #thisll need a hack for silverlight

import logging
log = logging.getLogger('sanity')

def no_stairs():
    message.add("stairs?")

def shudder_message():
    message.add("What was that?")


def step():
    state.player.steps += 1
    if state.player.steps % 50 == 0:
        shudder()

def bg_color(mode):
    if mode == 'sane':
        return colors.BLACK
    if mode == 'shudder':
        return colors.LIGHTGREY

def shudder(nomsg=False):
    if not state.enable_shudder:
        log.debug("can't shudder")
        return
        
    import explore
    room = explore.g.current_room
    if room.shudder_buffer:
        room.mode = 'shudder'
        room.update_bg()
        explore.g.buffer.draw()
        pytality.term.flip()
        time.sleep(0.04)

        room.mode = 'sane'
        room.update_bg()
        explore.g.buffer.draw()
        pytality.term.flip()
        if not nomsg:
            shudder_message()
            state.player.lose_san(1)

