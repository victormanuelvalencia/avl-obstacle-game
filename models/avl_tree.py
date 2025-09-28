from models.obstacle import Obstacle

class AVLNode:
    """
    Node of an AVL tree that contains an obstacle.
    Nodes are ordered by (x1, y1) coordinates.

    Attributes:
        _obstacle (Obstacle): The obstacle stored in this node.
        parent (AVLNode | None): Reference to the parent node.
        _height (int): Height of this node in the AVL tree.
        _left (AVLNode | None): Left child node.
        _right (AVLNode | None): Right child node.

    Note:
        This class provides standard getters and setters for:
        - Coordinates (x1, y1, x2, y2)
        - Obstacle object
        - Height
        - Parent, left, and right children
    """

    def __init__(self, obstacle: Obstacle, parent=None):
        """
        Initialize a new AVL tree node.

        Args:
            obstacle (Obstacle): The obstacle stored in this node.
            parent (AVLNode, optional): Reference to the parent node. Defaults to None.
        """
        self._obstacle = obstacle
        self.parent = parent
        self._height = 1
        self._left = None
        self._right = None

    # --- General Getters ---
    def get_x1(self): return self._obstacle.rect.left
    def get_y1(self): return self._obstacle.rect.top
    def get_x2(self): return self._obstacle.rect.right
    def get_y2(self): return self._obstacle.rect.bottom
    def get_obstacle(self): return self._obstacle
    def get_height(self): return self._height
    def get_left(self): return self._left
    def get_right(self): return self._right
    def get_parent(self): return self.parent

    # --- General Setters ---
    def set_height(self, value): self._height = value
    def set_left(self, node): self._left = node
    def set_right(self, node): self._right = node
    def set_parent(self, node): self.parent = node

    def to_dict(self):
        """
        Convert the node data into a dictionary.

        Returns:
            dict: Dictionary representation of the obstacle (coordinates and type).
        """
        return self._obstacle.to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a node from a dictionary (e.g., JSON data).

        Args:
            data (dict): Dictionary containing obstacle data.

        Returns:
            AVLNode: New node containing the obstacle.
        """
        obstacle = Obstacle(data)
        return cls(obstacle)


class AVLTree:
    """
    AVL tree structure for storing obstacles.

    Attributes:
        _root (AVLNode | None): Root node of the tree.
    """

    def __init__(self):
        """Initialize an empty AVL tree."""
        self._root = None

    def get_root(self): return self._root
    def set_root(self, node): self._root = node