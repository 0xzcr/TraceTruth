from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PySide6.QtCore import QTimer


class ReplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.events = []
        self.index = 0
        self.current_text = ""

        layout = QVBoxLayout()
        controls = QHBoxLayout()

        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.step_button = QPushButton("Step")
        self.reset_button = QPushButton("Reset")

        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.step_button.clicked.connect(self.step)
        self.reset_button.clicked.connect(self.reset)

        controls.addWidget(self.play_button)
        controls.addWidget(self.pause_button)
        controls.addWidget(self.step_button)
        controls.addWidget(self.reset_button)

        self.viewer = QTextEdit()
        self.viewer.setReadOnly(True)

        layout.addLayout(controls)
        layout.addWidget(self.viewer)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.step)

    def load_events(self, events):
        self.events = events
        self.reset()

    def play(self):
        if self.events:
            self.timer.start()

    def pause(self):
        self.timer.stop()

    def reset(self):
        self.timer.stop()
        self.index = 0
        self.current_text = ""
        self.viewer.setPlainText("")

    def step(self):
        if self.index >= len(self.events):
            self.timer.stop()
            return
        event = self.events[self.index]
        self.current_text = apply_event(self.current_text, event)
        self.viewer.setPlainText(self.current_text)
        self.index += 1


def apply_event(text, event):
    _, event_type, content, cursor_pos, _, _ = event
    if cursor_pos is None:
        cursor_pos = len(text)

    if event_type == "KEYPRESS" and content:
        return text[:cursor_pos] + content + text[cursor_pos:]
    if event_type == "PASTE" and content:
        return text[:cursor_pos] + content + text[cursor_pos:]
    if event_type == "BACKSPACE":
        if cursor_pos > 0:
            return text[:cursor_pos - 1] + text[cursor_pos:]
        return text
    if event_type == "DELETE":
        if cursor_pos < len(text):
            return text[:cursor_pos] + text[cursor_pos + 1 :]
        return text
    return text
