import pygame
from models.car import Car
from controllers.car_controller import CarController

class GameView:
    def __init__(self, config):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego del Carrito con AVL")

        self.clock = pygame.time.Clock()

        # Crear modelo del carrito con datos del JSON
        self.car = Car(
            x_min=50,
            y_min=self.HEIGHT // 2,
            x_max=100,
            y_max=(self.HEIGHT // 2) + 30,
            energy=100,
            speed_x=0,
            refresh_time=config["refresh_time"],
            speed_y=5,
            jump_height=config["jump_height"],
        )

        # Crear controlador que maneja la lógica
        self.car_controller = CarController(self.car)

        # Cargar imágenes del carro
        self.blue_car = pygame.image.load("views/assets/blue_car.png").convert_alpha()
        self.red_car = pygame.image.load("views/assets/red_car.png").convert_alpha()

        # Escalar imágenes al tamaño del carro
        width = self.car.get_x_max() - self.car.get_x_min()
        height = self.car.get_y_max() - self.car.get_y_min()
        self.blue_car = pygame.transform.scale(self.blue_car, (width, height))
        self.red_car = pygame.transform.scale(self.red_car, (width, height))

        # Offset para carretera infinita
        self.road_offset = 0

        # Lista de obstáculos
        self.obstacles = []

    def run(self):
        running = True
        spawn_timer = 0  # para controlar aparición de obstáculos

        while running:
            self.screen.fill((150, 150, 150))  # Fondo gris (carretera)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if not self.car.is_jumping():
                if keys[pygame.K_UP]:
                    self.car_controller.move_up()
                if keys[pygame.K_DOWN]:
                    self.car_controller.move_down()
                if keys[pygame.K_SPACE]:
                    self.car.set_jumping(True)

            # Salto
            self.car_controller.jump()

            self.road_offset -= 5
            if self.road_offset <= -self.WIDTH:
                self.road_offset = 0

                pygame.draw.rect(self.screen, (100, 100, 100), (self.road_offset, 200, self.WIDTH, 200))
                pygame.draw.rect(self.screen, (100, 100, 100), (self.road_offset + self.WIDTH, 200, self.WIDTH, 200))

            # Seleccionar imagen según estado
            if self.car.is_jumping():
                car_img = self.red_car
            else:
                car_img = self.blue_car

            # Dibujar carro
            self.screen.blit(car_img, (self.car.get_x_min(), self.car.get_y_min()))

            # Mostrar energía en pantalla
            font = pygame.font.SysFont(None, 30)
            energy_text = font.render(f"Energía: {self.car.get_energy()}%", True, (0, 0, 0))
            self.screen.blit(energy_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

    pygame.quit()
