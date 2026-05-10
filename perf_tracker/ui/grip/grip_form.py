"""
ui/grip_form.py
Formulaire de saisie grip pour un joueur sélectionné.
5 indicateurs de 0 à 5 avec boutons de sélection.
"""

from PyQt5.QtWidgets import (
    QDoubleSpinBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from assets.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_BG_CARD, COLOR_BG_INPUT, COLOR_BORDER,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS, PADDING_CARD
)
from models.grip import create_grip, has_grip_submitted_today, get_grip_today


class GripForm(QWidget):
    """
    Formulaire grip pour un joueur.
    Émet back_requested() pour retourner à la liste.
    """
    back_requested   = pyqtSignal()
    grip_saved   = pyqtSignal()

    def __init__(self, player: dict, parent=None):
        super().__init__(parent)
        self.player   = player
        self._build_ui()
        self._check_already_submitted()

    # ── Construction UI ──────────────────────────────────────

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
        """)
        back_btn.clicked.connect(self.back_requested.emit)

        title = QLabel(
            f"Grip — {self.player['prenom']} {self.player['nom']}"
        )
        title.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
        """)

        header.addWidget(back_btn)
        header.addSpacing(16)
        header.addWidget(title)
        header.addStretch()
        main_layout.addLayout(header)

        # ── Carte formulaire ──
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(PADDING_CARD, PADDING_CARD,
                                       PADDING_CARD, PADDING_CARD)
        card_layout.setSpacing(16)

        # ── Indicateurs ──
        row_frame = QFrame()
        row_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_INPUT};
                border-radius: 8px;
            }}
        """)
        row_layout = QVBoxLayout(row_frame)
        row_layout.setContentsMargins(12, 8, 12, 8)
        row_layout.setSpacing(8)
        
        # Libellé
        lbl = QLabel("Force du Grip")
        lbl.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: {FONT_SIZE_BODY}px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

        desc = QLabel("Meilleur score des deux mains")
        desc.setStyleSheet(f"""
        color: {COLOR_TEXT_SECONDARY};
        font-size: {FONT_SIZE_SMALL}px;
        font-family: "{FONT_FAMILY}";
        border: none;
        background: transparent;
        """)
        
        # Zone de texte
        self.sb_grip = QDoubleSpinBox()
        self.sb_grip.setRange(0.0, 100.0)
        self.sb_grip.setSingleStep(0.1)
        self.sb_grip.setDecimals(1)

        row_layout.addWidget(lbl)
        row_layout.addWidget(desc)
        row_layout.addWidget(self.sb_grip)
        card_layout.addWidget(row_frame)

        # ── Message erreur ──
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet(f"""
            color: {COLOR_RED};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)

        # ── Bouton enregistrer ──
        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.setFixedHeight(46)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_GREEN};
                color: white;
                border: none;
                border-radius: {BORDER_RADIUS}px;
                font-size: {FONT_SIZE_BODY}px;
                font-weight: 700;
                font-family: "{FONT_FAMILY}";
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
            QPushButton:disabled {{
                background-color: #2A2A2A;
                color: #606060;
            }}
        """)
        self.save_btn.clicked.connect(lambda: self._on_save(self.sb_grip.value()))
        card_layout.addWidget(self.save_btn)

        main_layout.addWidget(card)
        main_layout.addStretch()

    # ── Logique ─────────────────────────────────────────────

    def _check_already_submitted(self):
        """Pré-remplit le formulaire si déjà saisi aujourd'hui, mais reste modifiable."""
        if has_grip_submitted_today(self.player["id"]):
            
            # Pré-remplir les valeurs
            value = get_grip_today(self.player["id"])
            valeur = value["grip"]
            print(valeur)
            if valeur is not None:
                self.sb_grip.setValue(valeur)
                self.sb_grip.setStyleSheet("color : gray;")
                self.save_btn.setText("Modifier la saisie")
            else:
                self.sb_grip.setStyleSheet("")
        
            self.error_label.setStyleSheet(f"""
                color: {COLOR_GREEN};
                font-size: {FONT_SIZE_SMALL}px;
                font-family: "{FONT_FAMILY}";
                border: none;
                background: transparent;
            """)
            self.error_label.show()

    def _on_save(self, value:float):
        try:
            create_grip(
                player_id   = self.player["id"],
                grip     = value,

            )
            self.save_btn.setEnabled(False)
            self.save_btn.setText("Enregistré !")
            self.grip_saved.emit()

        except Exception as e:
            self.error_label.setText(f"Erreur : {str(e)}")
            self.error_label.show()