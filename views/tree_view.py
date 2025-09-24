class TreeView:
    def __init__(self, controller):
        self.controller = controller

    def plot(self):
        """Método original mantenido para compatibilidad"""
        print("⚠️ Usa IntegratedGameView en lugar de TreeView.plot() para la vista integrada")

        root = self.controller.tree.get_root()
        if not root:
            print("⚠️ El árbol está vacío, nada para graficar.")
            return

        graph = nx.DiGraph()
        self._add_edges(graph, root)

        pos = nx.get_node_attributes(graph, 'pos')
        labels = {n: n for n in graph.nodes()}

        plt.figure(figsize=(8, 6))
        nx.draw(graph, pos, with_labels=True, labels=labels,
                node_size=1200, node_color="skyblue",
                font_size=10, font_weight="bold", arrows=False)
        plt.title("Árbol AVL de Obstáculos")
        plt.show()

    def _add_edges(self, graph, node, x=0, y=0, layer=1):
        if not node:
            return

        node_id = f"({node.get_x1()},{node.get_y1()})"
        graph.add_node(node_id, pos=(x, y))

        if node.get_left():
            left_id = f"({node.get_left().get_x1()},{node.get_left().get_y1()})"
            graph.add_edge(node_id, left_id)
            self._add_edges(graph, node.get_left(), x - 1 / layer, y - 1, layer + 1)

        if node.get_right():
            right_id = f"({node.get_right().get_x1()},{node.get_right().get_y1()})"
            graph.add_edge(node_id, right_id)
            self._add_edges(graph, node.get_right(), x + 1 / layer, y - 1, layer + 1)