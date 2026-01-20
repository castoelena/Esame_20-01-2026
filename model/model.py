import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()

        self._nodes = []
        self._edges = []
        self._artists_min_albums = []
        self._mappa_id = {}

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, n_alb):
        self._artists_min_albums = DAO.get_artists_albums(n_alb)

    def build_graph(self):
        self._graph.clear()

        for a in self._artists_min_albums:
            self._nodes.append(a)

        for a in self._artists_min_albums:
            self._mappa_id[a.id] = a

        self._graph.add_nodes_from(self._nodes)

        genres = DAO.get_stesso_genere()
        for a1, a2, genre in genres:
            self._edges.append((a1, a2, genre))
        self._graph.add_weighted_edges_from(self._edges)

    def get_nodes(self):
        return self._graph.nodes()
    def get_num_nodes(self):
        return self._graph.number_of_nodes()
    def get_edges(self):
        return list(self._graph.edges(data=True))
    def get_num_edges(self):
        return self._graph.number_of_edges()


