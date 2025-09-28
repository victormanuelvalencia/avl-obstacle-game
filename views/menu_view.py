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
        """
        Display the main menu and handle user input.

        Returns:
            bool: True if the player clicks "Play", False if the window is closed.
        """
        running = True
        while running:
            self.screen.fill((30, 30, 40))  # Dark background

            # Render title text
            title_text = self.font_title.render("Car Game", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
            self.screen.blit(title_text, title_rect)

            # Render "Play" button
            play_text = self.font_button.render("PLAY", True, (0, 0, 0))
            play_rect = play_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            pygame.draw.rect(self.screen, (100, 200, 100), play_rect.inflate(40, 20))  # Green button
            self.screen.blit(play_text, play_rect)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False  # Exit the program
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_rect.collidepoint(event.pos):
                        return True  # Start the game

            # Update display and limit frame rate
            pygame.display.flip()
            self.clock.tick(60)