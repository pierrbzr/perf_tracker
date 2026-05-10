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

from models.graphs import RPEChart


class RPETeamGraph(QWidget):
    """
    Liste des joueurs avec indication si grip déjà saisi aujourd'hui.
    Émet grip_selected(player_dict) au clic sur un joueur.
    """
    back_requested  = pyqtSignal()

    def __init__(self, days : int=7, parent=None):
        super().__init__(parent)
        self.days = days
        self._build_ui()
        
    def update_days_charts(self, new_days: int):
        if new_days == 1:
            self.chart.refresh_today()
        else:
            self.days = new_days
            self.chart.set_days(new_days)
            
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

        title = QLabel("Graphique — Évolution du RPE")
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
            ("Aujourd'hui", 1),
            ("7 jours", 7),
            ("14 jours", 14),
            ("30 jours", 30),
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
            btn.clicked.connect(lambda checked, d=attribut: self.update_days_charts(d))
            legend.addWidget(btn)
        legend.addStretch()
        main_layout.addLayout(legend)
        
        test_chart = QFrame()
        test_chart.setFixedHeight(500)
        
        layout = QHBoxLayout(test_chart)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)
        
        self.chart = RPEChart(30)
        self.chart.setMinimumHeight(500)
        layout.addWidget(self.chart)
        
        main_layout.addWidget(test_chart)
        
        main_layout.addStretch()
        
    def _refresh(self):
        self.chart.set_days(self.days)