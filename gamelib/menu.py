import pytality
import event
import state
import player
class main_menu:
    buffer = None

@event.on('main_menu.start')
def main_menu_setup():
    main_menu.buffer = pytality.buffer.Buffer(width=0, height=0)
    main_menu.buffer.children.append(pytality.buffer.PlainText(
        "(F) FIGHTER             (R) RANGER             (W) WIZARD",
        x=0, y=state.height/2, center_to=state.width,
    ))

@event.on('main_menu.draw')
def main_menu_draw():
    main_menu.buffer.draw()
    pytality.term.flip()

@event.on('main_menu.run')
def main_menu_run():
    k = pytality.term.getkey()
    if not k:
        return
        
    k = k.lower()
    if k in ('f', 'r', 'w'):
        if k == 'f':
            state.player = player.Fighter()
        elif k == 'r':
            state.player = player.Ranger()
        else:
            state.player = player.Wizard()

        state.mode = 'explore'
        return

