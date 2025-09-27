import pygame

class Car:
    """
    Represents a car in the game with position, speed, energy, and jump behavior.

    Attributes:
        _x1 (int): Left x-coordinate of the car.
        _y1 (int): Top y-coordinate of the car.
        _x2 (int): Right x-coordinate of the car.
        _y2 (int): Bottom y-coordinate of the car.
        _energy (int): Remaining energy of the car.
        _speed_x (int): Horizontal movement speed.
        _refresh_time (int): Refresh rate for updates (in ms).
        _speed_y (int): Vertical movement speed.
        _jump_height (int): Maximum height of a jump.
        _color (tuple[int, int, int]): RGB color of the car.
        _is_jumping (bool): Whether the car is currently jumping.
        _jump_offset (int): Vertical offset applied during a jump.

    Note:
        This class provides standard getters and setters for
        position, energy, speed, jump parameters, and color.
    """

    def __init__(self,
                 x1=0, y1=0, x2=50, y2=30,
                 energy=100,
                 speed_x=1, refresh_time=200, speed_y=1,
                 jump_height=80, color=(0, 0, 255)):
        """
        Initialize a Car instance.

        Args:
            x1 (int, optional): Left x-coordinate. Defaults to 0.
            y1 (int, optional): Top y-coordinate. Defaults to 0.
            x2 (int, optional): Right x-coordinate. Defaults to 50.
            y2 (int, optional): Bottom y-coordinate. Defaults to 30.
            energy (int, optional): Initial energy. Defaults to 100.
            speed_x (int, optional): Horizontal speed. Defaults to 1.
            refresh_time (int, optional): Refresh rate (ms). Defaults to 200.
            speed_y (int, optional): Vertical speed. Defaults to 1.
            jump_height (int, optional): Maximum jump height. Defaults to 80.
            color (tuple[int, int, int], optional): RGB color. Defaults to blue.
        """
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

    # --- General Getters ---
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

    # --- General Setters ---
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

    def get_collision_rect(self):
        """
        Get the dynamic collision rectangle of the car.

        Note:
            Always returns the base rectangle of the car,
            ignoring the visual jump offset.

        Returns:
            pygame.Rect: Rectangle representing the car's collision area.
        """
        width = self._x2 - self._x1
        height = self._y2 - self._y1
        return pygame.Rect(self._x1, self._y1, width, height)

    def decrease_energy(self, amount):
        """
        Decrease the car's energy by a given amount.

        Args:
            amount (int): Value to subtract from the current energy.

        Note:
            The energy value will not go below zero.
        """
        self._energy = max(self._energy - amount, 0)