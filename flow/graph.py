from collections import defaultdict
import math

class node():

    def __init__(self, y, x, state):

        self.state = state

        self.y = y
        self.x = x

        self.f = 0 # Total cost
        self.g = 0 # Cost to node from start
        self.h = 0 # Heuristic cost estimate

        self.neighbors = []
        self.parent = None

    def __repr__(self):
        return f"{self.state}"
        #return f"Node at ({self.y},{self.x})"

    def find_neighbors(self, d, delete = False):
        """
        Given dictionary of nodes that exist, adds or deletes neighbors
        """

        search = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        ]

        for s in search:

            new_y = self.y + s[1]
            new_x = self.x + s[0]

            res = d.get((new_y, new_x))

            if res:

                if delete == False:
                    # TODO: Make not ugly and if in check is needed
                    if res.state != "*" and res not in self.neighbors:
                        self.neighbors.append(res)

                else:
                    try:
                        res.neighbors.remove(self)
                    except:
                        None

class graph():

    def __init__(self, graph):
        """
        Given nested list like, f.ex.
        Where . is an empty square and * is not in use
        (I think passing a tuple/list where [0] is the length of each row and [1] being the flattened data. Easier to work with, and i can later make something to convert this below to said flattened structure)

        [
            3,
            ["A", ".", "A","*", "B", ".","*", "*", "B"],
        ]

        Make node objects with correct neighbors and  states
        Will also store location of terminals (any other symbol than . or *)
        """

        self.width = graph[0]
        self.height = math.ceil(len(graph[1]) / self.width)
        self.nodes = []
        self.terminals = defaultdict(list)

        # Make nodes if square is in play
        for i,n in enumerate(graph[1]):

            y = i // self.width
            x = i % self.width

            new_node = node(y, x, n)
            self.nodes.append(new_node)

            if n != "." and n != "*":
                self.terminals[n].append(new_node)

        # Dictionary on coord tuple
        self.node_locations = {
                (n.y, n.x) : n for n in self.nodes
            }

        self.add_neighbors()

        # By concatinating the lists not appending (make one long list not nested list)
        self.all_terminals = []
        for t in self.terminals.values():
            self.all_terminals += t

        # Non terminals and * nodes
        self.usable_nodes = [x for x in self.nodes if x not in self.all_terminals and x.state != "*"]

    def reset_node_states(self, nodes=None):
        """
        Sets states to default symbol ".". keeps terminals same state

        Warning: If nodes[] contains terminal it will overwrite

        TODO perhaps make set node state
        """

        if nodes == None:
            nodes = self.usable_nodes

        # TODO is this safe?
        for node in nodes:
            node.state = "."

    def display_one_line_graph(self, n, padding=1):

        # Adds padding width between each char
        line = (padding*" ").join([
                node.state for node in
                self.nodes[self.width*n:self.width*(n+1)]
            ])

        return line

    def display_graph(self, paths_alone=False):

        for i in range(self.height):
            print (self.display_one_line_graph(i))

    def set_neighbors(self, conditions):
        """
        Attempts to remove all neighbors from given nodes
        Lets terminals have a local environment

        I.e. it is a node, context comes from what calls function
        """

        for c in conditions:

            c.find_neighbors(
                    self.node_locations,
                    delete = True
                )
            c.neighbors = []

    def reset_astar_values(self, nodes=None):
        """
        Reset attr. to none and inf
        Unsure if this is best practice, but seeing as im going to have to run a* one million times...
        """

        if nodes == None:
            nodes = self.nodes

        for n in nodes:
            n.f = float("inf")
            n.g = float("inf")
            n.h = float("inf")

            n.parent = None

    def add_neighbors(self, nodes = None):

        # TODO: If performance issues, this function might be part of it
        # TODO: Solve how to re-add all restrictions
        checked = []

        if not nodes:
            nodes = self.nodes

        for n in nodes:

            checked.append(n)

            n.find_neighbors(
                    self.node_locations
                )
            for neigh in n.neighbors:

                if neigh in checked:
                    continue

                # TODO: Call find neighbors on just n?
                neigh.find_neighbors(
                    self.node_locations
                )
