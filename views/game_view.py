import pygame
from controllers.button_controller import ButtonController
from models.car import Car
from controllers.car_controller import CarController
from models.obstacle import Obstacle
from utils.file_admin import read_json
from components.button import Button

class GameView:
    """
    Main game view for the road game.
    Handles rendering the road, car, obstacles, UI, and pause logic.
    """

    GAME_WIDTH = 800
    HEIGHT = 800

    def __init__(self, config, obstacles_file="config/obstacles.json"):
        """
        Initialize the game view.

        Args:
            config: Dictionary with game configuration (refresh_time, jump_height, etc.)
            obstacles_file: Path to the JSON file with obstacle definitions.
        """
        self.config = config
        self.screen = None
        self.clock = pygame.time.Clock()

        # Pause button and controller
        self.pause_button = Button(x=20, y=130, width=100, height=40, text="PAUSE")
        self.button_controller = ButtonController()

        # Car setup
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

        # Car images
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

        # Road background
        self.road_img = pygame.image.load("views/assets/5_carriles.png").convert_alpha()
        self.road_offset = 0

        # Load obstacles
        data = read_json(obstacles_file)
        self.obstacles = [Obstacle(obs) for obs in data["obstacles"]]

        # Pause state
        self.paused = False

    def set_screen(self, screen):
        """Assign the Pygame screen surface for rendering."""
        self.screen = screen

    def handle_input(self):
        """
        Handle keyboard input to move or jump the car.
        Does nothing if the game is paused.
        """
        if self.button_controller.is_paused():
            return

        keys = pygame.key.get_pressed()
        if not self.car.is_jumping():
            if keys[pygame.K_UP]:
                self.car_controller.move_up()
            if keys[pygame.K_DOWN]:
                self.car_controller.move_down()
            if keys[pygame.K_SPACE]:
                self.car.set_jumping(True)

        self.car_controller.jump()

    def handle_events(self, events):
        """
        Handle Pygame events such as quitting or pressing the pause button.

        Args:
            events: List of Pygame events.

        Returns:
            "quit" if the user wants to exit, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            self.button_controller.handle_pause_button(self.pause_button, event)
        return None

    def update_obstacles(self, dx):
        """
        Update all obstacles' positions and check collisions with the car.

        Args:
            dx: Amount to scroll obstacles horizontally.
        """
        if self.button_controller.is_paused():
            return

        for obs in self.obstacles:
            obs.update(dx)
            if (not self.car.is_jumping() and
                    self.car.get_collision_rect().colliderect(obs.rect) and
                    not obs.hit):
                self.car.decrease_energy(obs.damage)
                obs.hit = True

    def draw_game_area(self):
        """
        Render the game area including road, obstacles, car, pause button, and UI.
        Handles scrolling and visual jump offset.
        """
        dx = self.car.get_speed_x() or 5

        # Draw road background repeatedly in Y
        img_height = self.road_img.get_height()
        for y in range(0, self.HEIGHT, img_height):
            self.screen.blit(self.road_img, (self.road_offset, y))
            self.screen.blit(self.road_img, (self.road_offset + self.GAME_WIDTH, y))

        # Scroll the road if not paused
        if not self.button_controller.is_paused():
            self.road_offset -= dx
            if self.road_offset <= -self.GAME_WIDTH:
                self.road_offset = 0

        # Update and draw obstacles
        self.update_obstacles(dx)
        for obs in self.obstacles:
            obs.draw(self.screen)

        # Draw the car with jump offset
        car_img = self.red_car if self.car.is_jumping() else self.blue_car
        car_x, car_y = self.car.get_x1(), self.car.get_y1() + self.car.get_jump_offset()
        if not self.car.is_jumping():
            shadow_surface = pygame.Surface((car_img.get_width(), car_img.get_height()))
            shadow_surface.fill((0, 0, 0))
            shadow_surface.set_alpha(50)
            self.screen.blit(shadow_surface, (car_x + 3, car_y + 3))
        self.screen.blit(car_img, (car_x, car_y))

        # Draw pause button
        self.pause_button.draw(self.screen)

        # Show "PAUSE" message if paused
        if self.button_controller.is_paused():
            font = pygame.font.Font(None, 72)
            text_surf = font.render("PAUSE", True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(self.GAME_WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(text_surf, text_rect)

        # Draw UI elements
        self.draw_ui()

    def draw_ui(self):
        """
        Draw the game's UI including energy panel, energy bar, and jump status.
        """
        font_title = pygame.font.Font(None, 28)
        font_info = pygame.font.Font(None, 24)

        # Energy panel
        panel_surface = pygame.Surface((280, 100))
        panel_surface.fill((0, 0, 0))
        panel_surface.set_alpha(180)
        self.screen.blit(panel_surface, (10, 10))
        pygame.draw.rect(self.screen, (100, 150, 255), (10, 10, 280, 100), 2)

        # Energy text
        energy = self.car.get_energy()
        energy_text = font_title.render("ENERGY", True, (255, 255, 255))
        self.screen.blit(energy_text, (20, 20))

        # Energy bar
        bar_width, bar_height = 200, 15
        bar_x, bar_y = 20, 45
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        energy_width = int((energy / 100) * bar_width)
        if energy > 60:
            energy_color = (0, 255, 0)
        elif energy > 30:
            energy_color = (255, 255, 0)
        else:
            energy_color = (255, 0, 0)
        pygame.draw.rect(self.screen, energy_color, (bar_x, bar_y, energy_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Jump status
        jump_status = "JUMPING" if self.car.is_jumping() else "ON ROAD"
        status_color = (255, 100, 100) if self.car.is_jumping() else (100, 255, 100)
        status_text = font_info.render(jump_status, True, status_color)
        self.screen.blit(status_text, (20, 70))