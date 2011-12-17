import logging
log = logging.getLogger('game')

class GameShutdown(Exception):
    pass
    
import event
def start():
    log.debug("Game starting")
