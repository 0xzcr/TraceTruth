from PySide6.QtWidgets import QTextEdit
from database.database import log_event


class TraceEditor(QTextEdit):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        key = event.text()
        if key:
            log_event("KEYPRESS", key)
        super().keyPressEvent(event)

    def insertFromMimeData(self, source):
        text = source.text()
        if text:
            log_event("PASTE", text)
        super().insertFromMimeData(source)
