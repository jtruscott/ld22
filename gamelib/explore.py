import pytality
import event
import state
import player
import room
import message
import sanity

class g:
    #items go here
    pass

@event.on('explore.start')
def explore_start():
    state.player = player.Ranger()
    state.player.x = 40
    state.player.y = 6

    pytality.term.clear()
    x = state.width - 80
    g.buffer = pytality.buffer.Buffer(x=x, width=state.width - x, height=0)

    g.text = pytality.buffer.PlainText(
        "YOU ARE A %s" % state.player.title,
        x=0, y=state.height/2, center_to=g.buffer.width,
        fg=pytality.colors.BLUE
    )

    g.stat_bar = pytality.buffer.Box(
        width=g.buffer.width, height=6, padding_x=2, padding_y=1,
        draw_left=False, draw_top=False,
        children = [
            pytality.buffer.RichText("<GREEN>Health:</>  %s", y=0),
            pytality.buffer.RichText("<YELLOW>Stamina:</> %s", y=2)
        ]
    )
    g.room_container = pytality.buffer.Buffer(x=0, width=g.buffer.width, height=state.height - g.stat_bar.height, y=g.stat_bar.height)
    g.buffer.children += [g.text, g.stat_bar, g.room_container]


    for i in range(10):
        message.add("hoo boy!")

    set_room(room.Room(room.layout))

def set_room(r):
    g.current_room = r
    g.room_container.children = [g.current_room]
    g.current_room.activate()

def update_stat_bar():
    g.stat_bar.children[0].format(chr(0xDB) * state.player.hp)
    g.stat_bar.children[1].format(chr(0xDB) * state.player.stamina)


@event.on('explore.draw')
def explore_draw():
    update_stat_bar()

    g.buffer.draw()
    message.box.draw()
    pytality.term.flip()

@event.on('explore.run')
def explore_run():
    k = pytality.term.getkey()
    if k == 'home':
        message.scroll(home=True)
    elif k == 'pgup':
        message.scroll(delta=-1)
    elif k == 'pgdn':
        message.scroll(delta=1)
    elif k == 'end':
        message.scroll(end=True)

    elif k == 'up':
        g.current_room.try_to_move(dy=-1)
    elif k == 'down':
        g.current_room.try_to_move(dy=1)
    elif k == 'left':
        g.current_room.try_to_move(dx=-1)
    elif k == 'right':
        g.current_room.try_to_move(dx=1)
    
    #debug keys
    elif k == 's':
        sanity.shudder()
    elif k == 'b':
        state.inventory.append("blue key")
    return

