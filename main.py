from models.avl_tree import AVLTree
from controllers.avl_tree_controller import AVLTreeController
from views.tree_view import TreeView

if __name__ == "__main__":
    tree = AVLTree()
    controller = AVLTreeController(tree)

    # Insertar obstáculos
    controller.insert(20, 2, 12, 4, "roca")
    controller.insert(15, 1, 6, 3, "hueco")
    controller.insert(10, 3, 18, 6, "barrera")
    controller.insert(25, 0, 3, 2, "árbol")
    controller.insert(30, 0, 3, 2, "árbol")
    controller.insert(35, 0, 3, 2, "árbol")
    controller.insert(23, 0, 3, 2, "árbol")
    controller.insert(20, 0, 3, 2, "árbol")
    controller.insert(28, 0, 3, 2, "árbol")

    print("Recorrido inorder (por x luego y):")
    print(controller.inorder())

    print("Recorrido preorder (por x luego y):")
    print(controller.preorder())

    print("Recorrido postorder (por x luego y):")
    print(controller.postorder())

    # Definir rango
    x_min, x_max, y_min, y_max = 15, 30, 0, 3

    # Imprimir directamente con la nueva función
    controller.print_range_query(x_min, x_max, y_min, y_max)

    # Graficar árbol
    plotter = TreeView(controller)
    plotter.plot()
