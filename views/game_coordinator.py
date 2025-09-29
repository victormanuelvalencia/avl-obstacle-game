import pygame
import threading
from views.game_view import GameView
from views.tree_view import TreeView
from controllers.obstacle_cleanup_controller import ObstacleCleanupController


class GameCoordinator:
    """
    Coordinates the main game logic and the AVL tree visualization.

    Attributes:
        config (dict): Game configuration settings.
        avl_controller (AVLTreeController): Controller managing the AVL tree.
        game_view (GameView): View responsible for rendering the game area.
        tree_view (TreeView): View responsible for rendering the AVL tree.
        cleanup_controller (ObstacleCleanupController): Controller for removing obstacles.
        WIDTH (int): Total width of the combined game and tree display.
        HEIGHT (int): Total height of the display.
        screen (pygame.Surface): Pygame surface for rendering.
        clock (pygame.time.Clock): Pygame clock to control FPS.
        tree_update_event (threading.Event): Event to trigger AVL tree redraw.
        running (bool): Game loop running flag.
        tree_thread (threading.Thread): Background thread for updating the tree view.
    """

    def __init__(self, config, avl_controller, obstacles_file="config/obstacles.json"):
        """
        Initializes the GameCoordinator with configuration, AVL controller,
        and optional obstacles file.
        """
        self.config = config
        self.avl_controller = avl_controller

        # Views
        self.game_view = GameView(config, obstacles_file)
        self.tree_view = TreeView(avl_controller, self.game_view.GAME_WIDTH)

        # Obstacle cleanup controller
        self.cleanup_controller = ObstacleCleanupController(avl_controller)

        # Display setup
        self.WIDTH = self.game_view.GAME_WIDTH + self.tree_view.TREE_WIDTH
        self.HEIGHT = self.game_view.HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Car Game + AVL Tree")
        self.clock = pygame.time.Clock()

        # Pass the screen to views
        self.game_view.set_screen(self.screen)
        self.tree_view.set_screen(self.screen)

        # Thread synchronization
        self.tree_update_event = threading.Event()
        self.running = True

        # AVL tree background thread
        self.tree_thread = threading.Thread(target=self._tree_loop, daemon=True)
        self.tree_thread.start()

    def _tree_loop(self):
        """
        Background thread responsible for regenerating the tree view
        without freezing the main game loop.
        """
        while self.running:
            if self.tree_update_event.wait(timeout=0.1):
                try:
                    self.tree_view.tree_surface = self.tree_view.create_tree_surface()
                except Exception as e:
                    print(f"⚠️ Error in tree thread: {e}")
                finally:
                    self.tree_update_event.clear()

    def run(self):
        """
        Main game loop: handles events, updates game logic, redraws the
        game and tree views, and manages obstacle cleanup.
        """
        while self.running:
            # Clear the screen
            self.screen.fill((45, 45, 55))

            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Pass clicks to TreeView (buttons and inputs)
                    self.tree_view.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    # Pass key input to TreeView (text input)
                    self.tree_view.handle_key(event)

            # Pass events to GameView (pause button, etc.)
            self.game_view.handle_events(events)

            # Main game logic
            if not self.game_view.button_controller.is_paused():

                # Process logic only if the game is NOT over
                if not (self.game_view.game_over or self.game_view.game_won):
                    self.game_view.handle_input()

                    dx = self.game_view.car.get_speed_x() or 5
                    self.game_view.update_obstacles(dx)

                    # Remove obstacles only while the game is running
                    removed = self.cleanup_controller.cleanup_obstacles(
                        self.game_view.obstacles,
                        self.game_view.GAME_WIDTH
                    )

                    if removed:
                        print("🗑️ Obstacles removed from the screen:")
                        for obs in removed:
                            print(f" - {obs.type} at ({obs.rect.left}, {obs.rect.top})")

                        print("🌳 Current AVL tree state (in-order):")
                        current_tree = self.avl_controller.inorder()
                        print(" -> ".join(current_tree) if current_tree else " Empty tree")

                        # Signal to regenerate the tree
                        self.tree_update_event.set()

            # Drawing
            self.game_view.draw_game_area()
            self.tree_view.draw_tree_area()

            pygame.display.flip()
            self.clock.tick(60)

        # Gracefully close
        self.running = False
        self.tree_update_event.set()
        pygame.quit()