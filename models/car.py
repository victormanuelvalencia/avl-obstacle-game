class Car:
    """
    Representa el carrito controlado por el jugador.
    """
    def __init__(self, x=0, y=0, energy=100):
        self.x = x
        self.y = y
        self.energy = energy
        self.is_jumping = False

    def move_up(self):
        pass

    def move_down(self):
        pass

    def jump(self):
        pass

    def collide(self, obstacle):
        """
        Procesa una colisión con un obstáculo.
        """
        pass
