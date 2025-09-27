from models.avl_tree import AVLNode, AVLTree
from models.obstacle import Obstacle

class AVLTreeController:
    """
    Controller for managing an AVL tree of obstacles.
    Provides insertion, deletion, search, traversal, rebalancing, and range queries.
    """

    def __init__(self, tree):
        """
        Initialize the controller with a given AVL tree.

        Args:
            tree (AVLTree): The AVL tree instance to manage.
        """
        self.tree = tree

    def _height(self, node):
        """Return the height of the node, or 0 if None."""
        if node is None:
            return 0
        return node.get_height()

    def _update_height(self, node):
        """Update the height of the node based on its children's heights."""
        if node is None:
            return
        left_height = self._height(node.get_left())
        right_height = self._height(node.get_right())
        node.set_height(1 + max(left_height, right_height))

    def _balance_factor(self, node):
        """Calculate the balance factor of the node: left_height - right_height."""
        if node is None:
            return 0
        return self._height(node.get_left()) - self._height(node.get_right())

    def search(self, x1, y1):
        """
        Search for an obstacle node by coordinates (x1, y1).

        Args:
            x1 (int): X-coordinate of the obstacle.
            y1 (int): Y-coordinate of the obstacle.

        Returns:
            AVLNode | None: The node if found, otherwise None.
        """
        if self.tree.get_root() is None:
            print("The tree is empty.")
            return None
        return self._search(self.tree.get_root(), x1, y1)

    def _search(self, current_node: AVLNode, x1, y1):
        """Recursive helper for search."""
        if current_node is None:
            return None
        if x1 == current_node.get_x1() and y1 == current_node.get_y1():
            return current_node
        if x1 < current_node.get_x1() or (x1 == current_node.get_x1() and y1 < current_node.get_y1()):
            return self._search(current_node.get_left(), x1, y1)
        return self._search(current_node.get_right(), x1, y1)

    def insert(self, data: dict):
        """
        Insert a new obstacle into the AVL tree.

        Args:
            data (dict): Obstacle data, e.g., {"type": "...", "sprite": "...", "x1": .., "y1": .., ...}
        """
        obstacle_obj = Obstacle(data)
        node = self.search(obstacle_obj.rect.left, obstacle_obj.rect.top)
        if node is not None:
            print(f"⚠️ Obstacle at ({obstacle_obj.rect.left}, {obstacle_obj.rect.top}) already exists.")
            return
        new_node = AVLNode(obstacle_obj)
        if self.tree.get_root() is None:
            self.tree.set_root(new_node)
        else:
            root = self.tree.get_root()
            root = self._insert(root, new_node, parent=None)
            self.tree.set_root(root)

    def _insert(self, root: AVLNode, new_node: AVLNode, parent: AVLNode):
        """Recursive helper for insertion, with rebalancing."""
        if root is None:
            new_node.set_parent(parent)
            return new_node
        if new_node.get_x1() < root.get_x1() or (
                new_node.get_x1() == root.get_x1() and new_node.get_y1() < root.get_y1()):
            root.set_left(self._insert(root.get_left(), new_node, root))
        else:
            root.set_right(self._insert(root.get_right(), new_node, root))
        self._update_height(root)
        return self._rebalance(root)

    def delete(self, x1, y1):
        """Delete a node by coordinates (x1, y1)."""
        node = self.search(x1, y1)
        if node is None:
            print(f"⚠️ Node at ({x1}, {y1}) not found.")
            return
        self._delete(node)

    def _delete(self, node: AVLNode):
        """Helper for deletion handling all cases (0, 1, 2 children)."""
        if node.get_left() is None and node.get_right() is None:
            self._replace_node(node, None)
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
        else:
            child = node.get_left() if node.get_left() else node.get_right()
            self._replace_node(node, child)
        self._rebalance_upwards(node.get_parent())

    def _rebalance(self, node):
        """Check balance factor and apply rotations if needed."""
        balance = self._balance_factor(node)
        if balance > 1 and self._balance_factor(node.get_left()) >= 0:
            return self._rotate_right(node)
        if balance < -1 and self._balance_factor(node.get_right()) <= 0:
            return self._rotate_left(node)
        if balance > 1 and self._balance_factor(node.get_left()) < 0:
            node.set_left(self._rotate_left(node.get_left()))
            return self._rotate_right(node)
        if balance < -1 and self._balance_factor(node.get_right()) > 0:
            node.set_right(self._rotate_right(node.get_right()))
            return self._rotate_left(node)
        return node

    def _get_predecessor(self, node):
        """Return the inorder predecessor (max of left subtree)."""
        current = node.get_left()
        while current.get_right():
            current = current.get_right()
        return current

    def _replace_node(self, old_node, new_node):
        """Replace old_node with new_node, updating parent references."""
        parent = old_node.get_parent()
        if parent is None:
            self.tree.set_root(new_node)
        elif old_node == parent.get_left():
            parent.set_left(new_node)
        else:
            parent.set_right(new_node)
        if new_node:
            new_node.set_parent(parent)

    def _rebalance_upwards(self, node):
        """Traverse ancestors upwards and rebalance each."""
        while node:
            self._update_height(node)
            node = self._rebalance(node)
            node = node.get_parent()

    def _rotate_right(self, node):
        """Perform a right rotation."""
        y = node.get_left()
        T3 = y.get_right()
        y.set_right(node)
        node.set_left(T3)
        y.set_parent(node.get_parent())
        node.set_parent(y)
        if T3:
            T3.set_parent(node)
        if y.get_parent():
            if y.get_parent().get_left() == node:
                y.get_parent().set_left(y)
            else:
                y.get_parent().set_right(y)
        else:
            self.tree.set_root(y)
        self._update_height(node)
        self._update_height(y)
        return y

    def _rotate_left(self, node):
        """Perform a left rotation."""
        y = node.get_right()
        T2 = y.get_left()
        y.set_left(node)
        node.set_right(T2)
        y.set_parent(node.get_parent())
        node.set_parent(y)
        if T2:
            T2.set_parent(node)
        if y.get_parent():
            if y.get_parent().get_left() == node:
                y.get_parent().set_left(y)
            else:
                y.get_parent().set_right(y)
        else:
            self.tree.set_root(y)
        self._update_height(node)
        self._update_height(y)
        return y

    def postorder(self):
        """Return a list of nodes in postorder traversal."""
        return self._postorder(self.tree.get_root())

    def _postorder(self, node):
        if node is None:
            return []
        return self._postorder(node.get_left()) + self._postorder(node.get_right()) + [
            f"({node.get_x1()}, {node.get_y1()})"]

    def inorder(self):
        """Return a list of nodes in inorder traversal."""
        return self._inorder(self.tree.get_root())

    def _inorder(self, node):
        if node is None:
            return []
        return self._inorder(node.get_left()) + [f"({node.get_x1()}, {node.get_y1()})"] + self._inorder(
            node.get_right())

    def preorder(self):
        """Return a list of nodes in preorder traversal."""
        return self._preorder_recursive(self.tree.get_root())

    def _preorder_recursive(self, node):
        if node is None:
            return []
        return [f"({node.get_x1()}, {node.get_y1()})"] + self._preorder_recursive(
            node.get_left()) + self._preorder_recursive(node.get_right())

    def range_query(self, x1, x2, y1, y2):
        """Return a list of nodes whose (x1, y1) are inside the given rectangle."""
        result = []
        self._range_query(self.tree.get_root(), x1, x2, y1, y2, result)
        return result

    def _range_query(self, node, x1, x2, y1, y2, result):
        if not node:
            return
        if node.get_x1() > x1:
            self._range_query(node.get_left(), x1, x2, y1, y2, result)
        if x1 <= node.get_x1() <= x2 and y1 <= node.get_y1() <= y2:
            result.append({
                "x1": node.get_x1(),
                "y1": node.get_y1(),
                "x2": node.get_x2(),
                "y2": node.get_y2(),
                "tipo": node.get_obstacle()
            })
        if node.get_x1() < x2:
            self._range_query(node.get_right(), x1, x2, y1, y2, result)

    def print_range_query(self, x1, x2, y1, y2):
        """Print obstacles within the given range."""
        resultados = self.range_query(x1, x2, y1, y2)
        print(f"\n🔎 Obstacles in x=[{x1},{x2}], y=[{y1},{y2}]:")
        if not resultados:
            print(" (None found)")
            return
        for obs in resultados:
            print(f" - Object: {obs['tipo']} | Coords: ({obs['x1']}, {obs['y1']}) - ({obs['x2']}, {obs['y2']})")

    def load_from_list(self, obstacles_list):
        """Load multiple obstacles from a list of dictionaries."""
        for obs in obstacles_list:
            try:
                self.insert(obs)
            except Exception as e:
                print(f"Error inserting obstacle: {e}")