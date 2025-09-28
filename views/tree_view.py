# views/tree_view.py
import sys
import time
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
        self.dirty = True  # 🚩 redibujar árbol cuando cambie
        self.buttons = self._create_buttons()
        self.highlight_nodes = []  # nodos a resaltar en recorrido (formato "(x,y)")
        self.animation_delay_ms = 500  # ms entre pasos de la animación

    def set_screen(self, screen):
        self.screen = screen

    def mark_dirty(self):
        self.dirty = True

    # ------------------------
    # Dibujo del árbol
    # ------------------------
    def create_tree_surface(self):
        root = self.avl_controller.tree.get_root()
        if not root:
            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=80)
            ax.text(0.5, 0.5, '🌳 Árbol Vacío', ha='center', va='center',
                    fontsize=20, transform=ax.transAxes, color='gray')
            ax.axis('off')
        else:
            graph = nx.DiGraph()
            self._add_edges(graph, root)
            root_id = f"({root.get_x1()},{root.get_y1()})"
            # layout jerárquico (sin pygraphviz)
            pos = self.hierarchy_pos(graph, root=root_id)

            labels = {n: n for n in graph.nodes()}

            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=80)

            # Colorear nodos resaltados en rojo (si ya fueron visitados)
            node_colors = [
                "red" if n in self.highlight_nodes else "lightblue"
                for n in graph.nodes()
            ]

            nx.draw(
                graph, pos, with_labels=True, labels=labels,
                node_size=600, node_color=node_colors,
                font_size=6, font_weight="bold", arrows=False,
                ax=ax, edge_color='gray', linewidths=1
            )
            ax.set_title("Árbol AVL", fontsize=10)
            ax.axis('off')

        # matplotlib -> surface pygame
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()
        size = canvas.get_width_height()
        surface = pygame.image.frombuffer(raw_data, size, 'RGBA')
        plt.close(fig)
        return surface

    def _add_edges(self, graph, node):
        if not node:
            return
        node_id = f"({node.get_x1()},{node.get_y1()})"
        graph.add_node(node_id)
        if node.get_left():
            left_id = f"({node.get_left().get_x1()},{node.get_left().get_y1()})"
            graph.add_edge(node_id, left_id)
            self._add_edges(graph, node.get_left())
        if node.get_right():
            right_id = f"({node.get_right().get_x1()},{node.get_right().get_y1()})"
            graph.add_edge(node_id, right_id)
            self._add_edges(graph, node.get_right())

    def draw_tree_area(self):
        # Fondo del área del árbol
        pygame.draw.rect(self.screen, (240, 240, 240),
                         (self.game_width, 0, self.TREE_WIDTH, self.HEIGHT))
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.game_width, 0), (self.game_width, self.HEIGHT), 3)

        if self.dirty or self.tree_surface is None:
            self.tree_surface = self.create_tree_surface()
            self.dirty = False

        if self.tree_surface:
            tree_x = self.game_width + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
            tree_y = 50
            self.screen.blit(self.tree_surface, (tree_x, tree_y))

        # Dibujar botones
        self.draw_buttons()

    # ------------------------
    # Botones de recorrido
    # ------------------------
    def _create_buttons(self):
        btn_width, btn_height = 120, 30
        x = self.game_width + (self.TREE_WIDTH - btn_width) // 2
        y_start = 10
        spacing = 5
        buttons = {
            "Inorden": pygame.Rect(x, y_start, btn_width, btn_height),
            "Preorden": pygame.Rect(x, y_start + btn_height + spacing, btn_width, btn_height),
            "Postorden": pygame.Rect(x, y_start + 2 * (btn_height + spacing), btn_width, btn_height),
        }
        return buttons

    def draw_buttons(self):
        font = pygame.font.SysFont("Arial", 16, bold=True)
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            label = font.render(text, True, (0, 0, 0))
            self.screen.blit(label, (rect.x + 10, rect.y + 5))

    def handle_click(self, pos):
        for text, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if text == "Inorden":
                    recorrido = self.avl_controller.inorder()
                elif text == "Preorden":
                    recorrido = self.avl_controller.preorder()
                else:
                    recorrido = self.avl_controller.postorder()

                # ejecutar animación (recorrido puede ser lista de strings o de objetos)
                self.animate_traversal(recorrido)

    # ------------------------
    # Animación de recorrido
    # ------------------------
    def animate_traversal(self, nodes):
        """
        nodes: lista devuelta por AVLTreeController (ej: ["(10, 20)", "(5, 30)", ...])
        Normalizamos cada item a la etiqueta que usamos en el grafo: "(x,y)" (sin espacios).
        """
        # Normalizar nodos del recorrido al formato "(x,y)"
        normalized = []
        for item in nodes:
            if isinstance(item, str):
                nid = item.replace(" ", "")  # quitar espacios: "(x, y)" -> "(x,y)"
            else:
                # si vienen como objetos de nodo
                try:
                    nid = f"({item.get_x1()},{item.get_y1()})"
                except Exception:
                    nid = str(item).replace(" ", "")
            normalized.append(nid)

        # Animar (acumular resaltados y mostrar paso a paso)
        for nid in normalized:
            if nid not in self.highlight_nodes:
                self.highlight_nodes.append(nid)

            # Forzamos regenerar surface con nodos resaltados
            self.dirty = True
            self.tree_surface = self.create_tree_surface()

            # blit inmediato (misma lógica que draw_tree_area, pero sin recrear surface otra vez)
            tree_x = self.game_width + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
            tree_y = 50
            # Nota: no limpiamos todo el fondo del juego aquí, solo dibujamos el panel del árbol
            self.screen.blit(self.tree_surface, (tree_x, tree_y))
            self.draw_buttons()
            pygame.display.flip()

            # procesar eventos (permitir cerrar la ventana durante la animación)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # opcional: si quieres manejar clicks durante animación, puedes:
                # elif ev.type == pygame.MOUSEBUTTONDOWN:
                #     self.handle_click(ev.pos)

            # esperar el tiempo definido en ms
            pygame.time.wait(int(self.animation_delay_ms))

        # Al final puedes limpiar los resaltados (si prefieres que desaparezcan)
        # self.highlight_nodes.clear()
        # self.dirty = True

    # ------------------------
    # Layout jerárquico sin pygraphviz
    # ------------------------
    def hierarchy_pos(self, G, root=None, width=1., vert_gap=0.2,
                      vert_loc=0, xcenter=0.5, pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        neighbors = list(G.neighbors(root))
        if parent is not None and parent in neighbors:
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / len(neighbors)
            nextx = xcenter - width / 2 - dx / 2
            for neighbor in neighbors:
                nextx += dx
                pos = self.hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap,
                                         vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                         pos=pos, parent=root)
        return pos


"""
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
        print("Marcar que el árbol cambió y debe regenerarse")
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