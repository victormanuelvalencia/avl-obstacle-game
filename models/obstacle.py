import pygame

class Obstacle:
    """
    Represents an obstacle on the road.

    Attributes:
        type (str): Type of obstacle (e.g., cone, rock, oil, hole, barrera).
        hit (bool): Flag indicating whether the obstacle has been hit.
        init_x1 (int): Initial fixed x-coordinate (used for AVL tree).
        init_y1 (int): Initial fixed y-coordinate (used for AVL tree).
        damage (int): Amount of damage caused by this obstacle.
        rect (pygame.Rect): Rectangle representing position and size for collisions.
        image (pygame.Surface): Loaded and scaled sprite image of the obstacle.
    """

    def __init__(self, data: dict):
        """
        Initialize an obstacle from data.

        Args:
            data (dict): Dictionary containing obstacle information.
                Required keys:
                    - "type" (str): Obstacle type.
                    - "x1", "y1", "x2", "y2" (int): Coordinates of the obstacle.
                    - "sprite" (str): Path to the obstacle image.
        """
        self.type = data["type"]
        self.hit = False

        # Fixed coordinates for AVL usage
        self.init_x1 = data["x1"]
        self.init_y1 = data["y1"]

        # Damage based on type
        damage_map = {
            "cone": 5,
            "rock": 15,
            "oil": 10,
            "hole": 20,
            "barrera": 12
        }
        self.damage = damage_map.get(self.type, 10)

        # Create collision rectangle
        x1, y1, x2, y2 = data["x1"], data["y1"], data["x2"], data["y2"]
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)

        # Load and scale image
        self.image = pygame.image.load(data["sprite"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def update(self, dx: int):
        """
        Move the obstacle along the X-axis (road scrolling).

        Args:
            dx (int): Amount to shift left (positive values scroll left).
        """
        self.rect.x -= dx

    def draw(self, screen):
        """
        Render the obstacle on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        screen.blit(self.image, self.rect)

    def to_dict(self):
        """
        Export obstacle state as a dictionary (e.g., for JSON storage).

        Returns:
            dict: Dictionary with obstacle type and coordinates.
        """
        return {
            "type": self.type,
            "x1": self.rect.left,
            "y1": self.rect.top,
            "x2": self.rect.right,
            "y2": self.rect.bottom
        }