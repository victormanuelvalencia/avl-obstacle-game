import pygame
from controllers.avl_tree_controller import AVLTreeController
from models.avl_tree import AVLTree
from utils.file_admin import read_json
from views.menu_view import MenuView
from views.game_coordinator import GameCoordinator

if __name__ == "__main__":
    pygame.init()

    # 1. Display the main menu
    menu = MenuView()
    start_game = menu.run()  # Wait until the player selects "PLAY" or closes the window

    if start_game:
        # 2. Create the AVL tree and its controller
        tree = AVLTree()
        controller = AVLTreeController(tree)

        # 3. Load game configuration from JSON
        data = read_json("config/settings.json")
        config = data["config"]

        # 4. Load obstacles from JSON and insert them into the tree
        obs_data = read_json("config/obstacles.json")
        try:
            controller.load_from_list(obs_data["obstacles"])
            print("Obstacles loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Could not load obstacles: {e}")

        # 5. Create the game coordinator and run the game
        coordinator = GameCoordinator(config, controller)
        coordinator.run()

    pygame.quit()