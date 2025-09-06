class GameState:
    """
    Estado general del juego (Carretera)
    """
    def __init__(self, distance, car, obstacles_tree):
        self.distance = distance
        self.car = car
        self.obstacles_tree = obstacles_tree
        self.is_running = True
