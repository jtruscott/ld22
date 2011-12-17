import pytality
import event
import game

import logging
log = logging.getLogger('main')

def main():
    pytality.term.init(width=120,height=60)
    pytality.term.set_title('Dungeon Game    (LD48 #22: Alone)')
    try:
        event.fire('setup')
        game.start()

    except game.GameShutdown:
        pytality.term.reset()
    except KeyboardInterrupt:
        pytality.term.reset()
        raise
    except Exception, e:
        log.exception(e)
        raise

    finally:
        log.debug('Shutting down')
        logging.shutdown()
