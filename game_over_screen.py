from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt


class GameOverScreen(QMainWindow):
    def __init__(self, on_game_over_callback):
        super().__init__()
        self.on_game_over_callback = on_game_over_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Game Over')
        self.setGeometry(300, 300, 600, 400)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        gameOverLabel = QLabel('Game Over!')
        gameOverLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(gameOverLabel)

        # Redirect to the start screen after 10 seconds
        QTimer.singleShot(10000, self.on_game_over_callback)
        self.show()
