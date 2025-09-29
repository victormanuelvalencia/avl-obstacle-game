import pygame

class MenuView:
    """
    Main menu view for the car game.
    Displays a title and a "Play" button and handles user input to start the game.
    """

    def __init__(self, width=800, height=600):
        """
        Initialize the menu view.

        Args:
            width (int): Width of the window.
            height (int): Height of the window.
        """
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Main Menu - Car Game")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 50)

    def run(self):
        running = True
        while running:
            self.screen.fill((30, 30, 40))  # Dark background

            # Render title text
            title_text = self.font_title.render("Car Game", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
            self.screen.blit(title_text, title_rect)

            # Play button rectangle
            play_text = self.font_button.render("PLAY", True, (0, 0, 0))
            play_rect = play_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            button_rect = play_rect.inflate(40, 20)

            # --- Hover effect ---
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                button_color = (50, 150, 50)  # Darker green on hover
            else:
                button_color = (100, 200, 100)  # Normal green

            pygame.draw.rect(self.screen, button_color, button_rect)
            self.screen.blit(play_text, play_rect)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return True

            # Update display and frame rate
            pygame.display.flip()
            self.clock.tick(60)