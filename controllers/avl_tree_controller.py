from models.avl_tree import AVLNode, AVLTree

class AVLTreeController:
    def __init__(self, model: AVLTree):
        self.model = model

    # -------------------------
    # ALTURA Y BALANCE
    # -------------------------
    def _height(self, node):
        # If the node does not exist, its height is 0
        if node is None:
            return 0
        # Otherwise, return the height stored in the node
        return node.get_height()

    def _update_height(self, node):
        if node is None:
            return

        # Get the height of the left and right children
        left_height = self._height(node.get_left())
        right_height = self._height(node.get_right())

        # Update this node's height as 1 + the maximum child height
        new_height = 1 + max(left_height, right_height)
        node.set_height(new_height)

    def _balance_factor(self, node):
        if node is None:
            return 0

        # Calculate height difference: left - right
        left_height = self._height(node.get_left())
        right_height = self._height(node.get_right())
        return left_height - right_height

    # ------------------------
    # Search
    # ------------------------
    def search(self, x_min, y_min):
        """
        Search for an obstacle in the tree by coordinates (x_min, y_min in case of draw).
        It returns the node if found, otherwise return None.
        """

        # Looking for the root, and if is empty it returns a None
        if self.model.get_root() is None:
            print("The tree is empty.")
            return None
        else:
            # if there is any root, then it calls the recursive function that will look for the x_min or y_min
            # value
            return self._search(self.model.get_root(), x_min, y_min)

    def _search(self, current_node, x_min, y_min):
        # Case: there is no nodes
        if current_node is None:
            return None

        # Case: found the exact same values and return the node
        if (x_min == current_node.get_x_min() and
                y_min == current_node.get_y_min()):
            return current_node

        # If it doesn't find the values then search in the left subtree
        if (x_min < current_node.get_x_min() or
                # in case of x draw
                (x_min == current_node.get_x_min() and y_min < current_node.get_y_min())):
            return self._search(current_node.get_left(), x_min, y_min)

        # Otherwise, search in the right subtree
        return self._search(current_node.get_right(), x_min, y_min)

    # -------------------------
    # Insert
    # -------------------------
    def insert(self, x_min, y_min, x_max, y_max, obstacle):
        # Searching if it already exists
        node = self.search(x_min, y_min)

        if node is not None:
            print(f"⚠️ Obstacle at ({x_min}, {y_min}) already exists.")
            return
        else:
            # If it doesn't exist, then create the new node
            new_node = AVLNode(x_min, y_min, x_max, y_max, obstacle)

            # If root is empty, insert here the new node
            if self.model.get_root() is None:
                self.model.set_root(new_node)
            else:
                # If there is a root, the calls Recursive insert
                root = self.model.get_root()
                # From the root to the leafs
                root = self._insert(root, new_node, parent = None)
                # This is in case we need a rebalance, we update the new root
                self.model.set_root(root)

    def _insert(self, root, new_node: AVLNode, parent: AVLNode):
        # Caso base: espacio vacío → insertar aquí
        if not root:
            new_node.set_parent(parent)  # 👈 asignamos el padre
            return new_node

        # Comparación por (x_min, y_min)
        if (new_node.get_x_min() < root.get_x_min() or
                (new_node.get_x_min() == root.get_x_min() and new_node.get_y_min() < root.get_y_min())):
            root.set_left(self._insert(root.get_left(), new_node, root))
        else:
            root.set_right(self._insert(root.get_right(), new_node, root))

        # Actualizar altura
        self._update_height(root)

        # Rebalancear
        return self._rebalance(root)

    # -------------------------
    # Rebalance (insertion)
    # -------------------------
    def _rebalance(self, node):
        """
        Checks the balance factor of a node and applies the proper rotation if needed.
        Uses the idea of "high node", "middle node", and "low node" for clarity.
        """

        # Calculate balance factor
        balance = self._balance_factor(node)

        # -------------------------
        # CASE 1: Left-Left (balance > 1 and new node is in the left subtree of the left child)
        # -------------------------
        if balance > 1 and self._balance_factor(node.get_left()) >= 0:
            # Middle = left child
            middle = node.get_left()
            # High = the node itself
            high = node

            # After rotation:
            # middle becomes the new parent
            # middle.right becomes high.left
            # high becomes right child of middle
            return self._rotate_right(high)

        # -------------------------
        # CASE 2: Right-Right (balance < -1 and new node is in the right subtree of the right child)
        # -------------------------
        if balance < -1 and self._balance_factor(node.get_right()) <= 0:
            # Middle = right child
            middle = node.get_right()
            # High = the node itself
            high = node

            # After rotation:
            # middle becomes the new parent
            # middle.left becomes high.right
            # high becomes left child of middle
            return self._rotate_left(high)

        # -------------------------
        # CASE 3: Left-Right (balance > 1 and new node is in the right subtree of the left child)
        # -------------------------
        if balance > 1 and self._balance_factor(node.get_left()) < 0:
            # High = node
            high = node
            # Middle = left child
            middle = node.get_left()
            # Low = right child of middle
            low = middle.get_right()

            # Step 1: rotate middle -> left
            high.set_left(self._rotate_left(middle))
            # Step 2: rotate high -> right
            return self._rotate_right(high)

        # -------------------------
        # CASE 4: Right-Left (balance < -1 and new node is in the left subtree of the right child)
        # -------------------------
        if balance < -1 and self._balance_factor(node.get_right()) > 0:
            # High = node
            high = node
            # Middle = right child
            middle = node.get_right()
            # Low = left child of middle
            low = middle.get_left()

            # Step 1: rotate middle -> right
            high.set_right(self._rotate_right(middle))
            # Step 2: rotate high -> left
            return self._rotate_left(high)

        # If node is already balanced, just return it
        return node

    # -------------------------
    # Predecessor
    # -------------------------

    def _get_predecessor(self, node):
        """Finds the inorder predecessor (max value in left subtree)."""
        current = node.get_left()
        while current.get_right() is not None:
            current = current.get_right()
        return current

    # -------------------------
    # Replace nodes (for deleting)
    # -------------------------

    def _replace_node(self, old_node, new_node):
        """Replaces one subtree with another, updating parent references."""
        parent = old_node.get_parent()

        if parent is None:
            self.model.set_root(new_node)
        elif old_node == parent.get_left():
            parent.set_left(new_node)
        else:
            parent.set_right(new_node)

        if new_node is not None:
            new_node.set_parent(parent)

    # -------------------------
    # Delete
    # -------------------------

    def delete(self, x_min, y_min):
        node = self.search(x_min, y_min)
        if node is None:
            print(f"⚠️ Node at ({x_min}, {y_min}) not found.")
            return
        self._delete(node)

    def _delete(self, node):
        # --- Case 1: node is a leaf ---
        if node.get_left() is None and node.get_right() is None:
            self._replace_node(node, None)

        # --- Case 2: node has two children ---
        elif node.get_left() is not None and node.get_right() is not None:
            predecessor = self._get_predecessor(node)

            # Si el predecesor no es hijo directo del nodo
            if predecessor.get_parent() != node:
                self._replace_node(predecessor, predecessor.get_left())
                predecessor.set_left(node.get_left())
                if predecessor.get_left():
                    predecessor.get_left().set_parent(predecessor)

            self._replace_node(node, predecessor)
            predecessor.set_right(node.get_right())
            if predecessor.get_right():
                predecessor.get_right().set_parent(predecessor)

        # --- Case 3: node has only one child ---
        else:
            child = node.get_left() if node.get_left() else node.get_right()
            self._replace_node(node, child)

        # Rebalance upward
        self._rebalance_upwards(node.get_parent())

# ?????????????

    def _rebalance_upwards(self, node):
        """Traverse upwards from a node and rebalance each ancestor."""
        while node is not None:
            self._update_height(node)
            node = self._rebalance(node)
            node = node.get_parent()

    # -------------------------
    # Ratations
    # -------------------------
    def _rotate_right(self, node):
        y = node.get_left()
        T3 = y.get_right()

        # Rotación
        y.set_right(node)
        node.set_left(T3)

        # Actualizar padres
        y.set_parent(node.get_parent())
        node.set_parent(y)
        if T3:
            T3.set_parent(node)

        # Conectar con el padre original
        if y.get_parent():
            if y.get_parent().get_left() == node:
                y.get_parent().set_left(y)
            else:
                y.get_parent().set_right(y)
        else:
            self.model.set_root(y)

        # Actualizar alturas
        self._update_height(node)
        self._update_height(y)

        return y

    def _rotate_left(self, node):
        y = node.get_right()
        T2 = y.get_left()

        # Rotación
        y.set_left(node)
        node.set_right(T2)

        # Actualizar padres
        y.set_parent(node.get_parent())
        node.set_parent(y)
        if T2:
            T2.set_parent(node)

        # Conectar con el padre original
        if y.get_parent():
            if y.get_parent().get_left() == node:
                y.get_parent().set_left(y)
            else:
                y.get_parent().set_right(y)
        else:
            self.model.set_root(y)

        # Actualizar alturas
        self._update_height(node)
        self._update_height(y)

        return y

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

    def range_query(self, x_min, x_max, y_min, y_max):
        """
        Devuelve una lista de nodos (o coordenadas) cuyos (x_min, y_min)
        estén dentro del rango definido por:
        x_min <= nodo.x_min <= x_max
        y_min <= nodo.y_min <= y_max
        """
        result = []
        self._range_query(self.model.get_root(), x_min, x_max, y_min, y_max, result)
        return result

    def _range_query(self, node, x_min, x_max, y_min, y_max, result):
        if not node:
            return

        # Si todo el subárbol izquierdo está fuera del rango por la derecha
        if node.get_x_min() > x_min:
            self._range_query(node.get_left(), x_min, x_max, y_min, y_max, result)

        # --- Verificar si el nodo actual está dentro del rango ---
        if (x_min <= node.get_x_min() <= x_max) and (y_min <= node.get_y_min() <= y_max):
            result.append({
                "x_min": node.get_x_min(),
                "y_min": node.get_y_min(),
                "x_max": node.get_x_max(),
                "y_max": node.get_y_max(),
                "tipo": node.get_obstacle()
            })

        # Si todo el subárbol derecho está fuera del rango por la izquierda
        if node.get_x_min() < x_max:
            self._range_query(node.get_right(), x_min, x_max, y_min, y_max, result)

    def print_range_query(self, x_min, x_max, y_min, y_max):
        """Imprime los obstáculos dentro del rango dado."""
        resultados = self.range_query(x_min, x_max, y_min, y_max)

        print(f"\n🔎 Obstáculos en el rango x=[{x_min}, {x_max}], y=[{y_min}, {y_max}]:")
        if not resultados:
            print(" (Ninguno encontrado)")
            return

        for obs in resultados:
            print(f" - Objeto: {obs['tipo']} | Coords: ({obs['x_min']}, {obs['y_min']}) "
                  f"- ({obs['x_max']}, {obs['y_max']})")

