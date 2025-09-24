import pygame
from models.obstacle import Obstacle
from utils.file_admin import read_json
from models.car import Car
from controllers.car_controller import CarController


class GameView:
    def __init__(self, config):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego del Carrito con AVL")
        self.clock = pygame.time.Clock()
        self.config = config

        # Carrito
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

        # Obstáculos
        data = read_json("config/obstacles.json")
        self.obstacles = [Obstacle(obs) for obs in data["obstacles"]]

    def run(self):
        running = True
        dx = self.car.get_speed_x() or 5

        while running:
            self.screen.fill((150, 150, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Control del carrito
            keys = pygame.key.get_pressed()
            if not self.car.is_jumping():
                if keys[pygame.K_UP]:
                    self.car_controller.move_up()
                if keys[pygame.K_DOWN]:
                    self.car_controller.move_down()
                if keys[pygame.K_SPACE]:
                    self.car.set_jumping(True)

            self.car_controller.jump()

            # Dibujar carretera
            self.road_offset -= dx
            if self.road_offset <= -self.WIDTH:
                self.road_offset = 0
            pygame.draw.rect(self.screen, (100, 100, 100), (self.road_offset, 200, self.WIDTH, 200))
            pygame.draw.rect(self.screen, (100, 100, 100), (self.road_offset + self.WIDTH, 200, self.WIDTH, 200))

            # Obstáculos
            for obs in self.obstacles:
                obs.update(dx)
                obs.draw(self.screen)
                if (not self.car.is_jumping() and
                        self.car.get_collision_rect().colliderect(obs.rect) and
                        not obs.hit):
                    self.car.decrease_energy(obs.damage)
                    obs.hit = True

            # Dibujar carrito
            car_img = self.red_car if self.car.is_jumping() else self.blue_car
            self.screen.blit(car_img, (self.car.get_x1(), self.car.get_y1() + self.car.get_jump_offset()))

            # Mostrar energía
            font = pygame.font.SysFont(None, 30)
            energy_text = font.render(f"Energía: {self.car.get_energy()}%", True, (0, 0, 0))
            self.screen.blit(energy_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()