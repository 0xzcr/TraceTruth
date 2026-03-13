from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit


class TraceEditor(QTextEdit):
    def __init__(self, event_logger):
        super().__init__()
        self.event_logger = event_logger

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        cursor_pos = cursor.position()
        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()

        key = event.key()
        text = event.text()

        if key == Qt.Key_Backspace:
            self.event_logger.log("BACKSPACE", cursor_pos=cursor_pos, selection_start=selection_start, selection_end=selection_end)
        elif key == Qt.Key_Delete:
            self.event_logger.log("DELETE", cursor_pos=cursor_pos, selection_start=selection_start, selection_end=selection_end)
        elif text:
            self.event_logger.log("KEYPRESS", content=text, cursor_pos=cursor_pos, selection_start=selection_start, selection_end=selection_end)

        super().keyPressEvent(event)

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        cursor_pos = cursor.position()
        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        text = source.text()

        if text:
            self.event_logger.log("PASTE", content=text, cursor_pos=cursor_pos, selection_start=selection_start, selection_end=selection_end)

        super().insertFromMimeData(source)
