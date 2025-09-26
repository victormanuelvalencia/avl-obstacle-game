# views/game_coordinator.py
import pygame
from views.game_view import GameView
from views.tree_view import TreeView
from controllers.obstacle_cleanup_controller import ObstacleCleanupController

class GameCoordinator:
    def __init__(self, config, avl_controller, obstacles_file="config/obstacles.json"):
        self.config = config
        self.avl_controller = avl_controller

        # Vistas
        self.game_view = GameView(config, obstacles_file)
        self.tree_view = TreeView(avl_controller, self.game_view.GAME_WIDTH)

        # Controlador de limpieza de obstáculos
        self.cleanup_controller = ObstacleCleanupController(avl_controller)



        # Pantalla total
        self.WIDTH = self.game_view.GAME_WIDTH + self.tree_view.TREE_WIDTH
        self.HEIGHT = self.game_view.HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego Carrito + Árbol AVL")
        self.clock = pygame.time.Clock()

        # Pasar pantalla a las vistas
        self.game_view.set_screen(self.screen)
        self.tree_view.set_screen(self.screen)

    def run(self):
        running = True

        while running:
            self.screen.fill((45, 45, 55))

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Manejo del carrito y obstáculos
            self.game_view.handle_input()

            # Actualizar obstáculos
            dx = self.game_view.car.get_speed_x() or 5
            self.game_view.update_obstacles(dx)

            print("inicio de removed")
            # Limpieza de obstáculos fuera de pantalla
            removed = self.cleanup_controller.cleanup_obstacles(self.game_view.obstacles, self.game_view.GAME_WIDTH)

            print(removed)
            if removed:
                print("hola desde removed")
                print("🗑️ Obstáculos eliminados de la pantalla:")
                for obs in removed:
                    print(f" - {obs.type} en ({obs.rect.left}, {obs.rect.top})")

                # Mostrar el estado actual del árbol
                current_tree = self.avl_controller.inorder()
                print("🌳 Estado actual del árbol AVL (in-order):")
                print(" -> ".join(current_tree) if current_tree else " Árbol vacío")

                # Regenerar la superficie del árbol para la vista
                self.tree_view.tree_surface = self.tree_view.create_tree_surface()

            # Dibujar áreas
            self.game_view.draw_game_area()
            self.tree_view.draw_tree_area()

            # Actualizar pantalla
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
