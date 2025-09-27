import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_size=24, bg_color=(50, 50, 50), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen):
        # Cambiar color si el mouse está encima
        color = (self.bg_color[0]+30, self.bg_color[1]+30, self.bg_color[2]+30) if self.hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)  # borde

        # Texto centrado
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True  # botón presionado
        return False
