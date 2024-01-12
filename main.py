# Import necessary PyQt5 modules
import sys
import traceback

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDesktopWidget

from game_window import GalacticPioneers


# StartScreen class definition
class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.background_image = None
        self.game_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Galactic Pioneers - Start Screen')
        self.setGeometry(300, 300, 800, 600)

        # Load the background image
        self.background_image = QPixmap('start_screen.png')

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        # Add a label
        titleLabel = QLabel('Welcome to Galactic Pioneers!')
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titleLabel)

        startButton = QPushButton('Start Game')
        startButton.clicked.connect(self.start_game)
        layout.addWidget(startButton)

        # Add more buttons for options/settings here if needed

        exitButton = QPushButton('Exit')
        exitButton.clicked.connect(self.close)
        layout.addWidget(exitButton)

        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.show()

    def start_game(self):
        self.close()
        self.game_window = GalacticPioneers()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)


class GameOverScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Game Over')
        self.setGeometry(300, 300, 600, 400)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        gameOverLabel = QLabel('Game Over! Redirecting to main screen...')
        gameOverLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(gameOverLabel)

        # Redirect to the start screen after 10 seconds
        time = 10000
        QTimer.singleShot(time, self.redirect_to_start)

        self.show()

    def redirect_to_start(self):
        self.close()
        global ex
        ex = StartScreen()  # Assuming StartScreen is defined as before

# Modify the main function
def main():
    try:
        app = QApplication(sys.argv)
        ex = StartScreen()  # Start with the start screen
        sys.exit(app.exec_())
    except Exception as e:
        print("An error occurred:", str(e))
        traceback.print_exc()


if __name__ == '__main__':
    print("Starting application")
    main()
    print("Application closed")
