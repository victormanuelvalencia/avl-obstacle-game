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
            speed_x=config["car_speed"],
            refresh_time=config["refresh_time"],
            speed_y=5,
            jump_height=config["jump_height"],
            color=(0, 0, 255)  # azul por defecto
        )

        # Crear controlador que maneja la lógica
        self.car_controller = CarController(self.car)

        # Colores
        self.base_color = (0, 0, 255)   # Azul
        self.jump_color = (255, 0, 0)   # Rojo

    def run(self):
        running = True
        while running:
            self.screen.fill((200, 200, 200))  # Fondo gris (carretera)

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

            # Movimiento automático
            self.car_controller.move_forward()

            # Salto
            self.car_controller.jump()

            # Dibujar carrito
            color = self.jump_color if self.car.is_jumping() else self.base_color
            rect = pygame.Rect(
                self.car.get_x_min(),
                self.car.get_y_min(),
                self.car.get_x_max() - self.car.get_x_min(),
                self.car.get_y_max() - self.car.get_y_min()
            )
            pygame.draw.rect(self.screen, color, rect)

            # Mostrar energía en pantalla
            font = pygame.font.SysFont(None, 30)
            energy_text = font.render(f"Energía: {self.car.get_energy()}%", True, (0, 0, 0))
            self.screen.blit(energy_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
