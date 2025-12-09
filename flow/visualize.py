from curses import wrapper
import curses
import time

from collections import defaultdict

from graph import *
from boards import *
from cbs import *

class path_window():

    def __init__(self, height, width,  begin_y, begin_x, padding=0):
        """
        New window object. Width and height are graph dimensions
        """

        self.begin_x = begin_x
        self.begin_y = begin_y

        self.padding = padding
        self.width = width
        self.height = height

        self.win = curses.newwin(self.height, self.width, self.begin_x, self.begin_y)

    def draw_line(self, n, line):

        self.win.addstr(n,0, '{}'.format(line))

    def draw_graph(self, graph):
        """
        Graph object (i only use width and list of nodes)
        """

        for i in range (graph.height):
            self.draw_line(
                    i,
                    graph.display_one_line_graph(i, self.padding)
                )

class drawer():

    def __init__(self, graph, stdscr):

        # Graph
        self.graph = graph
        self.graph_width = self.graph.width
        self.graph_height = self.graph.height

        # Padding
        self.window_padding = 5
        self.character_padding = 1
        self.window_margin = 30     # Space from edge

        # Dimensions
        # TODO: Customize
        #self.start_x = int((self.screen_width -  self.row_width * self.padding) // 2)
        #self.start_y = int(self.screen_height * 0.2)

        self.stdscr = stdscr
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        #self.screen_height = 34
        #self.screen_width = 157

        # Windows
        self.windows = {}
        self.window_width = self.graph_width * (self.character_padding + 1) - self.character_padding
        self.window_height = self.graph.height + 1

        rest_space_window_margin = (self.screen_width - 2 * self.window_margin) % (self.window_width + self.window_padding)
        self.start_x = self.window_margin + (rest_space_window_margin // 2)
        self.end_x = self.screen_width - self.window_margin - (rest_space_window_margin // 2)

        self.max_windows_per_row = (self.screen_width - 2 * self.window_margin) // (self.window_width + 2 * self.window_padding)

        """
        print (self.start_x,
               self.end_x,
               self.max_windows_per_row,
               rest_space_window_margin)
        """

        # TODO: Create drawer in CBS?
        #for i, flow in enumerate(flows):
        #    self.windows[flow.state] = path_window(
        #            self.window_height,
        #            self.window_width,
        #            self.start_x + ((i % self.max_windows_per_row) * (self.window_width + 2 * self.window_padding)),
        #            (i // self.max_windows_per_row) * (self.window_height + self.window_padding - 2),
        #            self.character_padding
        #        )

    def draw(self):
        self.stdscr.addstr(0,0, "HHHEHE")

"""
g = graph(less_hard)
cbs = CBS_solver(g)

dd = drawer(g, "ss", cbs.flows)
"""
