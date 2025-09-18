import pygame

class CarController:
    def __init__(self, car_model):
        self.car = car_model
        self.jump_count = self.car.get_jump_height()
        self.last_move_time = pygame.time.get_ticks()

    def move_up(self):
        dy = self.car.get_speed_y()
        self.car.set_y1(self.car.get_y1() - dy)
        self.car.set_y2(self.car.get_y2() - dy)

    def move_down(self):
        dy = self.car.get_speed_y()
        self.car.set_y1(self.car.get_y1() + dy)
        self.car.set_y2(self.car.get_y2() + dy)

    def move_forward(self):
        """
        Avanza automáticamente en el eje X según refresh_time.
        """
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= self.car.get_refresh_time():
            dx = self.car.get_speed_x()
            self.car.set_x1(self.car.get_x1() + dx)
            self.car.set_x2(self.car.get_x2() + dx)
            self.last_move_time = now

    def jump(self):
        if self.car.is_jumping():
            if self.jump_count >= -self.car.get_jump_height():
                neg = 1 if self.jump_count >= 0 else -1
                dy = (self.jump_count ** 2) * 0.05 * neg
                self.car.set_y1(self.car.get_y1() - dy)
                self.car.set_y2(self.car.get_y2() - dy)
                self.jump_count -= 1
            else:
                self.car.set_jumping(False)
                self.jump_count = self.car.get_jump_height()

    def collide(self, obstacle, obstacle_types):
        tipo = obstacle.get_obstacle()
        damage = obstacle_types.get(tipo, 0)
        self.car.set_energy(self.car.get_energy() - damage)
        print(f"⚡ Colisión con {tipo}, energía restante: {self.car.get_energy()}%")