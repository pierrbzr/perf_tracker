"""
ui/player_form.py


"""

import re

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal

#from PyQt6 import QtCore, QtGui

from assets.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_BG_CARD, COLOR_BG_INPUT, COLOR_BORDER,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS, PADDING_CARD
)




class PlayerForm(QWidget):
    """
    Profil du joueur.
    Émet back_requested() pour retourner à la liste.
    """
    back_requested   = pyqtSignal()

    def __init__(self, player: dict, parent=None):
        super().__init__(parent)
        self.player = player
        self._build_ui()

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
            f"Profil de Joueur — {self.player['prenom']} {self.player['nom']}"
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
        
        # ── Liste joueurs scrollable ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(8)

        scroll.setWidget(self.list_widget)

        # ── Carte formulaire ──
        idendity_card = QFrame()
        idendity_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)
        idendity_card.setMaximumHeight(150)

        idendity_card_layout = QHBoxLayout(idendity_card)
        idendity_card_layout.setContentsMargins(PADDING_CARD, PADDING_CARD,
                                       PADDING_CARD, PADDING_CARD)
        idendity_card_layout.setSpacing(24)

        
# ── Cercle avec initiales

        nom = (f"{self.player['prenom']}" + " " + f"{self.player['nom']}")
        initiales = re.findall(r'\b([a-zA-Z]|\d+)', nom)
        initiale = initiales[0] + initiales[1]
        
        circle = QLabel(initiale)
        circle.setFixedSize(80, 80)
        circle.setAlignment(Qt.AlignCenter)
        circle.setStyleSheet("""
            QLabel {
                background-color: {COLOR_BG_INPUT};
                color: white;
                border-radius: 40px;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        idendity_card_layout.addWidget(circle)

# ── Nom et Prénom 

        infos_layout = QVBoxLayout()
        infos_layout.setSpacing(14)
        
        nom = QLabel(f"{self.player['prenom']} {self.player['nom']}")
        nom.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: {FONT_SIZE_BODY}px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        infos_layout.addWidget(nom)

# ── Détails du joueur

        details_layout = QHBoxLayout()
        details_layout.setSpacing(50)

# ── Poste et Taille

        left_col = QVBoxLayout()
        left_col.setSpacing(10)
        
        poste = QLabel(f"<b>Poste :</b> {self.player['poste']}")
        poste.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        taille = QLabel(f"<b>Taille :</b> {self.player['taille']} cm")
        taille.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        left_col.addWidget(poste)
        left_col.addWidget(taille)
        
# ── Numéro et Poids
  
        right_col = QVBoxLayout()
        right_col.setSpacing(10)
        
        numero = QLabel(f"<b>Numéro :</b>  #{self.player['numero']}")
        numero.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        poids = QLabel(f"<b>Poids :</b> {self.player['poids']} kg")
        poids.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        right_col.addWidget(numero)
        right_col.addWidget(poids)
        
# ── Ajout et disposition dans la carte
     
        details_layout.addLayout(left_col)
        details_layout.addLayout(right_col)
        
        infos_layout.addLayout(details_layout)
        
        idendity_card_layout.addLayout(infos_layout)
        idendity_card_layout.addStretch

        #scroll.setWidget(idendity_card)
        main_layout.addWidget(idendity_card)

# ── Carte des Statistiques

        stats_card = QFrame()
        stats_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)

        stats_card_layout = QHBoxLayout(stats_card)
        stats_card_layout.setContentsMargins(PADDING_CARD, PADDING_CARD,
                                       PADDING_CARD, PADDING_CARD)
        stats_card_layout.setSpacing(24)

        pr_label = QLabel("Records Personnels")
        pr_label.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        stats_card_layout.addWidget(pr_label)
        main_layout.addWidget(stats_card)
        main_layout.addStretch()



    # ── Logique ─────────────────────────────────────────────




    # ── Styles boutons ───────────────────────────────────────
