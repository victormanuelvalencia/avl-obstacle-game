from models.avl_tree import AVLTree
from controllers.avl_tree_controller import AVLTreeController
from utils.file_admin import read_json
from views.game import GameView
from views.tree_view import TreeView

if __name__ == "__main__":
    tree = AVLTree()
    controller = AVLTreeController(tree)

    # Leer configuración desde JSON
    data = read_json("config/settings.json")
    config = data["config"]

    # Iniciar la vista del juego
    game = GameView(config)
    game.run()

    # 1. Leer archivo JSON
    data = read_json("config/settings.json")

    # 2. Cargar obstáculos en el árbol
    controller.load_from_list(data["obstacles"])


    print("Recorrido inorder (por x luego y):")
    print(controller.inorder())

    print("Recorrido preorder (por x luego y):")
    print(controller.preorder())

    print("Recorrido postorder (por x luego y):")
    print(controller.postorder())

    node = controller.search(35, 0)
    if node:
        print("Node found")
        print("x = ", node.get_x_min(), "y = " , node.get_y_min(), "at heigh ", node.get_height())
    else:
        print("No node found")

    # Definir rango
    x_min, x_max, y_min, y_max = 15, 30, 0, 3

    # Imprimir directamente con la nueva función
    controller.print_range_query(x_min, x_max, y_min, y_max)

    # Graficar árbol
    plotter = TreeView(controller)
    plotter.plot()


