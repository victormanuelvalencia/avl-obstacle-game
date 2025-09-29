import pygame
import threading
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

        # Controlador de limpieza
        self.cleanup_controller = ObstacleCleanupController(avl_controller)

        # Pantalla
        self.WIDTH = self.game_view.GAME_WIDTH + self.tree_view.TREE_WIDTH
        self.HEIGHT = self.game_view.HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego Carrito + Árbol AVL")
        self.clock = pygame.time.Clock()

        # Pasar pantalla a las vistas
        self.game_view.set_screen(self.screen)
        self.tree_view.set_screen(self.screen)

        # 🔹 Sincronización con hilos
        self.tree_update_event = threading.Event()
        self.running = True

        # Hilo del árbol
        self.tree_thread = threading.Thread(target=self._tree_loop, daemon=True)
        self.tree_thread.start()

    def _tree_loop(self):
        """Hilo encargado de regenerar la vista del árbol sin frenar el juego."""
        while self.running:
            if self.tree_update_event.wait(timeout=0.1):
                try:
                    self.tree_view.tree_surface = self.tree_view.create_tree_surface()
                except Exception as e:
                    print(f"⚠️ Error en hilo del árbol: {e}")
                finally:
                    self.tree_update_event.clear()

    def run(self):
        while self.running:
            self.screen.fill((45, 45, 55))

            # === Manejo de eventos ===
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # pasar clics al TreeView (botones e inputs)
                    self.tree_view.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    # pasar teclas al TreeView (escribir en inputs)
                    self.tree_view.handle_key(event)

            # Pasar eventos al GameView (botón pausa, etc.)
            self.game_view.handle_events(events)

            # === Lógica principal ===
            if not self.game_view.button_controller.is_paused():

                # 🚫 Solo procesamos lógica si el juego NO terminó
                if not (self.game_view.game_over or self.game_view.game_won):
                    self.game_view.handle_input()

                    dx = self.game_view.car.get_speed_x() or 5
                    self.game_view.update_obstacles(dx)

                    # Limpieza de obstáculos solo mientras el juego sigue
                    removed = self.cleanup_controller.cleanup_obstacles(
                        self.game_view.obstacles,
                        self.game_view.GAME_WIDTH
                    )

                    if removed:
                        print("🗑️ Obstáculos eliminados de la pantalla:")
                        for obs in removed:
                            print(f" - {obs.type} en ({obs.rect.left}, {obs.rect.top})")

                        print("🌳 Estado actual del árbol AVL (in-order):")
                        current_tree = self.avl_controller.inorder()
                        print(" -> ".join(current_tree) if current_tree else " Árbol vacío")

                        # ✅ Señal para regenerar el árbol
                        self.tree_update_event.set()

            # === Dibujar ===
            self.game_view.draw_game_area()
            self.tree_view.draw_tree_area()

            pygame.display.flip()
            self.clock.tick(60)

        # Cerrar correctamente
        self.running = False
        self.tree_update_event.set()
        pygame.quit()