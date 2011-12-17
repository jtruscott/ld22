import pytality
import event
import state
import player
class g:
    buffer = None

@event.on('explore.start')
def explore_start():
    g.buffer = pytality.buffer.Buffer(width=0, height=0)
    g.text = pytality.buffer.PlainText(
        "YOU ARE A %s" % state.player.title,
        x=0, y=state.height/2, center_to=state.width,
    )
    g.buffer.children.append(g.text)

@event.on('explore.draw')
def explore_draw():
    g.buffer.draw()
    pytality.term.flip()

@event.on('explore.run')
def explore_run():
    k = pytality.term.getkey()
    return

