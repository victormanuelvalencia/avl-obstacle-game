import pygame

class CarController:
    def __init__(self, car_model):
        self.car = car_model
        self.last_move_time = pygame.time.get_ticks()
        self.jumping_up = True       # El próximo salto empieza subiendo
        self.jump_progress = 0

    def move_up(self):
        dy = self.car.get_speed_y()
        self.car.set_y1(self.car.get_y1() - dy)
        self.car.set_y2(self.car.get_y2() - dy)

    def move_down(self):
        dy = self.car.get_speed_y()
        self.car.set_y1(self.car.get_y1() + dy)
        self.car.set_y2(self.car.get_y2() + dy)

    def move_forward(self):
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= self.car.get_refresh_time():
            dx = self.car.get_speed_x()
            self.car.set_x1(self.car.get_x1() + dx)
            self.car.set_x2(self.car.get_x2() + dx)
            self.last_move_time = now

    def jump(self):
        if self.car.is_jumping():
            if self.jumping_up:
                self.jump_progress += self.car.get_speed_y()
                if self.jump_progress >= self.car.get_jump_height():
                    self.jump_progress = self.car.get_jump_height()
                    self.jumping_up = False
            else:
                self.jump_progress -= self.car.get_speed_y()
                if self.jump_progress <= 0:
                    self.jump_progress = 0
                    self.car.set_jumping(False)
                    self.jumping_up = True

            # Solo visual
            self.car.set_jump_offset(-self.jump_progress)
        else:
            self.jump_progress = 0
            self.car.set_jump_offset(0)
            self.jumping_up = True

    def collide(self, obstacle, obstacle_types):
        tipo = obstacle.get_obstacle()
        damage = obstacle_types.get(tipo, 0)
        self.car.set_energy(max(self.car.get_energy() - damage, 0))
        print(f"⚡ Colisión con {tipo}, energía restante: {self.car.get_energy()}%")