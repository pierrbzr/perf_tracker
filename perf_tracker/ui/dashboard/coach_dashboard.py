"""
ui/dashboard/coach_dashboard.py
Dashboard coach — placeholder en attendant le vrai contenu.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

from assets.theme import (
    COLOR_RED, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_BORDER, FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_BODY
)


class CoachDashboard(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        title = QLabel("🏒  Dashboard Coach")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            color: {COLOR_RED};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
        """)

        welcome = QLabel(f"Bienvenue, {self.user['prenom']} {self.user['nom']}")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_BODY}px;
            font-family: "{FONT_FAMILY}";
        """)

        placeholder = QLabel("[ Dashboard en construction ]")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_BODY}px;
            font-family: "{FONT_FAMILY}";
            border: 1px dashed {COLOR_BORDER};
            border-radius: 8px;
            padding: 40px;
            margin: 20px;
        """)

        logout_btn = QPushButton("Se déconnecter")
        logout_btn.setFixedWidth(200)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self.logout_requested.emit)

        layout.addWidget(title)
        layout.addWidget(welcome)
        layout.addWidget(placeholder)
        layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.Align)