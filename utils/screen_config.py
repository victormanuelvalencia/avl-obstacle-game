import pygame

def get_screen_config(scale: float = 0.8, game_ratio: float = 0.65) -> dict:
    """
    Calculate and return screen dimensions for the game window.

    Args:
        scale (float, optional): Percentage of the screen to use
            (e.g., 0.8 → 80%). Defaults to 0.8.
        game_ratio (float, optional): Proportion of the total width
            allocated to the game area (the rest is used for the tree view).
            Defaults to 0.65.

    Returns:
        dict: Dictionary with the following keys:
            - "width" (int): Total window width.
            - "height" (int): Total window height.
            - "game_width" (int): Width allocated to the game area.
            - "tree_width" (int): Width allocated to the tree view.
    """
    info = pygame.display.Info()

    width = int(info.current_w * scale)
    height = int(info.current_h * scale)

    game_width = int(width * game_ratio)
    tree_width = width - game_width

    return {
        "width": width,
        "height": height,
        "game_width": game_width,
        "tree_width": tree_width
    }