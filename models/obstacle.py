import pygame

class Obstacle:
    """
    Representa un obstáculo en la carretera.
    Contiene:
      - type: tipo del obstáculo (cone, rock, oil, etc.)
      - image: sprite cargado y escalado
      - rect: área rectangular (posición y tamaño) para colisiones
      - init_x1, init_y1: coordenadas iniciales fijas para AVL
    """

    def __init__(self, data: dict):
        self.type = data["type"]
        self.hit = False

        # Coordenadas iniciales (para AVL)
        self.init_x1 = data["x1"]
        self.init_y1 = data["y1"]

        # Daño según tipo
        damage_map = {
            "cone": 5,
            "rock": 15,
            "oil": 10,
            "hole": 20,
            "barrera": 12
        }
        self.damage = damage_map.get(self.type, 10)

        # Crear rectángulo
        x1, y1, x2, y2 = data["x1"], data["y1"], data["x2"], data["y2"]
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)

        # Cargar y escalar imagen
        self.image = pygame.image.load(data["sprite"]).convert_alpha()
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
