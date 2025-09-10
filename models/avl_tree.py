class AVLNode:
    """
    Nodo del árbol AVL que representa un obstáculo en el juego.
    Cada obstáculo ocupa un área rectangular definida por coordenadas.
    """
    def __init__(self, x_min, y_min, x_max, y_max, obstacle):
        self._x_min = x_min      # Coordenada izquierda del obstáculo
        self._y_min = y_min      # Coordenada inferior
        self._x_max = x_max      # Coordenada derecha
        self._y_max = y_max      # Coordenada superior
        self.obstacle = obstacle        # Tipo de obstáculo (ej: roca, hueco, barrera)

        # Atributos para AVL
        self._height = 1
        self._left = None
        self._right = None

    # ------------------------
    # Getters
    # ------------------------
    def get_x_min(self): return self._x_min
    def get_y_min(self): return self._y_min
    def get_x_max(self): return self._x_max
    def get_y_max(self): return self._y_max
    def get_tipo(self): return self._tipo
    def get_height(self): return self._height
    def get_left(self): return self._left
    def get_right(self): return self._right

    # ------------------------
    # Setters
    # ------------------------
    def set_x_min(self, value): self._x_min = value
    def set_y_min(self, value): self._y_min = value
    def set_x_max(self, value): self._x_max = value
    def set_y_max(self, value): self._y_max = value
    def set_tipo(self, value): self._tipo = value
    def set_height(self, value): self._height = value
    def set_left(self, node): self._left = node
    def set_right(self, node): self._right = node


class AVLTree:
    """
    Árbol AVL que almacena obstáculos del juego.
    El criterio de comparación para insertar/balancear es:
    - Primero x_min
    - En caso de empate, y_min
    """
    def __init__(self):
        self._root = None

    # Getter y Setter para la raíz
    def get_root(self): return self._root
    def set_root(self, node): self._root = node
