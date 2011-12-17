import event
import state

import logging
log = logging.getLogger('game')

class GameShutdown(Exception):
    pass

def start():
    log.debug("Game starting")

    lastmode = None
    while True:
        if lastmode != state.mode:
            lastmode = state.mode
            event.fire('%s.start' % lastmode)

        event.fire('%s.draw' % state.mode)
        event.fire('%s.run' % state.mode)
