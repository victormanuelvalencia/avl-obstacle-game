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
        x = self.game_width + 20  # alineados a la izquierda del panel
        y_start = self.HEIGHT - 3 * (btn_height + 10)  # empezar desde abajo
        spacing = 10
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
                try:
                    nid = f"({item.get_x1()},{item.get_y1()})"
                except Exception:
                    nid = str(item).replace(" ", "")
            normalized.append(nid)

        # Animar paso a paso
        for nid in normalized:
            if nid not in self.highlight_nodes:
                self.highlight_nodes.append(nid)

            self.dirty = True
            self.tree_surface = self.create_tree_surface()

            tree_x = self.game_width + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
            tree_y = 50
            self.screen.blit(self.tree_surface, (tree_x, tree_y))
            self.draw_buttons()
            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.wait(int(self.animation_delay_ms))

        # ✅ Al final del recorrido, limpiar resaltados y redibujar
        self.highlight_nodes.clear()
        self.dirty = True
        self.tree_surface = self.create_tree_surface()
        tree_x = self.game_width + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
        tree_y = 50
        self.screen.blit(self.tree_surface, (tree_x, tree_y))
        self.draw_buttons()
        pygame.display.flip()

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

