import pygame

def get_screen_config(scale=0.8, game_ratio=0.65):
    """
    Calcula y retorna las dimensiones de la ventana.
    - scale: porcentaje de la pantalla usado (ej. 0.8 → 80%)
    - game_ratio: proporción del área de juego frente al árbol
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
