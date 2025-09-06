class AVLNode:
    """
    Nodo del árbol AVL
    """
    def __init__(self, key, data=None):
        self.key = key        # Coordenada (x, y)
        self.data = data      # Objeto asociado (ej: obstáculo)
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    """
    Implementación del Árbol AVL para gestionar obstáculos
    """
    def __init__(self):
        self.root = None

    # ------------------------
    # Inserción
    # ------------------------
    def insert(self, key, data=None):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data=None):
        pass

    # ------------------------
    # Eliminación
    # ------------------------
    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        pass

    def _get_min(self, node):
        pass

    # ------------------------
    # Recorridos en profundidad (DFS)
    # ------------------------
    def inorder(self):
        pass

    def _inorder(self, node, result):
        pass

    def preorder(self):
        pass

    def _preorder(self, node, result):
        pass

    def postorder(self):
        pass

    def _postorder(self, node, result):
        pass

    # ------------------------
    # Recorrido en anchura (BFS)
    # ------------------------
    def breadth_first(self):
        pass

    # ------------------------
    # Consulta en rango
    # ------------------------
    def range_query(self, x_min, x_max, y_min, y_max):
        pass

    def _range_query(self, node, x_min, x_max, y_min, y_max, result):
        pass

    # ------------------------
    # Funciones de balanceo
    # ------------------------
    def _height(self, node):
        pass

    def _balance_factor(self, node):
        pass

    def _rotate_left(self, node):
        pass

    def _rotate_right(self, node):
        pass

    def _balance(self, node):
        pass

