import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TraceTruth Editor")
        self.resize(800, 600)

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()