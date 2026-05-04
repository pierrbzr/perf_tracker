"""
ui/rpe_form.py
Formulaire de saisie rpe pour un joueur sélectionné.
5 indicateurs de 0 à 5 avec boutons de sélection.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from assets.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_BG_CARD, COLOR_BG_INPUT, COLOR_BORDER,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS, PADDING_CARD
)
from models.rpe import create_rpe, has_rpe_submitted_today, get_rpe_today


# Libellés et descriptions des indicateurs
INDICATORS = [
    ("rpem",     "RPE Musculaire",      "Difficulté Musculaires"),
    ("rpec",      "RPE Cardio",       "Difficultés Cardio"),
]


class RPEForm(QWidget):
    """
    Formulaire rpe pour un joueur.
    Émet back_requested() pour retourner à la liste.
    """
    back_requested   = pyqtSignal()
    rpe_saved   = pyqtSignal()

    def __init__(self, player: dict, parent=None):
        super().__init__(parent)
        self.player   = player
        self.values   = {key: None for key, _, _ in INDICATORS}
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
            f"RPE — {self.player['prenom']} {self.player['nom']}"
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
        self.btn_groups = {}  # key → liste de boutons

        for key, label, description in INDICATORS:
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
            lbl = QLabel(f"{label}")
            lbl.setStyleSheet(f"""
                color: {COLOR_TEXT_PRIMARY};
                font-size: {FONT_SIZE_BODY}px;
                font-weight: 700;
                font-family: "{FONT_FAMILY}";
                border: none;
                background: transparent;
            """)

            desc = QLabel(description)
            desc.setStyleSheet(f"""
                color: {COLOR_TEXT_SECONDARY};
                font-size: {FONT_SIZE_SMALL}px;
                font-family: "{FONT_FAMILY}";
                border: none;
                background: transparent;
            """)

            # Boutons 1 à 10
            btns_layout = QHBoxLayout()
            btns_layout.setSpacing(18)
            btns = []

            for val in range(1, 11):
                btn = QPushButton(str(val))
                btn.setFixedSize(60, 40)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setProperty("indicator", key)
                btn.setProperty("value", val)
                btn.setStyleSheet(self._btn_style_inactive())
                btn.clicked.connect(
                    lambda checked, k=key, v=val: self._on_value_selected(k, v)
                )
                btns_layout.addWidget(btn)
                btns.append(btn)

            btns_layout.addStretch()
            self.btn_groups[key] = btns

            row_layout.addWidget(lbl)
            row_layout.addWidget(desc)
            row_layout.addLayout(btns_layout)
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
        self.save_btn.clicked.connect(self._on_save)
        card_layout.addWidget(self.save_btn)

        main_layout.addWidget(card)
        main_layout.addStretch()

    # ── Logique ─────────────────────────────────────────────

    def _check_already_submitted(self):
        """Pré-remplit le formulaire si déjà saisi aujourd'hui, mais reste modifiable."""
        if has_rpe_submitted_today(self.player["id"]):
            existing = get_rpe_today(self.player["id"])
            
            # Pré-remplir les valeurs
            for key, _, _ in INDICATORS:
                self._on_value_selected(key, existing[key])
                
            self.save_btn.setText("Modifier la saisie")
        
            self.error_label.setStyleSheet(f"""
                color: {COLOR_GREEN};
                font-size: {FONT_SIZE_SMALL}px;
                font-family: "{FONT_FAMILY}";
                border: none;
                background: transparent;
            """)
            self.error_label.show()

    def _on_value_selected(self, key: str, value: int):
        """Met à jour la valeur sélectionnée et rafraîchit les boutons."""
        self.values[key] = value

        # Rafraîchir les boutons du groupe
        for btn in self.btn_groups[key]:
            v = btn.property("value")
            if v == value:
                btn.setStyleSheet(self._btn_style_active())
            else:
                btn.setStyleSheet(self._btn_style_inactive())

    def _on_save(self):
        """Valide et enregistre le rpe en base."""
        # Vérifier que tout est rempli
        missing = [label for key, label, _ in INDICATORS
                   if self.values[key] is None]
        if missing:
            self.error_label.setText(
                f"Indicateur(s) manquant(s) : {', '.join(missing)}"
            )
            self.error_label.show()
            return

        self.error_label.hide()

        try:
            create_rpe(
                player_id   = self.player["id"],
                rpem     = self.values["rpem"],
                rpec      = self.values["rpec"],

            )
            self.save_btn.setEnabled(False)
            self.save_btn.setText("Enregistré !")
            self.rpe_saved.emit()

        except Exception as e:
            self.error_label.setText(f"Erreur : {str(e)}")
            self.error_label.show()

    # ── Styles boutons ───────────────────────────────────────

    def _btn_style_active(self) -> str:
        return f"""
            QPushButton {{
                background-color: {COLOR_GREEN};
                color: white;
                border: none;
                border-radius: {BORDER_RADIUS}px;
                font-size: {FONT_SIZE_BODY}px;
                font-weight: 700;
                font-family: "{FONT_FAMILY}";
            }}
        """

    def _btn_style_inactive(self) -> str:
        return f"""
            QPushButton {{
                background-color: {COLOR_BG_CARD};
                color: {COLOR_TEXT_SECONDARY};
                border: 1px solid {COLOR_BORDER};
                border-radius: {BORDER_RADIUS}px;
                font-size: {FONT_SIZE_BODY}px;
                font-weight: 700;
                font-family: "{FONT_FAMILY}";
            }}
        """