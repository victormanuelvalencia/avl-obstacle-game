class ButtonController:
    """
    Controller for managing a pause button state.
    """

    def __init__(self):
        """Initialize the button controller with a paused state."""
        self.paused = False

    def handle_pause_button(self, button, event):
        """
        Check if the pause button was pressed and toggle the paused state.

        Args:
            button: The button object to handle.
            event: The pygame event to check.

        Returns:
            True if the paused state was toggled, otherwise False.
        """
        if button.handle_event(event):
            self.paused = not self.paused
            return True
        return False

    def is_paused(self):
        """Return whether the game is currently paused."""
        return self.paused