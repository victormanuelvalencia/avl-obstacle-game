import pygame
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import networkx as nx

from controllers.obstacle_cleanup_controller import ObstacleCleanupController
from models.obstacle import Obstacle
from utils.file_admin import read_json
from models.car import Car
from controllers.car_controller import CarController

class IntegratedGameView:
    def __init__(self, config, avl_controller):
        pygame.init()
        # Expandimos la ventana para incluir el árbol
        self.WIDTH, self.HEIGHT = 1500, 768  # Más ancho para el árbol
        self.GAME_WIDTH = 1000  # Ancho original del juego
        self.TREE_WIDTH = 500   # Ancho para el árbol

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego del Carrito con AVL - Vista Integrada")
        self.clock = pygame.time.Clock()
        self.config = config

        # Guardar el controlador AVL
        self.avl_controller = avl_controller

        # ✅ Nuevo: controlador para limpiar obstáculos fuera de pantalla
        self.cleanup_controller = ObstacleCleanupController(self.avl_controller)

        # Carrito (mantener tu configuración original)
        self.car = Car(
            x1=50,
            y1=self.HEIGHT // 2,
            x2=100,
            y2=self.HEIGHT // 2 + 30,
            energy=100,
            speed_x=0,
            refresh_time=config["refresh_time"],
            speed_y=5,
            jump_height=config["jump_height"],
        )
        self.car_controller = CarController(self.car)

        # Imágenes (mantener tu configuración)
        width = self.car.get_x2() - self.car.get_x1()
        height = self.car.get_y2() - self.car.get_y1()
        self.blue_car = pygame.transform.scale(
            pygame.image.load("views/assets/blue_car.png").convert_alpha(),
            (width, height)
        )
        self.red_car = pygame.transform.scale(
            pygame.image.load("views/assets/red_car.png").convert_alpha(),
            (width, height)
        )

        self.road_offset = 0

        # Obstáculos (mantener tu configuración)
        data = read_json("config/obstacles.json")
        self.obstacles = [Obstacle(obs) for obs in data["obstacles"]]

        # Para el árbol
        self.tree_surface = None
        self.tree_update_counter = 0
        self.tree_update_interval = 30  # Actualizar árbol cada 30 frames

    def create_tree_surface(self):
        """Convierte el plot del árbol a una superficie de Pygame con mejor estilo"""
        root = self.avl_controller.tree.get_root()
        if not root:
            # Crear surface vacía con mejor diseño
            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)
            ax.text(0.5, 0.5, '🌳\nÁrbol Vacío', ha='center', va='center',
                    fontsize=20, transform=ax.transAxes, color='gray')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            fig.patch.set_facecolor('white')
        else:
            # Crear el gráfico del árbol con mejor estilo
            graph = nx.DiGraph()
            self._add_edges_to_graph(graph, root)

            pos = nx.get_node_attributes(graph, 'pos')
            labels = {n: n for n in graph.nodes()}

            fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)
            fig.patch.set_facecolor('white')

            # Dibujar el grafo con estilo mejorado
            nx.draw(graph, pos, with_labels=True, labels=labels,
                    node_size=1200, node_color="lightblue",
                    font_size=8, font_weight="bold", arrows=False, ax=ax,
                    edge_color='gray', linewidths=2, node_shape='o')

            ax.set_title("Estructura del Árbol", fontsize=14, fontweight='bold', pad=20)
            ax.axis('off')

        # Convertir matplotlib a superficie de Pygame
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()

        # Usar el método correcto según la versión de matplotlib
        try:
            raw_data = renderer.buffer_rgba()
            size = canvas.get_width_height()
            pygame_surface = pygame.image.frombuffer(raw_data, size, 'RGBA')
        except AttributeError:
            # Fallback para versiones más antiguas
            try:
                raw_data = renderer.tostring_rgb()
                size = canvas.get_width_height()
                pygame_surface = pygame.image.fromstring(raw_data, size, 'RGB')
            except AttributeError:
                raw_data = renderer.tostring_argb()
                size = canvas.get_width_height()
                pygame_surface = pygame.image.fromstring(raw_data, size, 'ARGB')

        plt.close(fig)  # Importante: cerrar figura para evitar memory leaks
        return pygame_surface

    def _add_edges_to_graph(self, graph, node, x=0, y=0, layer=1):
        """Método auxiliar para construir el grafo del árbol (tu lógica original)"""
        if not node:
            return

        node_id = f"({node.get_x1()},{node.get_y1()})"
        graph.add_node(node_id, pos=(x, y))

        if node.get_left():
            left_id = f"({node.get_left().get_x1()},{node.get_left().get_y1()})"
            graph.add_edge(node_id, left_id)
            self._add_edges_to_graph(graph, node.get_left(), x - 1 / layer, y - 1, layer + 1)

        if node.get_right():
            right_id = f"({node.get_right().get_x1()},{node.get_right().get_y1()})"
            graph.add_edge(node_id, right_id)
            self._add_edges_to_graph(graph, node.get_right(), x + 1 / layer, y - 1, layer + 1)

    def draw_game_area(self):
        """Dibujar el área del juego con mejor diseño"""
        # Fondo del área de juego con gradiente
        for y in range(self.HEIGHT):
            color_intensity = int(135 + (y / self.HEIGHT) * 50)  # Gradiente sutil
            pygame.draw.line(self.screen, (color_intensity, color_intensity, color_intensity),
                             (0, y), (self.GAME_WIDTH, y))

        # Dibujar carretera con mejor diseño
        dx = self.car.get_speed_x() or 5
        self.road_offset -= dx
        if self.road_offset <= -self.GAME_WIDTH:
            self.road_offset = 0

        road_y = 200
        road_height = 200

        # Carretera principal con bordes
        pygame.draw.rect(self.screen, (80, 80, 80), (self.road_offset, road_y, self.GAME_WIDTH, road_height))
        pygame.draw.rect(self.screen, (80, 80, 80),
                         (self.road_offset + self.GAME_WIDTH, road_y, self.GAME_WIDTH, road_height))

        # Bordes de la carretera
        pygame.draw.rect(self.screen, (255, 255, 255), (self.road_offset, road_y, self.GAME_WIDTH, 5))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.road_offset, road_y + road_height - 5, self.GAME_WIDTH, 5))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.road_offset + self.GAME_WIDTH, road_y, self.GAME_WIDTH, 5))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.road_offset + self.GAME_WIDTH, road_y + road_height - 5, self.GAME_WIDTH, 5))

        # Líneas centrales discontinuas más realistas
        line_width = 4
        line_length = 30
        line_gap = 20
        center_y = road_y + road_height // 2

        for x in range(self.road_offset, self.road_offset + self.GAME_WIDTH * 2, line_length + line_gap):
            if x + line_length <= self.GAME_WIDTH:
                pygame.draw.rect(self.screen, (255, 255, 0), (x, center_y - line_width // 2, line_length, line_width))

        # Obstáculos con mejor visualización
        for obs in self.obstacles:
            obs.update(dx)
            obs.draw(self.screen)
            if (not self.car.is_jumping() and
                    self.car.get_collision_rect().colliderect(obs.rect) and
                    not obs.hit):
                self.car.decrease_energy(obs.damage)
                obs.hit = True

        # Dibujar carrito con sombra
        car_img = self.red_car if self.car.is_jumping() else self.blue_car
        car_x, car_y = self.car.get_x1(), self.car.get_y1() + self.car.get_jump_offset()

        # Sombra del carrito
        if not self.car.is_jumping():
            shadow_surface = pygame.Surface((car_img.get_width(), car_img.get_height()))
            shadow_surface.fill((0, 0, 0))
            shadow_surface.set_alpha(50)
            self.screen.blit(shadow_surface, (car_x + 3, car_y + 3))

        self.screen.blit(car_img, (car_x, car_y))

        # Panel de información del juego mejorado
        self.draw_game_ui()

    def draw_tree_area(self):
        """Dibujar el área del árbol"""
        # Fondo del área del árbol
        pygame.draw.rect(self.screen, (240, 240, 240),
                         (self.GAME_WIDTH, 0, self.TREE_WIDTH, self.HEIGHT))

        # Línea separadora
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.GAME_WIDTH, 0), (self.GAME_WIDTH, self.HEIGHT), 3)

        # Actualizar superficie del árbol solo cada cierto intervalo
        self.tree_update_counter += 1
        if self.tree_update_counter >= self.tree_update_interval or self.tree_surface is None:
            self.tree_surface = self.create_tree_surface()
            self.tree_update_counter = 0

        # Dibujar el árbol si existe la superficie
        if self.tree_surface:
            # Centrar el árbol en su área
            tree_x = self.GAME_WIDTH + (self.TREE_WIDTH - self.tree_surface.get_width()) // 2
            tree_y = (self.HEIGHT - self.tree_surface.get_height()) // 2
            self.screen.blit(self.tree_surface, (tree_x, tree_y))

    def draw_game_ui(self):
        """Panel de información del juego con mejor diseño"""
        # Panel superior izquierdo con fondo semi-transparente
        panel_surface = pygame.Surface((280, 100))
        panel_surface.fill((0, 0, 0))
        panel_surface.set_alpha(180)
        self.screen.blit(panel_surface, (10, 10))

        # Borde del panel
        pygame.draw.rect(self.screen, (100, 150, 255), (10, 10, 280, 100), 2)

        # Energía con barra visual
        font_title = pygame.font.Font(None, 28)
        font_info = pygame.font.Font(None, 24)

        energy = self.car.get_energy()
        energy_text = font_title.render("ENERGÍA", True, (255, 255, 255))
        self.screen.blit(energy_text, (20, 20))

        # Barra de energía
        bar_width = 200
        bar_height = 15
        bar_x, bar_y = 20, 45

        # Fondo de la barra
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        # Barra de energía con colores según nivel
        energy_width = int((energy / 100) * bar_width)
        if energy > 60:
            energy_color = (0, 255, 0)  # Verde
        elif energy > 30:
            energy_color = (255, 255, 0)  # Amarillo
        else:
            energy_color = (255, 0, 0)  # Rojo

        pygame.draw.rect(self.screen, energy_color, (bar_x, bar_y, energy_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Porcentaje
        energy_percent = font_info.render(f"{energy}%", True, (255, 255, 255))
        self.screen.blit(energy_percent, (bar_x + bar_width + 10, bar_y - 2))

        # Estado del salto
        jump_status = "SALTANDO" if self.car.is_jumping() else "EN CARRETERA"
        status_color = (255, 100, 100) if self.car.is_jumping() else (100, 255, 100)
        status_text = font_info.render(jump_status, True, status_color)
        self.screen.blit(status_text, (20, 70))

        # Controles (panel inferior)
        # controls_surface = pygame.Surface((self.GAME_WIDTH - 20, 80))
        # controls_surface.fill((0, 0, 0))
        # controls_surface.set_alpha(150)
        # self.screen.blit(controls_surface, (10, self.HEIGHT - 90))

        # pygame.draw.rect(self.screen, (100, 150, 255), (10, self.HEIGHT - 90, self.GAME_WIDTH - 20, 80), 2)

        # controls_title = font_title.render("CONTROLES:", True, (255, 255, 255))
        # self.screen.blit(controls_title, (20, self.HEIGHT - 80))

        # controls = ["↑/↓ - Mover carrito", "ESPACIO - Saltar", "Evita los obstáculos rojos"]
        # for i, control in enumerate(controls):
          #  control_text = font_info.render(control, True, (200, 200, 200))
           # self.screen.blit(control_text, (20, self.HEIGHT - 55 + i * 18))

        # Mostrar información del AVL
        font_small = pygame.font.SysFont(None, 24)

        # Información del árbol
        node_count = self._count_nodes(self.avl_controller.tree.get_root())
        info_texts = [
            f"Nodos totales: {node_count}",
            f"Altura: {self.avl_controller._height(self.avl_controller.tree.get_root())}",
            "Recorridos disponibles:",
            "- Inorder",
            "- Preorder",
            "- Postorder"
        ]

        start_y = self.HEIGHT - 150
        for i, text in enumerate(info_texts):
            color = (100, 100, 100) if text.startswith("-") else (0, 0, 0)
            info_surface = font_small.render(text, True, color)
            self.screen.blit(info_surface, (self.GAME_WIDTH + 10, start_y + i * 20))

    def _count_nodes(self, node):
        """Contar nodos del árbol recursivamente"""
        if not node:
            return 0
        return 1 + self._count_nodes(node.get_left()) + self._count_nodes(node.get_right())

    def run(self):
        """Loop principal integrado con limpieza de obstáculos"""
        running = True

        while running:
            self.screen.fill((45, 45, 55))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Control del carrito
            keys = pygame.key.get_pressed()
            if not self.car.is_jumping():
                if keys[pygame.K_UP]:
                    self.car_controller.move_up()
                if keys[pygame.K_DOWN]:
                    self.car_controller.move_down()
                if keys[pygame.K_SPACE]:
                    self.car.set_jumping(True)

            self.car_controller.jump()

            # ✅ Llamar al cleanup cada frame
            self.cleanup_controller.cleanup_obstacles(self.WIDTH)

            # Dibujar ambas áreas
            self.draw_game_area()
            self.draw_tree_area()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        #1

