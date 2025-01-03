import signal
from PyQt6.QtCore import QTimer

exit_in_progress = False

class AppSignalUtil:
    """Utility class for handling application signals."""
    def __init__(self, app):
        self.app = app
        self.init_signal_handling()

    def init_signal_handling(self):
        """Initialize signal handling for clean exit."""
        signal.signal(signal.SIGINT, self.handle_exit_signal)
        signal.signal(signal.SIGTERM, self.handle_exit_signal)

        # Custom event loop to handle signals
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: None)
        self.timer.start(100)

    def handle_exit_signal(self, signum, frame):
        """Handle exit signals (SIGINT, SIGTERM)."""
        global exit_in_progress
        if not exit_in_progress:
            exit_in_progress = True
            print("Exit by signal")
            self.app.quit()