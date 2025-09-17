class Car:
    """
    Modelo del carrito (solo estado y configuración).
    """
    def __init__(self,
                 x_min=0, y_min=0, x_max=50, y_max=30,
                 energy=100,
                 speed_x=5, refresh_time=200, speed_y=5,
                 jump_height=80, color=(0, 0, 255)):
        self._x_min = x_min
        self._y_min = y_min
        self._x_max = x_max
        self._y_max = y_max
        self._energy = energy
        self._speed_x = speed_x
        self._refresh_time = refresh_time
        self._speed_y = speed_y
        self._jump_height = jump_height
        self._color = color
        self._is_jumping = False

    # --- Getters ---
    def get_x_min(self): return self._x_min
    def get_y_min(self): return self._y_min
    def get_x_max(self): return self._x_max
    def get_y_max(self): return self._y_max
    def get_energy(self): return self._energy
    def get_speed_x(self): return self._speed_x
    def get_refresh_time(self): return self._refresh_time
    def get_speed_y(self): return self._speed_y
    def get_jump_height(self): return self._jump_height
    def get_color(self): return self._color
    def is_jumping(self): return self._is_jumping

    # --- Setters ---
    def set_x_min(self, value): self._x_min = value
    def set_y_min(self, value): self._y_min = value
    def set_x_max(self, value): self._x_max = value
    def set_y_max(self, value): self._y_max = value
    def set_energy(self, value): self._energy = value
    def set_speed_x(self, value): self._speed_x = value
    def set_refresh_time(self, value): self._refresh_time = value
    def set_speed_y(self, value): self._speed_y = value
    def set_jump_height(self, value): self._jump_height = value
    def set_color(self, value): self._color = value
    def set_jumping(self, value): self._is_jumping = value
