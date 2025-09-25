import pygame

class Obstacle:
    """
    Representa un obstáculo en la carretera.
    Contiene:
      - type: tipo del obstáculo (cone, rock, oil, etc.)
      - image: sprite cargado y escalado
      - rect: área rectangular (posición y tamaño) para colisiones
    """

    def __init__(self, data: dict):
        """
        data: diccionario cargado desde JSON:
        {
          "type": "cone",
          "sprite": "views/assets/cone.png",
          "x1": 200,
          "y1": 150,
          "x2": 250,
          "y2": 200
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
        self.damage = damage_map.get(self.type, 10)

        # Cargar imagen
        self.image = pygame.image.load(data["sprite"]).convert_alpha()

        # Crear rectángulo de colisión a partir de coordenadas
        x1, y1, x2, y2 = data["x1"], data["y1"], data["x2"], data["y2"]
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)

        # Escalar sprite al tamaño del rectángulo
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def update(self, dx: int):
        """Desplazar obstáculo en eje X (scroll de la carretera)."""
        self.rect.x -= dx

    def draw(self, screen):
        """Dibujar en pantalla."""
        screen.blit(self.image, self.rect)

    def to_dict(self):
        """Guardar estado en JSON."""
        return {
            "type": self.type,
            "x1": self.rect.left,
            "y1": self.rect.top,
            "x2": self.rect.right,
            "y2": self.rect.bottom
        }
