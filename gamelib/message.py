import pytality
import state

box = pytality.buffer.MessageBox(x=0, y=0, width=state.width - 80, height=state.height)

def add(msg, scroll=True, flip=False):
    box.add(msg, scroll=scroll)
    if flip:
        box.draw()
        pytality.term.flip()

def error(msg, **kwargs):
    msg = '<RED>%s' % msg
    add(msg, **kwargs)

def scroll(**kwargs):
    box.scroll(**kwargs)
    box.draw()
    pytality.term.flip()
