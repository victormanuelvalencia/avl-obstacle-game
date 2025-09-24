import pygame

class Obstacle:
    """
    Representa un obstáculo en la carretera.
    Cada obstáculo tiene:
      - type: tipo (cone, rock, hole, etc.)
      - image: sprite cargado y escalado
      - rect: área rectangular de colisión
    """

    def __init__(self, data: dict):
        """
        data: diccionario cargado desde settings.json con:
        {
          "type": "cone",
          "sprite": "views/assets/cone.png",
          "x1": 200,
          "y1": 100,
          "x2": 250,
          "y2": 150
        }
        """
        self.type = data["type"]
        self.hit = False

        # Asignar daño según tipo de obstáculo
        damage_map = {
            "cone": 5,
            "rock": 15,
            "oil": 10,
            "hole": 20,
            "barrera": 12
        }
        self.damage = damage_map.get(self.type, 10)  # daño por defecto 10

        # Cargar imagen
        self.image = pygame.image.load(data["sprite"]).convert_alpha()

        # Rectángulo de colisión
        x1, y1, x2, y2 = data["x1"], data["y1"], data["x2"], data["y2"]
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)

        # Escalar la imagen al tamaño del rectángulo
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def update(self, dx: int):
        self.rect.x -= dx

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def to_dict(self):
        return {
            "type": self.type,
            "x1": self.rect.left,
            "y1": self.rect.top,
            "x2": self.rect.right,
            "y2": self.rect.bottom
        }