from models.avl_tree import AVLNode, AVLTree

class AVLTreeController:
    def __init__(self, model: AVLTree):
        self.model = model

    # -------------------------
    # ALTURA Y BALANCE
    # -------------------------
    def _height(self, node):
        return node.get_height() if node else 0

    def _update_height(self, node):
        node.set_height(1 + max(self._height(node.get_left()), self._height(node.get_right())))

    def _balance_factor(self, node):
        return self._height(node.get_left()) - self._height(node.get_right()) if node else 0

    # -------------------------
    # ROTACIONES
    # -------------------------
    def _rotate_right(self, z):
        y = z.get_left()
        T3 = y.get_right()

        # Rotar
        y.set_right(z)
        z.set_left(T3)

        # Actualizar alturas
        self._update_height(z)
        self._update_height(y)

        return y  # nueva raíz del subárbol

    def _rotate_left(self, z):
        y = z.get_right()
        T2 = y.get_left()

        # Rotar
        y.set_left(z)
        z.set_right(T2)

        # Actualizar alturas
        self._update_height(z)
        self._update_height(y)

        return y  # nueva raíz del subárbol

    # -------------------------
    # COMPARADOR DE OBSTÁCULOS
    # -------------------------
    def _compare(self, node_a, node_b):
        """Compara dos nodos según (x_min, y_min)."""
        if node_a.get_x_min() < node_b.get_x_min():
            return -1
        elif node_a.get_x_min() > node_b.get_x_min():
            return 1
        else:
            # Si empatan en x_min, se compara y_min
            if node_a.get_y_min() < node_b.get_y_min():
                return -1
            elif node_a.get_y_min() > node_b.get_y_min():
                return 1
            else:
                return 0  # Coordenadas repetidas → no se permite insertar

    # -------------------------
    # INSERCIÓN
    # -------------------------
    def insert(self, x_min, y_min, x_max, y_max, tipo):
        new_node = AVLNode(x_min, y_min, x_max, y_max, tipo)
        self.model.set_root(self._insert(self.model.get_root(), new_node))

    def _insert(self, root, new_node):
        # Inserción como en BST
        if not root:
            return new_node

        cmp = self._compare(new_node, root)
        if cmp == 0:
            print(f"⚠️ Obstáculo en ({new_node.get_x_min()}, {new_node.get_y_min()}) ya existe.")
            return root
        elif cmp < 0:
            root.set_left(self._insert(root.get_left(), new_node))
        else:
            root.set_right(self._insert(root.get_right(), new_node))

        # Actualizar altura
        self._update_height(root)

        # Balancear
        balance = self._balance_factor(root)

        # Caso Izquierda - Izquierda
        if balance > 1 and self._compare(new_node, root.get_left()) < 0:
            return self._rotate_right(root)

        # Caso Derecha - Derecha
        if balance < -1 and self._compare(new_node, root.get_right()) > 0:
            return self._rotate_left(root)

        # Caso Izquierda - Derecha
        if balance > 1 and self._compare(new_node, root.get_left()) > 0:
            root.set_left(self._rotate_left(root.get_left()))
            return self._rotate_right(root)

        # Caso Derecha - Izquierda
        if balance < -1 and self._compare(new_node, root.get_right()) < 0:
            root.set_right(self._rotate_right(root.get_right()))
            return self._rotate_left(root)

        return root

    # -------------------------
    # RECORRIDO POSTORDER
    # -------------------------
    def postorder(self):
        """
        Punto de entrada al recorrido postorder.
        Llama a la función recursiva comenzando desde la raíz.
        """
        root = self.model.get_root()
        return self._postorder(root)

    def _postorder(self, node):
        """
        Función recursiva que realiza el recorrido postorder.
        """
        if node is None:
            return []

        # Recursión sobre subárbol izquierdo
        left = self._postorder(node.get_left())

        # Recursión sobre subárbol derecho
        right = self._postorder(node.get_right())

        # Nodo actual al final
        current = [f"({node.get_x_min()}, {node.get_y_min()})"]

        return left + right + current

    # -------------------------
    # RECORRIDO INORDER
    # -------------------------
    def inorder(self):
        """
        Punto de entrada al recorrido inorder.
        Llama a la función recursiva comenzando desde la raíz.
        """
        root = self.model.get_root()
        return self._inorder(root)

    def _inorder(self, node):
        """
        Función recursiva que realiza el recorrido inorder.
        """
        if node is None:
            return []

        # Recursión sobre subárbol izquierdo
        left = self._inorder(node.get_left())

        # Nodo actual
        current = [f"({node.get_x_min()}, {node.get_y_min()})"]

        # Recursión sobre subárbol derecho
        right = self._inorder(node.get_right())

        return left + current + right

    # -------------------------
    # RECORRIDO PREORDER
    # -------------------------
    def preorder(self):
        """
        Punto de entrada al recorrido preorder.
        """
        root = self.model.get_root()
        return self._preorder_recursive(root)

    def _preorder_recursive(self, node):
        if node is None:
            return []

        current = [f"({node.get_x_min()}, {node.get_y_min()})"]
        left = self._preorder_recursive(node.get_left())
        right = self._preorder_recursive(node.get_right())

        return current + left + right