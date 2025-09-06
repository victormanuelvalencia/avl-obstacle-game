class Obstacle:
    """
    Representa un obstáculo en la carretera
    """
    def __init__(self, x, y, width, height, damage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = damage  # Energía que resta al carrito
