import pygame

class CarController:
    """
    Controller for moving a Car object within vertical road limits.
    Handles upward, downward, forward movement, and jumping logic.
    """

    def __init__(self, car_model, road_y=None, road_height=None):
        """
        Initialize the CarController.

        Args:
            car_model: The Car instance to control.
            road_y: Optional Y-coordinate of the road's top boundary.
            road_height: Optional height of the road area.
        """
        self.car = car_model
        self.last_move_time = pygame.time.get_ticks()
        self.jumping_up = True
        self.jump_progress = 0

        # Determine vertical movement limits
        car_height = self.car.get_y2() - self.car.get_y1()
        if road_y is not None and road_height is not None:
            self.min_y = road_y
            self.max_y = road_y + road_height - car_height
        else:
            self.min_y = 0
            self.max_y = 800 - car_height  # default

    def move_up(self):
        """Move the car upward within road limits."""
        dy = self.car.get_speed_y()
        new_y1 = max(self.min_y, self.car.get_y1() - dy)
        new_y2 = new_y1 + (self.car.get_y2() - self.car.get_y1())
        self.car.set_y1(new_y1)
        self.car.set_y2(new_y2)

    def move_down(self):
        """Move the car downward within road limits."""
        dy = self.car.get_speed_y()
        new_y1 = min(self.max_y, self.car.get_y1() + dy)
        new_y2 = new_y1 + (self.car.get_y2() - self.car.get_y1())
        self.car.set_y1(new_y1)
        self.car.set_y2(new_y2)

    def move_forward(self):
        """
        Move the car forward along the x-axis based on its speed and refresh time.
        Ensures movement occurs only after the refresh interval.
        """
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= self.car.get_refresh_time():
            dx = self.car.get_speed_x()
            self.car.set_x1(self.car.get_x1() + dx)
            self.car.set_x2(self.car.get_x2() + dx)
            self.last_move_time = now

    def jump(self):
        """
        Handle the car's jumping logic.
        Updates vertical jump progress and applies visual offset.
        """
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

            # Only visual offset for jump
            self.car.set_jump_offset(-self.jump_progress)
        else:
            self.jump_progress = 0
            self.car.set_jump_offset(0)
            self.jumping_up = True