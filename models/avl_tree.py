from models.obstacle import Obstacle

class AVLNode:
    """
    Nodo del árbol AVL que representa un obstáculo en el juego.
    Cada obstáculo ocupa un área rectangular definida por coordenadas.
    """
    def __init__(self, x1, x2, y1, y2, obstacle, parent = None):
        self._obstacle = obstacle  # Objeto Obstacle
        self.parent = parent

        # Atributos para AVL
        self._height = 1
        self._left = None
        self._right = None

    """
    Converts the node to dict to save it in json
    """
    def to_dict(self):
        """
        Convierte el nodo a dict (usando el método de Obstacle).
        """
        return self._obstacle.to_dict()

    """
    Build the node from the dict
    """
    @classmethod
    def from_dict(cls, data: dict):
        """
        Construye un nodo AVL a partir de un diccionario (JSON).
        """
        obstacle = Obstacle(data)  # Se crea el objeto Obstacle
        return cls(obstacle)

    # ------------------------
    # Getters
    # ------------------------
    def get_x1(self): return self._obstacle.rect.left
    def get_y1(self): return self._obstacle.rect.top
    def get_x2(self): return self._obstacle.rect.right
    def get_y2(self): return self._obstacle.rect.bottom
    def get_obstacle(self): return self._obstacle
    def get_height(self): return self._height
    def get_left(self): return self._left
    def get_right(self): return self._right
    def get_parent(self): return self.parent

    # ------------------------
    # Setters
    # ------------------------
    def set_height(self, value): self._height = value
    def set_left(self, node): self._left = node
    def set_right(self, node): self._right = node
    def set_parent(self, node): self.parent = node

class AVLTree:
    """
    Árbol AVL que almacena obstáculos del juego.
    El criterio de comparación para insertar/balancear es:
    - Primero x1
    - En caso de empate, y1
    """
    def __init__(self):
        self._root = None

    # Getter y Setter para la raíz
    def get_root(self): return self._root
    def set_root(self, node): self._root = node