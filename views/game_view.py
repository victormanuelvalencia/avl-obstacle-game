import pygame
from models.car import Car
from controllers.car_controller import CarController
<<<<<<< HEAD
from models.obstacle import Obstacle
from utils.file_admin import read_json

class GameView:
    GAME_WIDTH = 1000
    HEIGHT = 768

    def __init__(self, config, obstacles_file="config/obstacles.json"):
        self.config = config
        self.screen = None
        self.clock = pygame.time.Clock()

        # Carrito
        self.car = Car(
            x1=50,
            y1=self.HEIGHT // 2,
            x2=100,
            y2=self.HEIGHT // 2 + 30,
=======

class GameView:
    def __init__(self, config):
        self.WIDTH, self.HEIGHT = 1000, 800
        self.screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.config = config

        # Carrito
        road_y, road_height = 150, 400  # carretera más ancha
        self.road_y = road_y
        self.road_height = road_height

        self.car = Car(
            x1=50,
            y1=road_y + road_height // 2 - 15,  # centrar en carretera
            x2=100,
            y2=road_y + road_height // 2 + 15,
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed
            energy=100,
            speed_x=0,
            refresh_time=config["refresh_time"],
            speed_y=5,
            jump_height=config["jump_height"],
        )
<<<<<<< HEAD
        self.car_controller = CarController(self.car)
=======
        self.car_controller = CarController(self.car, road_y, road_height)
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed

        # Imágenes
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
<<<<<<< HEAD

        # Obstáculos
        data = read_json(obstacles_file)
        self.obstacles = [Obstacle(obs) for obs in data["obstacles"]]

    def set_screen(self, screen):
        self.screen = screen

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.car.is_jumping():
            if keys[pygame.K_UP]:
                self.car_controller.move_up()
            if keys[pygame.K_DOWN]:
                self.car_controller.move_down()
            if keys[pygame.K_SPACE]:
                self.car.set_jumping(True)
        self.car_controller.jump()

    def update_obstacles(self, dx):
        for obs in self.obstacles:
            obs.update(dx)
            if (not self.car.is_jumping() and
                    self.car.get_collision_rect().colliderect(obs.rect) and
                    not obs.hit):
                self.car.decrease_energy(obs.damage)
                obs.hit = True

    def draw_game_area(self):
        # Fondo y carretera
        for y in range(self.HEIGHT):
            color_intensity = int(135 + (y / self.HEIGHT) * 50)
            pygame.draw.line(self.screen, (color_intensity, color_intensity, color_intensity),
                             (0, y), (self.GAME_WIDTH, y))
        dx = self.car.get_speed_x() or 5
        self.road_offset -= dx
        if self.road_offset <= -self.GAME_WIDTH:
            self.road_offset = 0

        road_y, road_height = 200, 200
        pygame.draw.rect(self.screen, (80, 80, 80), (self.road_offset, road_y, self.GAME_WIDTH, road_height))
        pygame.draw.rect(self.screen, (80, 80, 80),
                         (self.road_offset + self.GAME_WIDTH, road_y, self.GAME_WIDTH, road_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.road_offset, road_y, self.GAME_WIDTH, 5))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.road_offset, road_y + road_height - 5, self.GAME_WIDTH, 5))

        # Líneas centrales
        line_width, line_length, line_gap = 4, 30, 20
        center_y = road_y + road_height // 2
        for x in range(self.road_offset, self.road_offset + self.GAME_WIDTH * 2, line_length + line_gap):
            if x + line_length <= self.GAME_WIDTH:
                pygame.draw.rect(self.screen, (255, 255, 0), (x, center_y - line_width // 2, line_length, line_width))

        # Obstáculos
        self.update_obstacles(dx)
        for obs in self.obstacles:
            obs.draw(self.screen)
=======
        self.obstacles = []

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles

    def draw_game_area(self, surface):
        dx = self.car.get_speed_x() or 5
        self.road_offset -= dx
        if self.road_offset <= -self.WIDTH:
            self.road_offset = 0

        # Fondo gradiente
        for y in range(self.HEIGHT):
            color_intensity = int(135 + (y / self.HEIGHT) * 50)
            pygame.draw.line(surface, (color_intensity, color_intensity, color_intensity),
                             (0, y), (self.WIDTH, y))

        # Carretera
        pygame.draw.rect(surface, (80, 80, 80), (self.road_offset, self.road_y, self.WIDTH, self.road_height))
        pygame.draw.rect(surface, (80, 80, 80), (self.road_offset + self.WIDTH, self.road_y, self.WIDTH, self.road_height))

        # Bordes
        pygame.draw.rect(surface, (255, 255, 255), (self.road_offset, self.road_y, self.WIDTH, 5))
        pygame.draw.rect(surface, (255, 255, 255), (self.road_offset, self.road_y + self.road_height - 5, self.WIDTH, 5))

        # Líneas centrales
        line_width, line_length, line_gap = 4, 30, 20
        center_y = self.road_y + self.road_height // 2
        for x in range(self.road_offset, self.road_offset + self.WIDTH * 2, line_length + line_gap):
            pygame.draw.rect(surface, (255, 255, 0), (x, center_y - line_width // 2, line_length, line_width))

        # Obstáculos
        for obs in self.obstacles:
            obs.update(dx)
            obs.draw(surface)
            if (not self.car.is_jumping() and
                self.car.get_collision_rect().colliderect(obs.rect) and
                not obs.hit):
                self.car.decrease_energy(obs.damage)
                obs.hit = True
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed

        # Carrito
        car_img = self.red_car if self.car.is_jumping() else self.blue_car
        car_x, car_y = self.car.get_x1(), self.car.get_y1() + self.car.get_jump_offset()
        if not self.car.is_jumping():
            shadow_surface = pygame.Surface((car_img.get_width(), car_img.get_height()))
            shadow_surface.fill((0, 0, 0))
            shadow_surface.set_alpha(50)
<<<<<<< HEAD
            self.screen.blit(shadow_surface, (car_x + 3, car_y + 3))
        self.screen.blit(car_img, (car_x, car_y))

        self.draw_ui()

    def draw_ui(self):
        font_title = pygame.font.Font(None, 28)
        font_info = pygame.font.Font(None, 24)

        # Panel energía
        panel_surface = pygame.Surface((280, 100))
        panel_surface.fill((0, 0, 0))
        panel_surface.set_alpha(180)
        self.screen.blit(panel_surface, (10, 10))
        pygame.draw.rect(self.screen, (100, 150, 255), (10, 10, 280, 100), 2)

        energy = self.car.get_energy()
        energy_text = font_title.render("ENERGÍA", True, (255, 255, 255))
        self.screen.blit(energy_text, (20, 20))
=======
            surface.blit(shadow_surface, (car_x + 3, car_y + 3))
        surface.blit(car_img, (car_x, car_y))

        # UI
        self.draw_game_ui(surface)

    def draw_game_ui(self, surface):
        panel_surface = pygame.Surface((280, 100))
        panel_surface.fill((0, 0, 0))
        panel_surface.set_alpha(180)
        surface.blit(panel_surface, (10, 10))
        pygame.draw.rect(surface, (100, 150, 255), (10, 10, 280, 100), 2)

        font_title = pygame.font.Font(None, 28)
        font_info = pygame.font.Font(None, 24)

        energy = self.car.get_energy()
        energy_text = font_title.render("ENERGÍA", True, (255, 255, 255))
        surface.blit(energy_text, (20, 20))
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed

        # Barra de energía
        bar_width, bar_height = 200, 15
        bar_x, bar_y = 20, 45
<<<<<<< HEAD
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
=======
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed
        energy_width = int((energy / 100) * bar_width)
        if energy > 60:
            energy_color = (0, 255, 0)
        elif energy > 30:
            energy_color = (255, 255, 0)
        else:
            energy_color = (255, 0, 0)
<<<<<<< HEAD
        pygame.draw.rect(self.screen, energy_color, (bar_x, bar_y, energy_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Estado salto
        jump_status = "SALTANDO" if self.car.is_jumping() else "EN CARRETERA"
        status_color = (255, 100, 100) if self.car.is_jumping() else (100, 255, 100)
        status_text = font_info.render(jump_status, True, status_color)
        self.screen.blit(status_text, (20, 70))
=======
        pygame.draw.rect(surface, energy_color, (bar_x, bar_y, energy_width, bar_height))
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Porcentaje
        energy_percent = font_info.render(f"{energy}%", True, (255, 255, 255))
        surface.blit(energy_percent, (bar_x + bar_width + 10, bar_y - 2))

        # Estado de salto
        jump_status = "SALTANDO" if self.car.is_jumping() else "EN CARRETERA"
        status_color = (255, 100, 100) if self.car.is_jumping() else (100, 255, 100)
        status_text = font_info.render(jump_status, True, status_color)
        surface.blit(status_text, (20, 70))
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed
