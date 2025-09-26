import pygame
<<<<<<< HEAD
from controllers.avl_tree_controller import AVLTreeController
from models.avl_tree import AVLTree
from utils.file_admin import read_json
from views.menu_view import MenuView
from views.game_coordinator import GameCoordinator
=======

from utils.file_admin import read_json
from models.obstacle import Obstacle
from models.avl_tree import AVLTree
from controllers.avl_tree_controller import AVLTreeController
from views.integrated_game_view import IntegratedGameView
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed

if __name__ == "__main__":
    pygame.init()
<<<<<<< HEAD

    # 1. Mostrar menú de inicio
    menu = MenuView()
    start_game = menu.run()  # Espera hasta que el jugador elija "JUGAR" o cierre
=======
    screen = pygame.display.set_mode((800, 600))  # pantalla temporal para crear obstáculos

    # 1. Crear árbol AVL y su controlador
    tree = AVLTree()
    controller = AVLTreeController(tree)
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed

    if start_game:
        # 2. Crear árbol y controlador
        tree = AVLTree()
        controller = AVLTreeController(tree)

<<<<<<< HEAD
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
=======
    # 3. Leer archivo de obstáculos
    obs_data = read_json("config/obstacles.json")
    obstacles = [Obstacle(obs) for obs in obs_data["obstacles"]]

    # 4. Cargar obstáculos en el árbol AVL
    try:
        controller.load_from_list(obs_data["obstacles"])
        print("Obstáculos cargados correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudieron cargar los obstáculos: {e}")

    # 5. Mostrar recorridos y consultas
    print("Recorrido inorder (por x luego y):")
    print(controller.inorder())
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed

        # 5. Crear coordinador del juego y ejecutar
        coordinator = GameCoordinator(config, controller)
        coordinator.run()

<<<<<<< HEAD
    pygame.quit()
=======
    print("Recorrido postorder (por x luego y):")
    print(controller.postorder())

    node = controller.search(400, 250)
    if node:
        print("x =", node.get_x1(), "y =", node.get_y1(), "height =", node.get_height())
    else:
        print("No node found")

    x_min, x_max, y_min, y_max = 0, 400, 100, 350
    controller.print_range_query(x_min, x_max, y_min, y_max)

    # 6. Crear la vista integrada del juego y ejecutar
    integrated_view = IntegratedGameView(config, controller, obstacles)
    integrated_view.run()

    pygame.quit()
>>>>>>> 5b717d8b1e51c55e07f33b1429e7fbddfd9a9aed
