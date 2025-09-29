import sys
import time
import pygame
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import networkx as nx

class TreeView:
    """
    Responsible for rendering the AVL tree and providing interactive buttons
    and input fields for range queries and traversal animations.

    Attributes:
        TREE_WIDTH (int): Width of the tree panel.
        HEIGHT (int): Height of the tree panel.
        tree_y_pos (int): Vertical position offset for the tree rendering.
        avl_controller (AVLTreeController): Controller managing the AVL tree.
        game_width (int): Width of the game area, used to align the tree panel.
        screen (pygame.Surface): Pygame surface to draw on.
        tree_surface (pygame.Surface): Surface with the rendered tree image.
        dirty (bool): Flag indicating that the tree needs to be redrawn.
        buttons (dict): Rects for traversal buttons (Inorder, Preorder, Postorder).
        highlight_nodes (list): Nodes to highlight during traversal animation.
        animation_delay_ms (int): Delay between animation steps in milliseconds.
        inputs (dict): Rects and text for graphical input fields.
        active_input (str): Currently active input field.
        font (pygame.font.Font): Font used for rendering text.
    """

    TREE_WIDTH = 500
    HEIGHT = 800
    tree_y_pos = 20

    def __init__(self, avl_controller, game_width):
        self.avl_controller = avl_controller
        self.game_width = game_width
        self.screen = None
        self.tree_surface = None
        self.dirty = True  # Flag to redraw tree when it changes
        self.buttons = self._create_buttons()
        self.highlight_nodes = []  # Nodes to highlight during traversal (format "(x,y)")
        self.animation_delay_ms = 500  # milliseconds between animation steps

        # Graphical input fields
        self.inputs = self._create_inputs()
        self.active_input = None  # Currently edited input
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def set_screen(self, screen):
        """Sets the Pygame surface for rendering."""
        self.screen = screen

    def mark_dirty(self):
        """Marks the tree as needing a redraw."""
        self.dirty = True

    def _create_inputs(self):
        """
        Creates input fields for range queries and the 'Consult' button.
        """
        btn_width, btn_height = 120, 30
        x = self.game_width + 350
        y_pos = self.HEIGHT - 325
        spacing = 40

        inputs = {
            "x_min": {"rect": pygame.Rect(x, y_pos, btn_width, btn_height), "text": ""},
            "x_max": {"rect": pygame.Rect(x, y_pos + spacing, btn_width, btn_height), "text": ""},
            "y_min": {"rect": pygame.Rect(x, y_pos + 2 * spacing, btn_width, btn_height), "text": ""},
            "y_max": {"rect": pygame.Rect(x, y_pos + 3 * spacing, btn_width, btn_height), "text": ""},
            "Consult": {"rect": pygame.Rect(x, y_pos + 4 * spacing + 10, btn_width + 3, btn_height)},
        }
        return inputs

    def draw_inputs(self):
        """Draws input fields and the 'Consult' button on the screen."""
        for key, info in self.inputs.items():
            rect = info["rect"]
            if key == "Consult":
                pygame.draw.rect(self.screen, (180, 220, 180), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                label = self.font.render("Consult Range", True, (0, 0, 0))
                self.screen.blit(label, (rect.x + 5, rect.y + 5))
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                text_surf = self.font.render(info["text"], True, (0, 0, 0))
                self.screen.blit(text_surf, (rect.x + 5, rect.y + 5))

                # Small label for the input
                label = self.font.render(key, True, (0, 0, 0))
                self.screen.blit(label, (rect.x - 50, rect.y + 5))

    def create_tree_surface(self):
        """
        Creates a Pygame surface with the current AVL tree drawn using matplotlib.
        Highlights nodes if specified in self.highlight_nodes.
        """
        root = self.avl_controller.tree.get_root()
        if not root:
            # Usar tamaño pequeño para que no expanda toda la ventana
            fig, ax = plt.subplots(figsize=(6, 5), dpi=80)
            ax.text(0.5, 0.5, '🌳 Empty Tree', ha='center', va='center',
                    fontsize=20, transform=ax.transAxes, color='gray')
            ax.axis('off')
        else:
            graph = nx.DiGraph()
            self._add_edges(graph, root)
            root_id = f"({root.get_x1()},{root.get_y1()})"

            pos = self.hierarchy_pos(graph, root=root_id)
            labels = {n: n for n in graph.nodes()}

            fig, ax = plt.subplots(figsize=(6, 5), dpi=80)
            node_colors = ["red" if n in self.highlight_nodes else "lightblue" for n in graph.nodes()]

            nx.draw(
                graph, pos, with_labels=True, labels=labels,
                node_size=600, node_color=node_colors,
                font_size=6, font_weight="bold", arrows=False,
                ax=ax, edge_color='gray', linewidths=1
            )
            ax.set_title("AVL Tree", fontsize=10)
            ax.axis('off')

        # Convert matplotlib figure to Pygame surface
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()
        size = canvas.get_width_height()
        surface = pygame.image.frombuffer(raw_data, size, 'RGBA')
        plt.close(fig)
        return surface

    def _add_edges(self, graph, node):
        """Recursively adds nodes and edges to the NetworkX graph."""
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
        """Draws the background, the AVL tree, and all buttons/inputs."""
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

        # Draw buttons and inputs
        self.draw_buttons()
        self.draw_inputs()

    def _create_buttons(self):
        """Creates buttons for Inorder, Preorder, and Postorder traversal."""
        btn_width, btn_height = 120, 30
        x = self.game_width + 20
        y_start = self.HEIGHT - 325
        spacing = 10
        buttons = {
            "Inorder": pygame.Rect(x, y_start, btn_width, btn_height),
            "Preorder": pygame.Rect(x, y_start + btn_height + spacing, btn_width, btn_height),
            "Postorder": pygame.Rect(x, y_start + 2 * (btn_height + spacing), btn_width, btn_height),
        }
        return buttons

    def draw_buttons(self):
        """Draws traversal buttons on the screen."""
        font = pygame.font.SysFont("Arial", 16, bold=True)
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            label = font.render(text, True, (0, 0, 0))
            self.screen.blit(label, (rect.x + 10, rect.y + 5))

    def handle_click(self, pos):
        """Handles mouse click events on buttons and input fields."""
        for key, info in self.inputs.items():
            if info["rect"].collidepoint(pos):
                if key == "Consult":
                    self._run_range_query()
                else:
                    self.active_input = key
                return

        for text, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if text == "Inorder":
                    traversal = self.avl_controller.inorder()
                elif text == "Preorder":
                    traversal = self.avl_controller.preorder()
                else:
                    traversal = self.avl_controller.postorder()

                # Run traversal animation
                self.animate_traversal(traversal)

    def handle_key(self, event):
        """Handles keyboard input for active text fields."""
        if self.active_input is None:
            return
        if event.key == pygame.K_BACKSPACE:
            self.inputs[self.active_input]["text"] = self.inputs[self.active_input]["text"][:-1]
        elif event.key == pygame.K_RETURN:
            self.active_input = None
        else:
            self.inputs[self.active_input]["text"] += event.unicode

    def _run_range_query(self):
        """Executes a range query based on the input fields."""
        try:
            x_min = int(self.inputs["x_min"]["text"])
            x_max = int(self.inputs["x_max"]["text"])
            y_min = int(self.inputs["y_min"]["text"])
            y_max = int(self.inputs["y_max"]["text"])
        except ValueError:
            print("⚠️ Values must be integers")
            return

        # Call AVL controller method
        self.avl_controller.print_range_query(x_min, x_max, y_min, y_max)

    def animate_traversal(self, nodes):
        """
        Animates the traversal of the given list of nodes.
        nodes: list returned by AVLTreeController (e.g., ["(10,20)", "(5,30)", ...])
        """
        normalized = []
        for item in nodes:
            if isinstance(item, str):
                nid = item.replace(" ", "")
            else:
                try:
                    nid = f"({item.get_x1()},{item.get_y1()})"
                except Exception:
                    nid = str(item).replace(" ", "")
            normalized.append(nid)

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

        # Clear highlights at the end
        self.highlight_nodes.clear()
        self.dirty = True
        self.tree_surface = self.create_tree_surface()
        tree_x = self.game_width + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
        tree_y = 50
        self.screen.blit(self.tree_surface, (tree_x, tree_y))
        self.draw_buttons()
        pygame.display.flip()

    def hierarchy_pos(self, G, root=None, width=1., vert_gap=0.2,
                      vert_loc=0, xcenter=0.5, pos=None, parent=None):
        """
        Computes a hierarchical layout for NetworkX graphs.
        """
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