import message
import pytality
colors = pytality.colors
import itertools

def no_stairs():
    message.add("stairs?")

bgcolors = itertools.cycle([colors.BLACK, colors.LIGHTGREY])
def bg_color():
    return bgcolors.next()
