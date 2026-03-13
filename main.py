import sys
from PySide6.QtWidgets import QApplication
from db.schema import create_schema
from auth.service import ensure_default_users
from ui.login_window import LoginWindow
from ui.student_window import StudentWindow
from ui.reviewer_window import ReviewerWindow


def main():
    create_schema()
    ensure_default_users()

    app = QApplication(sys.argv)
    app.setStyleSheet(
        "QMainWindow { background: #f8fafc; }"
        "QDialog { background: #f8fafc; }"
        "QTabBar::tab { padding: 8px 12px; }"
        "QTabWidget::pane { border: 1px solid #e5e7eb; border-radius: 10px; }"
    )
    login = LoginWindow()
    if login.exec() == 1 and login.user:
        if login.user["role"] == "student":
            window = StudentWindow(login.user)
        else:
            window = ReviewerWindow()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
