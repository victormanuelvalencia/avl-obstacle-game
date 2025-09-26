import pygame
from views.game_view import GameView
from views.tree_view_surface import TreeViewSurface

class IntegratedGameView:
    def __init__(self, config, avl_controller, obstacles):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1300, 800
        self.GAME_WIDTH = 800
        self.TREE_WIDTH = 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego del Carrito con AVL - Integrado")
        self.clock = pygame.time.Clock()

        # Inicializar vistas
        self.game_view = GameView(config)
        self.game_view.set_obstacles(obstacles)
        self.tree_view = TreeViewSurface(avl_controller)

    def draw_tree_area(self):
        pygame.draw.rect(self.screen, (240, 240, 240),
                         (self.GAME_WIDTH, 0, self.TREE_WIDTH, self.HEIGHT))
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.GAME_WIDTH, 0), (self.GAME_WIDTH, self.HEIGHT), 3)

        self.tree_view.update_surface()
        tree_surface = self.tree_view.surface
        if tree_surface:
            tree_x = self.GAME_WIDTH + (self.TREE_WIDTH - tree_surface.get_width()) // 2
            tree_y = (self.HEIGHT - tree_surface.get_height()) // 2
            self.screen.blit(tree_surface, (tree_x, tree_y))

    def run(self):
        running = True
        while running:
            self.screen.fill((45, 45, 55))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if not self.game_view.car.is_jumping():
                if keys[pygame.K_UP]:
                    self.game_view.car_controller.move_up()
                if keys[pygame.K_DOWN]:
                    self.game_view.car_controller.move_down()
                if keys[pygame.K_SPACE]:
                    self.game_view.car.set_jumping(True)

            self.game_view.car_controller.jump()
            self.game_view.draw_game_area(self.screen)
            self.draw_tree_area()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()