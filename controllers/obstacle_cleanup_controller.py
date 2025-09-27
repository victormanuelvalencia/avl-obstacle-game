class ObstacleCleanupController:
    """
    Controller to remove obstacles that have left the visible screen
    and update the AVL tree accordingly.
    """

    def __init__(self, avl_controller):
        """
        Initialize the cleanup controller.

        Args:
            avl_controller: The AVLTreeController instance managing obstacles.
        """
        self.avl_controller = avl_controller

    def cleanup_obstacles(self, obstacles_list, screen_width):
        """
        Remove obstacles that have moved off-screen and delete them from the AVL tree.

        Args:
            obstacles_list: List of active Obstacle instances.
            screen_width: Width of the game screen (unused here but can help future checks).

        Returns:
            List of removed obstacles.
        """
        removed = []

        for obs in obstacles_list[:]:
            if obs.rect.right < 0:  # Off-screen
                # Delete from AVL using initial coordinates
                self.avl_controller.delete(obs.init_x1, obs.init_y1)

                removed.append(obs)
                obstacles_list.remove(obs)

        return removed