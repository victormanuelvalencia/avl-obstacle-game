import pygame

class MenuView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Menú Principal - Juego del Carrito")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 50)

    def run(self):
        running = True
        while running:
            self.screen.fill((30, 30, 40))  # Fondo oscuro

            # Texto del título
            title_text = self.font_title.render("Juego del Carrito", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
            self.screen.blit(title_text, title_rect)

            # Botón Jugar
            play_text = self.font_button.render("JUGAR", True, (0, 0, 0))
            play_rect = play_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            pygame.draw.rect(self.screen, (100, 200, 100), play_rect.inflate(40, 20))  # Botón verde
            self.screen.blit(play_text, play_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False  # salir del programa
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_rect.collidepoint(event.pos):
                        return True  # iniciar el juego

            pygame.display.flip()
            self.clock.tick(60)
