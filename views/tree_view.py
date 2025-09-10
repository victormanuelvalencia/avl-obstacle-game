import matplotlib.pyplot as plt
import networkx as nx  # Para manejar nodos y edges más fácil

class TreeView:
    def __init__(self, controller):
        self.controller = controller

    def _add_edges(self, graph, node, pos, x=0, y=0, layer=1):
        """
        Construye recursivamente los nodos y aristas para el grafo.
        """
        if not node:
            return

        # Identificador único (coordenadas del obstáculo)
        node_id = f"({node.get_x_min()},{node.get_y_min()})"

        graph.add_node(node_id, pos=(x, y))

        # Hijo izquierdo
        if node.get_left():
            left_id = f"({node.get_left().get_x_min()},{node.get_left().get_y_min()})"
            graph.add_edge(node_id, left_id)
            self._add_edges(graph, node.get_left(), pos, x - 1/layer, y - 1, layer + 1)

        # Hijo derecho
        if node.get_right():
            right_id = f"({node.get_right().get_x_min()},{node.get_right().get_y_min()})"
            graph.add_edge(node_id, right_id)
            self._add_edges(graph, node.get_right(), pos, x + 1/layer, y - 1, layer + 1)

    def plot(self):
        """
        Dibuja el árbol AVL usando matplotlib y networkx.
        """
        root = self.controller.model.get_root()
        if not root:
            print("⚠️ El árbol está vacío, nada para graficar.")
            return

        graph = nx.DiGraph()
        pos = {}

        self._add_edges(graph, root, pos)

        node_labels = {n: n for n in graph.nodes()}
        pos = nx.get_node_attributes(graph, 'pos')

        plt.figure(figsize=(8, 6))
        nx.draw(graph, pos, with_labels=True, labels=node_labels,
                node_size=1200, node_color="skyblue",
                font_size=10, font_weight="bold", arrows=False)
        plt.title("Árbol AVL de Obstáculos")
        plt.show()
