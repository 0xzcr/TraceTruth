import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from database.database import create_schema
from engine.editor import TraceEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TraceTruth Editor")
        self.resize(800, 600)
        self.editor = TraceEditor()
        self.setCentralWidget(self.editor)


def main():
    create_schema()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
