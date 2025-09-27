
# views/tree_view.py
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
        self.dirty = True  # 🚩 necesita redibujarse al inicio

    def set_screen(self, screen):
        self.screen = screen

    def mark_dirty(self):
        """Marcar que el árbol cambió y debe regenerarse"""
        self.dirty = True

    def create_tree_surface(self):
        root = self.avl_controller.tree.get_root()
        if not root:
            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=80)  # 🔧 menos dpi para más velocidad
            ax.text(0.5, 0.5, '🌳 Árbol Vacío', ha='center', va='center',
                    fontsize=20, transform=ax.transAxes, color='gray')
            ax.axis('off')
        else:
            graph = nx.DiGraph()
            self._add_edges(graph, root)
            pos = nx.get_node_attributes(graph, 'pos')
            labels = {n: n for n in graph.nodes()}

            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=80)
            nx.draw(
                graph, pos, with_labels=True, labels=labels,
                node_size=600, node_color="lightblue",
                font_size=6, font_weight="bold", arrows=False,
                ax=ax, edge_color='gray', linewidths=1
            )
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

        # ✅ solo regenerar si hay cambios
        if self.dirty or self.tree_surface is None:
            self.tree_surface = self.create_tree_surface()
            self.dirty = False

        if self.tree_surface:
            tree_x = self.game_width + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
            tree_y = (self.HEIGHT - self.tree_surface.get_height()) // 2
            self.screen.blit(self.tree_surface, (tree_x, tree_y))

"""
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
            ax.text(0.5, 0.5, '🌳 Árbol Vacío', ha='center', va='center', fontsize=20,
                    transform=ax.transAxes, color='gray')
            ax.axis('off')
        else:
            graph = nx.DiGraph()
            self._add_edges(graph, root)
            pos = nx.get_node_attributes(graph, 'pos')
            labels = {n: n for n in graph.nodes()}

            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)
            nx.draw(graph, pos, with_labels=True, labels=labels, node_size=400, node_color="lightblue",
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
        node_id = f"{node.get_x1()}"  # solo x
        graph.add_node(node_id, pos=(x, y))
        if node.get_left():
            left_id = f"{node.get_left().get_x1()}"  # solo x
            graph.add_edge(node_id, left_id)
            self._add_edges(graph, node.get_left(), x - 1 / layer, y - 1, layer + 1)
        if node.get_right():
            right_id = f"{node.get_right().get_x1()}"  # solo x
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
            tree_y = 10
            self.screen.blit(self.tree_surface, (tree_x, tree_y))

        self.draw_traversals()

    def get_traversals(self):
        inorder = " ".join(self.avl_controller.inorder())   # sin comas
        preorder = " ".join(self.avl_controller.preorder()) # sin comas
        postorder = " ".join(self.avl_controller.postorder()) # sin comas
        return inorder, preorder, postorder

    def draw_traversals(self):
        font = pygame.font.SysFont("Arial", 16)
        inorder, preorder, postorder = self.get_traversals()

        x = self.game_width + 10
        max_width = self.TREE_WIDTH - 20

        traversals = [
            ("Inorder", inorder),
            ("Preorder", preorder),
            ("Postorder", postorder),
        ]

        if self.tree_surface:
            start_y = self.tree_surface.get_height() + 30
        else:
            start_y = 20

        y = start_y
        for title, traversal in traversals:
            self.screen.blit(font.render(f"{title}:", True, (0, 0, 0)), (x, y))
            y += 20

            lines = self.wrap_text(traversal, font, max_width)
            for line in lines:
                self.screen.blit(font.render(line, True, (0, 0, 0)), (x + 15, y))
                y += 20

            y += 8

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")  # dividir por espacio
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
"""