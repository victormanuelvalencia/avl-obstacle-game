from models.avl_tree import AVLNode, AVLTree
from models.obstacle import Obstacle


class AVLTreeController:
    def __init__(self, tree: AVLTree):
        self.tree = tree

    # Altura y balance
    def _height(self, node):
        return node.get_height() if node else 0

    def _update_height(self, node):
        if node:
            node.set_height(1 + max(self._height(node.get_left()), self._height(node.get_right())))

    def _balance_factor(self, node):
        return self._height(node.get_left()) - self._height(node.get_right()) if node else 0

    # Búsqueda
    def search(self, x1, y1):
        def _search(node):
            if not node:
                return None
            if (x1, y1) == (node.get_x1(), node.get_y1()):
                return node
            if (x1, y1) < (node.get_x1(), node.get_y1()):
                return _search(node.get_left())
            return _search(node.get_right())
        return _search(self.tree.get_root())

    # Inserción
    def insert(self, x1, y1, x2, y2, obstacle):
        if self.search(x1, y1):
            print(f"⚠️ Obstacle at ({x1}, {y1}) already exists.")
            return
        new_node = AVLNode(x1, y1, x2, y2, obstacle)
        self.tree.set_root(self._insert(self.tree.get_root(), new_node, parent=None))

    def _insert(self, root, new_node, parent):
        if not root:
            new_node.set_parent(parent)
            return new_node
        if (new_node.get_x1(), new_node.get_y1()) < (root.get_x1(), root.get_y1()):
            root.set_left(self._insert(root.get_left(), new_node, root))
        else:
            root.set_right(self._insert(root.get_right(), new_node, root))
        self._update_height(root)
        return self._rebalance(root)


    # Rotaciones
    def _rotate_left(self, node):
        y = node.get_right()
        node.set_right(y.get_left())
        if y.get_left(): y.get_left().set_parent(node)
        y.set_left(node)
        y.set_parent(node.get_parent())
        node.set_parent(y)
        self._update_height(node)
        self._update_height(y)
        if y.get_parent():
            if y.get_parent().get_left() == node:
                y.get_parent().set_left(y)
            else:
                y.get_parent().set_right(y)
        else:
            self.tree.set_root(y)
        return y

    def _rotate_right(self, node):
        y = node.get_left()
        node.set_left(y.get_right())
        if y.get_right(): y.get_right().set_parent(node)
        y.set_right(node)
        y.set_parent(node.get_parent())
        node.set_parent(y)
        self._update_height(node)
        self._update_height(y)
        if y.get_parent():
            if y.get_parent().get_left() == node:
                y.get_parent().set_left(y)
            else:
                y.get_parent().set_right(y)
        else:
            self.tree.set_root(y)
        return y

    # Rebalance
    def _rebalance(self, node):
        balance = self._balance_factor(node)
        if balance > 1:
            if self._balance_factor(node.get_left()) < 0:
                node.set_left(self._rotate_left(node.get_left()))
            return self._rotate_right(node)
        if balance < -1:
            if self._balance_factor(node.get_right()) > 0:
                node.set_right(self._rotate_right(node.get_right()))
            return self._rotate_left(node)
        return node

    def _rebalance_upwards(self, node):
        while node:
            self._update_height(node)
            node = self._rebalance(node).get_parent()

    # Eliminación
    def delete(self, x1, y1):
        node = self.search(x1, y1)
        if node:
            self._delete(node)
        else:
            print(f"⚠️ Node at ({x1}, {y1}) not found.")

    def _delete(self, node):
        def _replace(old, new):
            parent = old.get_parent()
            if not parent:
                self.tree.set_root(new)
            elif old == parent.get_left():
                parent.set_left(new)
            else:
                parent.set_right(new)
            if new: new.set_parent(parent)

        if node.get_left() and node.get_right():
            pred = node.get_left()
            while pred.get_right(): pred = pred.get_right()
            if pred.get_parent() != node:
                _replace(pred, pred.get_left())
                pred.set_left(node.get_left())
                pred.get_left().set_parent(pred)
            _replace(node, pred)
            pred.set_right(node.get_right())
            pred.get_right().set_parent(pred)
        else:
            child = node.get_left() or node.get_right()
            _replace(node, child)
        self._rebalance_upwards(node.get_parent())

    # Recorridos
    def inorder(self):
        def _inorder(node):
            if not node: return []
            return _inorder(node.get_left()) + [(node.get_x1(), node.get_y1())] + _inorder(node.get_right())
        return _inorder(self.tree.get_root())

    def preorder(self):
        def _preorder(node):
            if not node: return []
            return [(node.get_x1(), node.get_y1())] + _preorder(node.get_left()) + _preorder(node.get_right())
        return _preorder(self.tree.get_root())

    def postorder(self):
        def _postorder(node):
            if not node: return []
            return _postorder(node.get_left()) + _postorder(node.get_right()) + [(node.get_x1(), node.get_y1())]
        return _postorder(self.tree.get_root())

    # Range Query--
    def range_query(self, x1, x2, y1, y2):
        result = []

        def _range(node):
            if not node: return
            if node.get_x1() > x1: _range(node.get_left())
            if x1 <= node.get_x1() <= x2 and y1 <= node.get_y1() <= y2:
                result.append({
                    "x1": node.get_x1(), "y1": node.get_y1(),
                    "x2": node.get_x2(), "y2": node.get_y2(),
                    "tipo": node.get_obstacle()
                })
            if node.get_x1() < x2: _range(node.get_right())

        _range(self.tree.get_root())
        return result

    def print_range_query(self, x1, x2, y1, y2):
        results = self.range_query(x1, x2, y1, y2)
        print(f"\n🔎 Obstáculos en x=[{x1},{x2}], y=[{y1},{y2}]:")
        if not results: print(" (Ninguno encontrado)"); return
        for obs in results:
            print(f" - {obs['tipo']} | ({obs['x1']},{obs['y1']}) - ({obs['x2']},{obs['y2']})")

    # Cargar desde lista
    def load_from_list(self, obstacles_list):
        for obs in obstacles_list:
            try:
                obstacle_obj = Obstacle(obs)
                self.insert(obs["x1"], obs["y1"], obs["x2"], obs["y2"], obstacle_obj)
            except Exception as e:
                print(f"[ERROR] No se pudo cargar: {obs} -> {e}")