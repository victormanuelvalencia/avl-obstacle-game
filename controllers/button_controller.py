class ButtonController:
    def __init__(self):
        self.paused = False

    def handle_pause_button(self, button, event):
        """
        Verifica si el botón de pausa fue presionado y alterna el estado de pausa.
        Retorna True si se alternó.
        """
        if button.handle_event(event):
            self.paused = not self.paused
            return True
        return False

    def is_paused(self):
        return self.paused
