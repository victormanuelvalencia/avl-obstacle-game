from models.avl_tree import AVLNode, AVLTree
from models.obstacle import Obstacle


class AVLTreeController:
    def __init__(self, tree):
        self.tree = tree

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
    def search(self, x1, y1):
        """
        Search for an obstacle in the tree by coordinates (x1, y1 in case of draw).
        It returns the node if found, otherwise return None.
        """

        # Looking for the root, and if is empty it returns a None
        if self.tree.get_root() is None:
            print("The tree is empty.")
            return None
        else:
            # if there is any root, then it calls the recursive function that will look for the x1 or y1
            # value
            return self._search(self.tree.get_root(), x1, y1)

    def _search(self, current_node: AVLNode, x1, y1):
        # Case: there is no nodes
        if current_node is None:
            return None

        # Case: found the exact same values and return the node
        if (x1 == current_node.get_x1() and
                y1 == current_node.get_y1()):
            return current_node

        # If it doesn't find the values then search in the left subtree
        if (x1 < current_node.get_x1() or
                # in case of x draw
                (x1 == current_node.get_x1() and y1 < current_node.get_y1())):
            return self._search(current_node.get_left(), x1, y1)

        # Otherwise, search in the right subtree
        return self._search(current_node.get_right(), x1, y1)

    # -------------------------
    # Insert
    # -------------------------
    def insert(self, data: dict):
        """
        Inserta un nuevo obstáculo en el árbol AVL.
        data: diccionario cargado del JSON con los campos:
              { "type": "...", "sprite": "...", "x1": .., "y1": .., "x2": .., "y2": .. }
        """
        # Crear obstáculo desde el JSON
        obstacle_obj = Obstacle(data)

        # Revisar si ya existe un nodo con esas coordenadas
        node = self.search(obstacle_obj.rect.left, obstacle_obj.rect.top)
        if node is not None:
            print(f"⚠️ Obstacle at ({obstacle_obj.rect.left}, {obstacle_obj.rect.top}) already exists.")
            return

        # Crear el nuevo nodo AVL
        new_node = AVLNode(obstacle_obj)

        # Caso base: árbol vacío
        if self.tree.get_root() is None:
            self.tree.set_root(new_node)
        else:
            root = self.tree.get_root()
            root = self._insert(root, new_node, parent=None)
            self.tree.set_root(root)

    def _insert(self, root: AVLNode, new_node: AVLNode, parent: AVLNode):
        # Caso base: espacio vacío → insertar aquí
        if root is None:
            new_node.set_parent(parent)
            return new_node

        # Comparación por (x1, y1)
        if (new_node.get_x1() < root.get_x1() or
                (new_node.get_x1() == root.get_x1() and new_node.get_y1() < root.get_y1())):
            root.set_left(self._insert(root.get_left(), new_node, root))
        else:
            root.set_right(self._insert(root.get_right(), new_node, root))

        # Actualizar altura del nodo actual
        self._update_height(root)

        # Rebalancear si es necesario
        return self._rebalance(root)

    # -------------------------
    # Delete
    # -------------------------

    def delete(self, x1, y1):
        """
        Elimina el nodo con coordenadas (x1, y1).
        """
        node = self.search(x1, y1)
        if node is None:
            print(f"⚠️ Node at ({x1}, {y1}) not found.")
            return
        self._delete(node)

    def _delete(self, node: AVLNode):
        # --- Caso 1: nodo hoja ---
        if node.get_left() is None and node.get_right() is None:
            self._replace_node(node, None)

        # --- Caso 2: nodo con dos hijos ---
        elif node.get_left() is not None and node.get_right() is not None:
            predecessor = self._get_predecessor(node)

            if predecessor.get_parent() != node:
                self._replace_node(predecessor, predecessor.get_left())
                predecessor.set_left(node.get_left())
                if predecessor.get_left():
                    predecessor.get_left().set_parent(predecessor)

            self._replace_node(node, predecessor)
            predecessor.set_right(node.get_right())
            if predecessor.get_right():
                predecessor.get_right().set_parent(predecessor)

        # --- Caso 3: nodo con un solo hijo ---
        else:
            child = node.get_left() if node.get_left() else node.get_right()
            self._replace_node(node, child)

        # Rebalancear hacia arriba
        self._rebalance_upwards(node.get_parent())
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
            self.tree.set_root(new_node)
        elif old_node == parent.get_left():
            parent.set_left(new_node)
        else:
            parent.set_right(new_node)

        if new_node is not None:
            new_node.set_parent(parent)



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
            self.tree.set_root(y)

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
            self.tree.set_root(y)

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
        root = self.tree.get_root()
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
        current = [f"({node.get_x1()}, {node.get_y1()})"]

        return left + right + current

    # -------------------------
    # RECORRIDO INORDER
    # -------------------------
    def inorder(self):
        """
        Punto de entrada al recorrido inorder.
        Llama a la función recursiva comenzando desde la raíz.
        """
        root = self.tree.get_root()
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
        current = [f"({node.get_x1()}, {node.get_y1()})"]

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
        root = self.tree.get_root()
        return self._preorder_recursive(root)

    def _preorder_recursive(self, node):
        if node is None:
            return []

        current = [f"({node.get_x1()}, {node.get_y1()})"]
        left = self._preorder_recursive(node.get_left())
        right = self._preorder_recursive(node.get_right())

        return current + left + right

    def range_query(self, x1, x2, y1, y2):
        """
        Devuelve una lista de nodos (o coordenadas) cuyos (x1, y1)
        estén dentro del rango definido por:
        x1 <= nodo.x1 <= x2
        y1 <= nodo.y1 <= y2
        """
        result = []
        self._range_query(self.tree.get_root(), x1, x2, y1, y2, result)
        return result

    def _range_query(self, node, x1, x2, y1, y2, result):
        if not node:
            return

        # Si todo el subárbol izquierdo está fuera del rango por la derecha
        if node.get_x1() > x1:
            self._range_query(node.get_left(), x1, x2, y1, y2, result)

        # --- Verificar si el nodo actual está dentro del rango ---
        if (x1 <= node.get_x1() <= x2) and (y1 <= node.get_y1() <= y2):
            result.append({
                "x1": node.get_x1(),
                "y1": node.get_y1(),
                "x2": node.get_x2(),
                "y2": node.get_y2(),
                "tipo": node.get_obstacle()
            })

        # Si todo el subárbol derecho está fuera del rango por la izquierda
        if node.get_x1() < x2:
            self._range_query(node.get_right(), x1, x2, y1, y2, result)

    def print_range_query(self, x1, x2, y1, y2):
        """Imprime los obstáculos dentro del rango dado."""
        resultados = self.range_query(x1, x2, y1, y2)

        print(f"\n🔎 Obstáculos en el rango x=[{x1}, {x2}], y=[{y1}, {y2}]:")
        if not resultados:
            print(" (Ninguno encontrado)")
            return

        for obs in resultados:
            print(f" - Objeto: {obs['tipo']} | Coords: ({obs['x1']}, {obs['y1']}) "
                  f"- ({obs['x2']}, {obs['y2']})")

    # -------------------------
    # Load the nodes from the json
    # -------------------------


    def load_from_list(self, obstacles_list):
        for obs in obstacles_list:
            try:
                self.insert(obs)  # 👈 ahora insert recibe directamente el diccionario
            except Exception as e:
                print(f"[ERROR] No se pudo cargar obstáculo: {obs} -> {e}")
