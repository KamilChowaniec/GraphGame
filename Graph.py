class Graph:

    def __init__(self):
        self.graph_dict = dict()
        self.free = 0
        self.edges = []

    def getNeighbors(self, vertex):
        if vertex in self.graph_dict:
            return self.graph_dict[vertex][1]
        return None

    def __setitem__(self, key, value):
        if key in self.graph_dict:
            self.graph_dict[key][0] = value

    def __getitem__(self, item):
        if item in self.graph_dict:
            return self.graph_dict[item][0]
        return None

    def joinVertices(self, vertex1, vertex2):
        if vertex1 == vertex2 or vertex1 not in self.graph_dict or vertex2 not in self.graph_dict:
            return
        self.graph_dict[vertex1][1].add(vertex2)
        self.graph_dict[vertex2][1].add(vertex1)
        self.edges += [[vertex1, vertex2]]

    def addVertex(self, value=0):
        self.graph_dict[self.free] = [value, set()]
        self.free += 1
        return self.free - 1

    def delVertex(self, vertex):
        if vertex in self.graph_dict:
            for v in self.graph_dict[vertex][1]:
                self.graph_dict[v][1].discard(vertex)
            self.graph_dict.pop(vertex)
            edges = []
            for edge in self.edges:
                if vertex in edge:
                    edges.append(edge)
            for e in edges:
                self.edges.remove(e)

    def disconnectVertices(self, vertex1, vertex2):
        if vertex1 in self.graph_dict and vertex2 in self.graph_dict:
            if [vertex1, vertex2] in self.edges:
                self.edges.remove([vertex1, vertex2])
            elif [vertex2, vertex1] in self.edges:
                self.edges.remove([vertex2, vertex1])
            self.graph_dict[vertex1][1].discard(vertex2)
            self.graph_dict[vertex2][1].discard(vertex1)

    def getEdges(self):
        return self.edges

    def getEdges2(self):
        edges = set()
        for v in self.graph_dict:
            for v2 in self.graph_dict[v][1]:
                edges.add(frozenset([v, v2]))
        return [list(v) for v in edges]

    def clear(self):
        self.graph_dict.clear()

    def __iter__(self):
        return self.graph_dict.__iter__()
