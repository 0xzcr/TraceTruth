from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTabWidget, QTextEdit, QListWidgetItem, QLabel, QFrame
from PySide6.QtGui import QFont
from reviewer.paste_detector import detect_pastes
from reviewer.timeline import analyze_timeline
from reviewer.replay import ReplayWidget
from reviewer.mindmap import MindMapWidget
from db.sessions_repo import list_all_sessions_with_users
from db.documents_repo import get_document_by_session
from db.events_repo import list_events
from utils.time_utils import format_ts


class ReviewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TraceTruth - Reviewer")
        self.resize(1100, 700)

        central = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        sidebar = QFrame()
        sidebar.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; }"
        )
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(12, 12, 12, 12)
        sidebar_layout.setSpacing(8)

        sidebar_title = QLabel("Files")
        sidebar_title.setFont(QFont("Arial", 14, QFont.Bold))

        self.session_list = QListWidget()
        self.session_list.itemSelectionChanged.connect(self.load_selected_session)
        self.session_list.setStyleSheet(
            "QListWidget { border: 1px solid #d1d5db; border-radius: 8px; color: #111827; background: #ffffff; }"
        )

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            "QTabBar::tab { color: #111827; padding: 8px 12px; }"
        )
        self.doc_viewer = QTextEdit()
        self.doc_viewer.setReadOnly(True)
        self.doc_viewer.setStyleSheet(
            "QTextEdit { border: 1px solid #d1d5db; border-radius: 8px; padding: 8px; color: #111827; background: #ffffff; }"
        )

        self.paste_list = QListWidget()
        self.paste_list.setStyleSheet(
            "QListWidget { border: 1px solid #d1d5db; border-radius: 8px; color: #111827; background: #ffffff; }"
        )
        self.timeline_list = QListWidget()
        self.timeline_list.setStyleSheet(
            "QListWidget { border: 1px solid #d1d5db; border-radius: 8px; color: #111827; background: #ffffff; }"
        )
        self.replay_widget = ReplayWidget()
        self.mindmap_widget = MindMapWidget()

        self.tabs.addTab(self.doc_viewer, "Document")
        self.tabs.addTab(self.paste_list, "Paste Detection")
        self.tabs.addTab(self.timeline_list, "Timeline")
        self.tabs.addTab(self.replay_widget, "Replay")
        self.tabs.addTab(self.mindmap_widget, "Mind Map")

        sidebar_layout.addWidget(sidebar_title)
        sidebar_layout.addWidget(self.session_list)
        sidebar.setLayout(sidebar_layout)

        layout.addWidget(sidebar, 1)
        layout.addWidget(self.tabs, 3)
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.load_sessions()

    def load_sessions(self):
        self.session_list.clear()
        sessions = list_all_sessions_with_users()
        for session_id, start_time, end_time, username in sessions:
            label = f"{username} | {format_ts(start_time)} | {session_id}"
            item = QListWidgetItem(label)
            item.setData(1, session_id)
            self.session_list.addItem(item)

    def load_selected_session(self):
        items = self.session_list.selectedItems()
        if not items:
            return
        session_id = items[0].data(1)
        self.load_session(session_id)

    def load_session(self, session_id):
        doc = get_document_by_session(session_id)
        events = list_events(session_id)

        self.doc_viewer.setPlainText(doc["final_text"] if doc and doc["final_text"] else "")

        self.paste_list.clear()
        for p in detect_pastes(events):
            self.paste_list.addItem(f"{p['time_str']} | len={p['length']} | {p['content'][:40]}...")
        if self.paste_list.count() == 0:
            self.paste_list.addItem("No paste events detected")

        self.timeline_list.clear()
        for line in analyze_timeline(events):
            self.timeline_list.addItem(line)

        self.replay_widget.load_events(events)
        self.mindmap_widget.update_from_text(self.doc_viewer.toPlainText())
