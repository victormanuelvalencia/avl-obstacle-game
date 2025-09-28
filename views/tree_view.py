# views/tree_view.py
import sys
import time
import pygame
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import networkx as nx


class TreeView:
    TREE_WIDTH = 500
    HEIGHT = 800
    tree_y_pos = 20
    def __init__(self, avl_controller, game_width):
        self.avl_controller = avl_controller
        self.game_width = game_width
        self.screen = None
        self.tree_surface = None
        self.dirty = True  # 🚩 redibujar árbol cuando cambie
        self.buttons = self._create_buttons()
        self.highlight_nodes = []  # nodos a resaltar en recorrido (formato "(x,y)")
        self.animation_delay_ms = 500  # ms entre pasos de la animación

        # 🔹 Inputs gráficos
        self.inputs = self._create_inputs()
        self.active_input = None  # cuál está editando el usuario
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def set_screen(self, screen):
        self.screen = screen

    def mark_dirty(self):
        self.dirty = True

    # ------------------------
    # Inputs y botón de rango
    # ------------------------
    def _create_inputs(self):
        btn_width, btn_height = 120, 30
        x = self.game_width + 350
        y_pos = self.HEIGHT - 325
        spacing = 40

        inputs = {
            "x_min": {"rect": pygame.Rect(x, y_pos, btn_width, btn_height), "text": ""},
            "x_max": {"rect": pygame.Rect(x, y_pos + spacing, btn_width, btn_height), "text": ""},
            "y_min": {"rect": pygame.Rect(x, y_pos + 2 * spacing, btn_width, btn_height), "text": ""},
            "y_max": {"rect": pygame.Rect(x, y_pos + 3 * spacing, btn_width, btn_height), "text": ""},
            "Consultar": {"rect": pygame.Rect(x, y_pos + 4 * spacing + 10, btn_width, btn_height)},
        }
        return inputs

    def draw_inputs(self):
        for key, info in self.inputs.items():
            rect = info["rect"]
            if key == "Consultar":
                # Botón
                pygame.draw.rect(self.screen, (180, 220, 180), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                label = self.font.render("Consultar rango", True, (0, 0, 0))
                self.screen.blit(label, (rect.x + 5, rect.y + 5))
            else:
                # Caja de texto
                pygame.draw.rect(self.screen, (255, 255, 255), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                text_surf = self.font.render(info["text"], True, (0, 0, 0))
                self.screen.blit(text_surf, (rect.x + 5, rect.y + 5))

                # Etiqueta pequeña
                label = self.font.render(key, True, (0, 0, 0))
                self.screen.blit(label, (rect.x - 50, rect.y + 5))



    # ------------------------
    # Dibujo del árbol
    # ------------------------
    def create_tree_surface(self):
        root = self.avl_controller.tree.get_root()
        if not root:
            fig, ax = plt.subplots(figsize=(22, 21), dpi=80)
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

            fig, ax = plt.subplots(figsize=(6, 5), dpi=80)

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
            tree_y = self.tree_y_pos
            self.screen.blit(self.tree_surface, (tree_x, tree_y))

        # Dibujar botones e inputs
        self.draw_buttons()
        self.draw_inputs()


    # ------------------------
    # Botones de recorrido
    # ------------------------
    def _create_buttons(self):
        btn_width, btn_height = 120, 30
        x = self.game_width + 20  # alineados a la izquierda del panel
        y_start = self.HEIGHT - 325  # empezar desde abajo
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
        # inputs
        for key, info in self.inputs.items():
            if info["rect"].collidepoint(pos):
                if key == "Consultar":
                    self._run_range_query()
                else:
                    self.active_input = key
                return

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

    def handle_key(self, event):
        if self.active_input is None:
            return
        if event.key == pygame.K_BACKSPACE:
            self.inputs[self.active_input]["text"] = self.inputs[self.active_input]["text"][:-1]
        elif event.key == pygame.K_RETURN:
            self.active_input = None
        else:
            self.inputs[self.active_input]["text"] += event.unicode

    def _run_range_query(self):
        try:
            x_min = int(self.inputs["x_min"]["text"])
            x_max = int(self.inputs["x_max"]["text"])
            y_min = int(self.inputs["y_min"]["text"])
            y_max = int(self.inputs["y_max"]["text"])
        except ValueError:
            print("⚠️ Los valores deben ser enteros")
            return

        # Aquí ya usas tu propio método del controlador
        self.avl_controller.print_range_query(x_min, x_max, y_min, y_max)

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
            tree_y = self.tree_y_pos
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

