import pygame

from utils.file_admin import read_json
from models.obstacle import Obstacle
from models.avl_tree import AVLTree
from controllers.avl_tree_controller import AVLTreeController
from views.integrated_game_view import IntegratedGameView

if __name__ == "__main__":
    # 0. Inicializar Pygame para poder cargar imágenes
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # pantalla temporal para crear obstáculos

    # 1. Crear árbol AVL y su controlador
    tree = AVLTree()
    controller = AVLTreeController(tree)

    # 2. Leer configuración desde JSON
    data = read_json("config/settings.json")
    config = data["config"]

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

    print("Recorrido preorder (por x luego y):")
    print(controller.preorder())

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