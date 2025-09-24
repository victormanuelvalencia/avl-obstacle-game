import pygame

class Car:
    def __init__(self,
                 x1=0, y1=0, x2=50, y2=30,
                 energy=100,
                 speed_x=5, refresh_time=200, speed_y=5,
                 jump_height=80, color=(0, 0, 255)):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._energy = energy
        self._speed_x = speed_x
        self._refresh_time = refresh_time
        self._speed_y = speed_y
        self._jump_height = jump_height
        self._color = color
        self._is_jumping = False
        self._jump_offset = 0

    # Getters
    def get_x1(self): return self._x1
    def get_y1(self): return self._y1
    def get_x2(self): return self._x2
    def get_y2(self): return self._y2
    def get_energy(self): return self._energy
    def get_speed_x(self): return self._speed_x
    def get_refresh_time(self): return self._refresh_time
    def get_speed_y(self): return self._speed_y
    def get_jump_height(self): return self._jump_height
    def get_color(self): return self._color
    def is_jumping(self): return self._is_jumping
    def get_jump_offset(self): return self._jump_offset

    # Setters
    def set_x1(self, value): self._x1 = value
    def set_y1(self, value): self._y1 = value
    def set_x2(self, value): self._x2 = value
    def set_y2(self, value): self._y2 = value
    def set_energy(self, value): self._energy = value
    def set_speed_x(self, value): self._speed_x = value
    def set_refresh_time(self, value): self._refresh_time = value
    def set_speed_y(self, value): self._speed_y = value
    def set_jump_height(self, value): self._jump_height = value
    def set_color(self, value): self._color = value
    def set_jumping(self, value): self._is_jumping = value
    def set_jump_offset(self, value): self._jump_offset = value

    # Rectángulo de colisión dinámico
    def get_collision_rect(self):
        # Siempre devuelve la base del carro, ignorando salto visual
        width = self._x2 - self._x1
        height = self._y2 - self._y1
        return pygame.Rect(self._x1, self._y1, width, height)

    def decrease_energy(self, amount):
        self._energy = max(self._energy - amount, 0)