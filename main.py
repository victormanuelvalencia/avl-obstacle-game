import pygame
from controllers.avl_tree_controller import AVLTreeController
from models.avl_tree import AVLTree
from utils.file_admin import read_json
from views.menu_view import MenuView
from views.game_coordinator import GameCoordinator

if __name__ == "__main__":
    pygame.init()

    # 1. Mostrar menú de inicio
    menu = MenuView()
    start_game = menu.run()  # Espera hasta que el jugador elija "JUGAR" o cierre

    if start_game:
        # 2. Crear árbol y controlador
        tree = AVLTree()
        controller = AVLTreeController(tree)

        # 3. Leer configuración desde JSON
        data = read_json("config/settings.json")
        config = data["config"]

        # 4. Leer obstáculos desde JSON y cargarlos en el árbol
        obs_data = read_json("config/obstacles.json")
        try:
            controller.load_from_list(obs_data["obstacles"])
            print("Obstáculos cargados correctamente.")
        except Exception as e:
            print(f"[ERROR] No se pudieron cargar los obstáculos: {e}")

        # 5. Crear coordinador del juego y ejecutar
        coordinator = GameCoordinator(config, controller)
        coordinator.run()

    pygame.quit()
