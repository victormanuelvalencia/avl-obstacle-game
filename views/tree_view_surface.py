import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import networkx as nx
import pygame

class TreeViewSurface:
    def __init__(self, avl_controller):
        self.avl_controller = avl_controller
        self.surface = None
        self.update_counter = 0
        self.update_interval = 30  # frames

    def create_surface(self):
        root = self.avl_controller.tree.get_root()
        if not root:
            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)
            ax.text(0.5, 0.5, '🌳\nÁrbol Vacío', ha='center', va='center',
                    fontsize=20, transform=ax.transAxes, color='gray')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            fig.patch.set_facecolor('white')
        else:
            graph = nx.DiGraph()
            self._add_edges(graph, root)
            pos = nx.get_node_attributes(graph, 'pos')
            labels = {n: n for n in graph.nodes()}

            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)
            fig.patch.set_facecolor('white')
            nx.draw(graph, pos, with_labels=True, labels=labels,
                    node_size=1200, node_color="lightblue",
                    font_size=8, font_weight="bold", arrows=False, ax=ax,
                    edge_color='gray', linewidths=2, node_shape='o')
            ax.set_title("Estructura del Árbol", fontsize=14, fontweight='bold', pad=20)
            ax.axis('off')

        # Convertir a PyGame Surface
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()
        size = canvas.get_width_height()
        surface = pygame.image.frombuffer(raw_data, size, 'RGBA')
        plt.close(fig)
        self.surface = surface
        return surface

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

    def update_surface(self):
        self.update_counter += 1
        if self.update_counter >= self.update_interval or self.surface is None:
            self.create_surface()
            self.update_counter = 0