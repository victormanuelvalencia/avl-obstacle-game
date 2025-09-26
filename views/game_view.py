import pygame
from models.car import Car
from controllers.car_controller import CarController

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
            energy=100,
            speed_x=0,
            refresh_time=config["refresh_time"],
            speed_y=5,
            jump_height=config["jump_height"],
        )
        self.car_controller = CarController(self.car, road_y, road_height)

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

        # Carrito
        car_img = self.red_car if self.car.is_jumping() else self.blue_car
        car_x, car_y = self.car.get_x1(), self.car.get_y1() + self.car.get_jump_offset()
        if not self.car.is_jumping():
            shadow_surface = pygame.Surface((car_img.get_width(), car_img.get_height()))
            shadow_surface.fill((0, 0, 0))
            shadow_surface.set_alpha(50)
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

        # Barra de energía
        bar_width, bar_height = 200, 15
        bar_x, bar_y = 20, 45
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        energy_width = int((energy / 100) * bar_width)
        if energy > 60:
            energy_color = (0, 255, 0)
        elif energy > 30:
            energy_color = (255, 255, 0)
        else:
            energy_color = (255, 0, 0)
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