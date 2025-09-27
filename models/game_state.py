class GameState:
    """
    Represents the overall state of the game (e.g., the road scenario).

    Attributes:
        distance (int | float): The distance covered or remaining in the game.
        car (Car): The car object controlled by the player.
        obstacles_tree (AVLTree): AVL tree containing obstacles on the road.
        is_running (bool): Flag indicating whether the game is currently active.
    """

    def __init__(self, distance, car, obstacles_tree):
        """
        Initialize the game state.

        Args:
            distance (int | float): Initial game distance.
            car (Car): The car object controlled by the player.
            obstacles_tree (AVLTree): Tree structure storing obstacles.
        """
        self.distance = distance
        self.car = car
        self.obstacles_tree = obstacles_tree
        self.is_running = True