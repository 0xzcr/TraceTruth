from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QFrame,
    QToolBar,
    QFontComboBox,
    QComboBox,
    QColorDialog,
)
from PySide6.QtGui import QFont, QIcon, QTextCharFormat, QTextCursor, QTextListFormat, QAction, QColor
from PySide6.QtCore import Qt
from editor.session_manager import SessionManager
from editor.event_logger import EventLogger
from editor.trace_editor import TraceEditor
from db.documents_repo import update_document_text


class StudentWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("TraceTruth - Student")
        self.user = user
        self.resize(900, 600)

        self.session_manager = SessionManager(user_id=user["id"], device="local", app_version="0.1")
        session_id, doc_id = self.session_manager.start()
        self.event_logger = EventLogger(session_id)
        self.doc_id = doc_id

        central = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("Editor")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        subtitle = QLabel(f"Logged in as: {self.user['username']}")
        subtitle.setStyleSheet("color: #6b7280;")
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(subtitle)

        editor_card = QFrame()
        editor_card.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; }"
        )
        editor_layout = QVBoxLayout()
        editor_layout.setContentsMargins(12, 12, 12, 12)
        editor_layout.setSpacing(8)

        self.editor = TraceEditor(self.event_logger)
        self.editor.setStyleSheet(
            "QTextEdit { border: 1px solid #d1d5db; border-radius: 8px; padding: 8px; color: #111827; background: #ffffff; }"
        )
        self.editor.setAlignment(Qt.AlignLeft)
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(
            "QPushButton { background: #111827; color: white; padding: 8px 12px; border-radius: 8px; }"
            "QPushButton:hover { background: #1f2937; }"
        )
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #10b981;")

        self.save_button.clicked.connect(self.save_document)

        self.toolbar = self._build_toolbar()
        self.addToolBar(self.toolbar)

        footer = QHBoxLayout()
        footer.addWidget(self.save_button)
        footer.addWidget(self.status_label)
        footer.addStretch(1)

        editor_layout.addWidget(self.editor)
        editor_layout.addLayout(footer)
        editor_card.setLayout(editor_layout)

        layout.addLayout(header)
        layout.addWidget(editor_card)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def save_document(self):
        text = self.editor.toPlainText()
        update_document_text(self.doc_id, text)
        self.event_logger.log("SAVE")
        self.status_label.setText("Saved")

    def closeEvent(self, event):
        self.save_document()
        self.session_manager.end()
        event.accept()

    def _build_toolbar(self):
        toolbar = QToolBar("Formatting")
        toolbar.setMovable(False)
        toolbar.setStyleSheet(
            "QToolBar { background: #ffffff; border: 1px solid #e5e7eb; }"
            "QToolButton { padding: 6px; }"
        )

        bold_action = QAction("B", self)
        bold_action.setCheckable(True)
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction("I", self)
        italic_action.setCheckable(True)
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        underline_action = QAction("U", self)
        underline_action.setCheckable(True)
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

        toolbar.addSeparator()

        align_left = QAction("Left", self)
        align_left.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        toolbar.addAction(align_left)

        align_center = QAction("Center", self)
        align_center.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignHCenter))
        toolbar.addAction(align_center)

        align_right = QAction("Right", self)
        align_right.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        toolbar.addAction(align_right)

        align_justify = QAction("Justify", self)
        align_justify.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        toolbar.addAction(align_justify)

        toolbar.addSeparator()

        font_box = QFontComboBox()
        font_box.currentFontChanged.connect(self.set_font_family)
        toolbar.addWidget(font_box)

        size_box = QComboBox()
        for size in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36]:
            size_box.addItem(str(size))
        size_box.setCurrentText("12")
        size_box.currentTextChanged.connect(self.set_font_size)
        toolbar.addWidget(size_box)

        toolbar.addSeparator()

        bullet_action = QAction("Bullets", self)
        bullet_action.triggered.connect(self.insert_bullets)
        toolbar.addAction(bullet_action)

        number_action = QAction("Numbered", self)
        number_action.triggered.connect(self.insert_numbered)
        toolbar.addAction(number_action)

        toolbar.addSeparator()

        text_color_action = QAction("Text Color", self)
        text_color_action.triggered.connect(self.pick_text_color)
        toolbar.addAction(text_color_action)

        highlight_action = QAction("Highlight", self)
        highlight_action.triggered.connect(self.pick_highlight_color)
        toolbar.addAction(highlight_action)

        toolbar.addSeparator()

        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.editor.undo)
        toolbar.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.editor.redo)
        toolbar.addAction(redo_action)

        toolbar.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self.editor.cut)
        toolbar.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.editor.copy)
        toolbar.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.editor.paste)
        toolbar.addAction(paste_action)

        select_all_action = QAction("Select All", self)
        select_all_action.triggered.connect(self.editor.selectAll)
        toolbar.addAction(select_all_action)

        toolbar.addSeparator()

        strike_action = QAction("Strike", self)
        strike_action.setCheckable(True)
        strike_action.triggered.connect(self.toggle_strike)
        toolbar.addAction(strike_action)

        clear_action = QAction("Clear Format", self)
        clear_action.triggered.connect(self.clear_formatting)
        toolbar.addAction(clear_action)

        toolbar.addSeparator()

        indent_action = QAction("Indent", self)
        indent_action.triggered.connect(self.indent)
        toolbar.addAction(indent_action)

        outdent_action = QAction("Outdent", self)
        outdent_action.triggered.connect(self.outdent)
        toolbar.addAction(outdent_action)

        line_spacing_1 = QAction("Line 1.0", self)
        line_spacing_1.triggered.connect(lambda: self.set_line_spacing(100))
        toolbar.addAction(line_spacing_1)

        line_spacing_15 = QAction("Line 1.5", self)
        line_spacing_15.triggered.connect(lambda: self.set_line_spacing(150))
        toolbar.addAction(line_spacing_15)

        line_spacing_2 = QAction("Line 2.0", self)
        line_spacing_2.triggered.connect(lambda: self.set_line_spacing(200))
        toolbar.addAction(line_spacing_2)

        return toolbar

    def toggle_bold(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if checked else QFont.Normal)
        self.merge_format(fmt)

    def toggle_italic(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.merge_format(fmt)

    def toggle_underline(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.merge_format(fmt)

    def set_font_family(self, font):
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self.merge_format(fmt)

    def set_font_size(self, size_text):
        try:
            size = int(size_text)
        except ValueError:
            return
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self.merge_format(fmt)

    def insert_bullets(self):
        cursor = self.editor.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDisc)
        cursor.insertList(fmt)

    def insert_numbered(self):
        cursor = self.editor.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDecimal)
        cursor.insertList(fmt)

    def pick_text_color(self):
        color = QColorDialog.getColor(parent=self)
        if not color.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self.merge_format(fmt)

    def pick_highlight_color(self):
        color = QColorDialog.getColor(parent=self)
        if not color.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        self.merge_format(fmt)

    def toggle_strike(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(checked)
        self.merge_format(fmt)

    def clear_formatting(self):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Normal)
        fmt.setFontItalic(False)
        fmt.setFontUnderline(False)
        fmt.setFontStrikeOut(False)
        fmt.setForeground(QColor("#111827"))
        fmt.setBackground(QColor("transparent"))
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)

    def indent(self):
        cursor = self.editor.textCursor()
        block_format = cursor.blockFormat()
        block_format.setLeftMargin(block_format.leftMargin() + 20)
        cursor.setBlockFormat(block_format)

    def outdent(self):
        cursor = self.editor.textCursor()
        block_format = cursor.blockFormat()
        block_format.setLeftMargin(max(0, block_format.leftMargin() - 20))
        cursor.setBlockFormat(block_format)

    def set_line_spacing(self, percent):
        cursor = self.editor.textCursor()
        block_format = cursor.blockFormat()
        block_format.setLineHeight(percent, block_format.ProportionalHeight)
        cursor.setBlockFormat(block_format)

    def merge_format(self, fmt):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)
