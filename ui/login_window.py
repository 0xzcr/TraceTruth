from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from auth.service import authenticate


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TraceTruth Login")
        self.user = None
        self.setMinimumWidth(420)

        title = QLabel("TraceTruth")
        title_font = QFont("Arial", 18, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #000000;")
        title.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        card = QFrame()
        card.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; }"
        )
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #ef4444;")

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        login_button.setStyleSheet(
            "QPushButton { background: #111827; color: white; padding: 10px; border-radius: 8px; }"
            "QPushButton:hover { background: #1f2937; }"
        )

        self.username_input.setStyleSheet(
            "QLineEdit { padding: 10px; border: 1px solid #d1d5db; border-radius: 8px; }"
        )
        self.password_input.setStyleSheet(
            "QLineEdit { padding: 10px; border: 1px solid #d1d5db; border-radius: 8px; }"
        )

        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(login_button)
        card_layout.addWidget(self.status_label)
        card.setLayout(card_layout)

        layout.addWidget(title)
        layout.addWidget(card)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        user = authenticate(username, password)
        if user:
            self.user = user
            self.accept()
        else:
            self.status_label.setText("Invalid credentials")
