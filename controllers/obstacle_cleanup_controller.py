class ObstacleCleanupController:
    def __init__(self, avl_controller):
        self.avl_controller = avl_controller

    def cleanup_obstacles(self, obstacles_list, screen_width):
        """Elimina obstáculos que ya salieron de la pantalla."""
        removed = []

        for obs in obstacles_list[:]:
            if obs.rect.right < 0:  # ya salió de la pantalla
                # Eliminar del AVL usando coordenadas iniciales
                self.avl_controller.delete(obs.init_x1, obs.init_y1)

                removed.append(obs)
                obstacles_list.remove(obs)

        return removed
