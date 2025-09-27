import pygame
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import networkx as nx

class TreeView:
    TREE_WIDTH = 500
    HEIGHT = 700

    def __init__(self, avl_controller, game_width):
        self.avl_controller = avl_controller
        self.game_width = game_width
        self.screen = None
        self.tree_surface = None
        self.update_counter = 0
        self.update_interval = 30  # frames

    def set_screen(self, screen):
        self.screen = screen

    def create_tree_surface(self):
        root = self.avl_controller.tree.get_root()
        if not root:
            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)
            ax.text(0.5, 0.5, '🌳 Árbol Vacío', ha='center', va='center', fontsize=20, transform=ax.transAxes, color='gray')
            ax.axis('off')
        else:
            graph = nx.DiGraph()
            self._add_edges(graph, root)
            pos = nx.get_node_attributes(graph, 'pos')
            labels = {n: n for n in graph.nodes()}

            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)
            nx.draw(graph, pos, with_labels=True, labels=labels, node_size=600, node_color="lightblue",
                    font_size=6, font_weight="bold", arrows=False, ax=ax, edge_color='gray', linewidths=2)
            ax.set_title("Árbol AVL", fontsize=10)
            ax.axis('off')

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()
        size = canvas.get_width_height()
        surface = pygame.image.frombuffer(raw_data, size, 'RGBA')
        plt.close(fig)
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

    def draw_tree_area(self):
        pygame.draw.rect(self.screen, (240, 240, 240),
                         (self.game_width, 0, self.TREE_WIDTH, self.HEIGHT))
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.game_width, 0), (self.game_width, self.HEIGHT), 3)

        self.update_counter += 1
        if self.update_counter >= self.update_interval or self.tree_surface is None:
            self.tree_surface = self.create_tree_surface()
            self.update_counter = 0

        if self.tree_surface:
            tree_x = self.game_width + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
            tree_y = (self.HEIGHT - self.tree_surface.get_height()) // 2
            self.screen.blit(self.tree_surface, (tree_x, tree_y))
