from PySide6.QtWidgets import QTextEdit
from database.database import log_event


class TraceEditor(QTextEdit):

    def __init__(self):
        super().__init__()

    # Detect typing
    def keyPressEvent(self, event):
        key = event.text()

        if key:  # only log real characters
            log_event("KEYPRESS", key)

        super().keyPressEvent(event)

    # Detect paste events
    def insertFromMimeData(self, source):
        text = source.text()

        if text:
            log_event("PASTE", text)

        super().insertFromMimeData(source)