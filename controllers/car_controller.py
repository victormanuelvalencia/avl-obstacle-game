import pygame

class CarController:
    def __init__(self, car_model):
        self.car = car_model
        self.jump_count = self.car.get_jump_height()
        self.last_move_time = pygame.time.get_ticks()

    def move_up(self):
        dy = self.car.get_speed_y()
        self.car.set_y_min(self.car.get_y_min() - dy)
        self.car.set_y_max(self.car.get_y_max() - dy)

    def move_down(self):
        dy = self.car.get_speed_y()
        self.car.set_y_min(self.car.get_y_min() + dy)
        self.car.set_y_max(self.car.get_y_max() + dy)

    def move_forward(self):
        """
        Avanza automáticamente en el eje X según refresh_time.
        """
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= self.car.get_refresh_time():
            dx = self.car.get_speed_x()
            self.car.set_x_min(self.car.get_x_min() + dx)
            self.car.set_x_max(self.car.get_x_max() + dx)
            self.last_move_time = now

    def jump(self):
        if self.car.is_jumping():
            if self.jump_count >= -self.car.get_jump_height():
                neg = 1 if self.jump_count >= 0 else -1
                dy = (self.jump_count ** 2) * 0.05 * neg
                self.car.set_y_min(self.car.get_y_min() - dy)
                self.car.set_y_max(self.car.get_y_max() - dy)
                self.jump_count -= 1
            else:
                self.car.set_jumping(False)
                self.jump_count = self.car.get_jump_height()

    def collide(self, obstacle, obstacle_types):
        tipo = obstacle.get_obstacle()
        damage = obstacle_types.get(tipo, 0)
        self.car.set_energy(self.car.get_energy() - damage)
        print(f"⚡ Colisión con {tipo}, energía restante: {self.car.get_energy()}%")
