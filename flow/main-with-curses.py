from boards import *
from cbs import *
from visualize import *

from curses import wrapper

#cbs.solve_puzzle()

# TODO: Call solver with curses

def main(stdscr, with_curses):

    g = graph(less_hard)
    d = drawer(g, stdscr)

    cbs = CBS_solver(g, True, stdscr, d)

    stdscr.clear()

    stdscr.refresh()

    #dd.ww.win.addstr(0,0, 'HH')
    #dd.ww.draw_graph(g)
    for window in d.windows.values():
        window.draw_graph(g)
        window.win.refresh()

    #stdscr.addstr(10,0, '{}'.format(stdscr.getmaxyx()))
    #stdscr.addstr(2,0, '{}'.format(dd.ww.height))

    stdscr.getkey()

wrapper(main, with_curses=True)
#print (" ".join(g.display_one_line_graph(2)))
#print(g.display_one_line_graph(2, 2)[-1])
