"""
ui/graphs.py
Liste des joueurs pour sélectionner qui remplit son grip.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal

from assets.theme import (
    COLOR_GREEN, COLOR_GREEN_DARK, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_BG_CARD, COLOR_BG_HOVER, COLOR_BORDER,
    COLOR_GOOD, COLOR_WARNING, COLOR_DANGER, COLOR_NEUTRAL,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS
)
from models.player import get_all_players
from models.wellness import get_team_wellness_today, get_team_wellness_range


class WellnessTeamGraph(QWidget):
    """
    Liste des joueurs avec indication si grip déjà saisi aujourd'hui.
    Émet grip_selected(player_dict) au clic sur un joueur.
    """
    back_requested  = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # ── Header ──
        header = QHBoxLayout()

        back_btn = QPushButton("Retour")
        back_btn.setFixedWidth(100)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_GREEN};
                border: 2px solid {COLOR_GREEN};
                border-radius: {BORDER_RADIUS}px;
                padding: 6px 12px;
                font-size: {FONT_SIZE_SMALL}px;
                font-weight: 600;
                font-family: "{FONT_FAMILY}";
            }}
            QPushButton:hover {{
                background-color: {COLOR_GREEN};
                color: white;
            }}
            QPushButton:pressed {{ background-color: {COLOR_GREEN_DARK}; }}

        """)
        back_btn.clicked.connect(self.back_requested.emit)

        title = QLabel("Graphique — Évolution du Wellness ")
        title.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
        """)

        self.refresh_btn = QPushButton("↺ Actualiser")
        self.refresh_btn.setFixedWidth(120)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_TEXT_SECONDARY};
                border: 1px solid {COLOR_BORDER};
                border-radius: {BORDER_RADIUS}px;
                padding: 6px 12px;
                font-size: {FONT_SIZE_SMALL}px;
                font-family: "{FONT_FAMILY}";
            }}
            QPushButton:hover {{
                border-color: {COLOR_GREEN};
                color: {COLOR_GREEN};
            }}
            QPushButton:pressed {{ color: {COLOR_GREEN_DARK}; }}
        """)
        self.refresh_btn.clicked.connect(self._refresh)

        header.addWidget(back_btn)
        header.addSpacing(16)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        main_layout.addLayout(header)
        
        # ── Légende ──
        legend = QHBoxLayout()
        legend.setSpacing(16)
        for texte , attribut in [
            ("7 jours", "week"),
            ("30 jours", "month"),
        ]:
            btn = QPushButton(texte)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLOR_TEXT_SECONDARY};
                    border: 1px solid {COLOR_BORDER};
                    border-radius: {BORDER_RADIUS}px;
                    padding: 6px 12px;
                    font-size: {FONT_SIZE_SMALL}px;
                    font-family: "{FONT_FAMILY}";
                }}
                QPushButton:hover {{
                    border-color: {COLOR_GREEN};
                    color: {COLOR_GREEN};
                }}
                QPushButton:pressed {{ color: {COLOR_GREEN_DARK}; }}
            """)
            legend.addWidget(btn)
        legend.addStretch()
        main_layout.addLayout(legend)
        main_layout.addStretch()

    def _load_players(self):
        print("Graphique Wellness en construction")
        
    def _refresh(self):
        """Recharge la liste des joueurs depuis la BDD."""
        self._load_players()