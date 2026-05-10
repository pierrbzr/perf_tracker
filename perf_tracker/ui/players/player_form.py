"""
ui/player_form.py
"""

import re

from PyQt5.QtWidgets import (
    QGridLayout, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal

#from PyQt6 import QtCore, QtGui

from assets.theme import (
    COLOR_GREEN, COLOR_GREEN_DARK, COLOR_GREEN_LIGHT, COLOR_RED, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_BG_CARD, COLOR_BG_INPUT, COLOR_BORDER,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS, PADDING_CARD, FONT_SIZE_SUBTITLE
)

# ── Définition des données ──────────────────────────────────────

CARDS = [
    {
        "id": "bench",
        "title": "Bench :",
        "value": "100kg", 
    },
    {
        "id": "squat",
        "title": "Squat :",
        "value": "160kg", 
    },
    {
        "id": "deadlift",
        "title": "Deadlift :",
        "value": "180kg", 
    },
    {
        "id": "clean",
        "title": "Clean :",
        "value": "90kg", 
    },
    {
        "id": "broad_jump",
        "title": "Broad Jump :",
        "value": "250 cm", 
    },
    {
        "id": "cmj",
        "title": "CMJ :",
        "value": "43cm", 
    },
    {
        "id": "pull_up",
        "title": "Pull Up :",
        "value": "12", 
    },
    {
        "id": "sprint_5m",
        "title": "Sprint 5m :",
        "value": "1'04", 
    },
    {
        "id": "sprint_10m",
        "title": "Sprint 10m :",
        "value": "1'94", 
    },
    {
        "id": "sprint_20m",
        "title": "Sprint 20m :",
        "value": "3'10", 
    },
    
]

def make_card(data):
    card = QFrame()
    card.setObjectName("card")
    card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)
    card.setMinimumHeight(140)
    card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    
    layout = QVBoxLayout(card)
    layout.setContentsMargins(PADDING_CARD, PADDING_CARD,
                                       PADDING_CARD, PADDING_CARD)
    layout.setSpacing(12)
    
    value_layout = QHBoxLayout()
    value_layout.setContentsMargins(0, 12, 0, 0)
    value_layout.setSpacing(0)
    
    # Titre
    titre_label = QLabel(data["title"])
    titre_label.setObjectName("cardTitle")
    titre_label.setWordWrap(True)
    titre_label.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: {FONT_SIZE_SUBTITLE}px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
    
    # Valeur
    valeur_label = QLabel(f"    " + data["value"])
    valeur_label.setObjectName("cardValue")
    valeur_label.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SUBTITLE}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
    
    btn_layout = QHBoxLayout()
    btn_layout.setContentsMargins(20, 0, 20, 0)
    btn_layout.setSpacing(0)
    
    # Bouton 
    btn = QPushButton("Voir Détails")
    btn.setObjectName("cardButton")
    btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_GREEN};
                color: white;
                border: none;
                border-radius: {BORDER_RADIUS}px;
                font-size: {FONT_SIZE_BODY}px;
                font-weight: 700;
                font-family: "{FONT_FAMILY}";
                padding: 10px;
            }}
            QPushButton:hover {{ background-color: {COLOR_GREEN_LIGHT}; }}
            QPushButton:pressed {{ background-color: {COLOR_GREEN_DARK}; }}
        """)
    btn.setCursor(Qt.PointingHandCursor)
    btn.clicked.connect(lambda checked, d=data: print(f"[Card {d['id']}] {d['title']} → {d['value']}"))

    value_layout.addStretch()
    value_layout.addWidget(titre_label)
    value_layout.addWidget(valeur_label)
    value_layout.addStretch()
    
    btn_layout.addWidget(btn)
    
    layout.addLayout(value_layout)
    layout.addStretch()
    layout.addLayout(btn_layout)

    return card


class CardsContainer(QFrame):
    COLUMNS = 3          # nb de colonnes max
    CARD_MIN_W = 180     # largeur minimale d'une carte (px)

    def __init__(self, cards_data, parent=None):
        super().__init__(parent)
        self.setObjectName("cardsContainer")
        self.cards_data = cards_data

        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(16, 16, 16, 16)
        self._grid.setSpacing(12)

        self._build_grid(self.COLUMNS)

    # Reconstruit la grille avec `cols` colonnes
    def _build_grid(self, cols: int):
        # Vider sans détruire les widgets
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        for i, data in enumerate(self.cards_data):
            row, col = divmod(i, cols)
            card = make_card(data)
            self._grid.addWidget(card, row, col)

        # Colonnes de poids égal → responsive
        for c in range(cols):
            self._grid.setColumnStretch(c, 1)

    # Recalcule le nb de colonnes selon la largeur disponible
    def resizeEvent(self, event):
        super().resizeEvent(event)
        available_w = event.size().width() - 32   # marges
        cols = max(1, available_w // self.CARD_MIN_W)
        cols = min(cols, self.COLUMNS)

        current_cols = self._grid.columnCount()
        if cols != current_cols:
            self._build_grid(cols)
            
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

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")  # ← évite un fond blanc parasite
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)
        
        # ── Carte Idendité ──
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
        circle.setStyleSheet(f"""
            QLabel {{
                background-color: {COLOR_BG_INPUT};
                color: white;
                border-radius: 40px;
                font-size: 28px;
                font-weight: bold;
            }}
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
        details_layout.setSpacing(100)

# ── Poste et Numéro

        poste = QLabel(f"<b>Poste :</b> {self.player['poste']}")
        poste.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        numero = QLabel(f"<b>Numéro :</b>  #{self.player['numero']}")
        numero.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

# ── Taille et Poids
        
        taille = QLabel(f"<b>Taille :</b> {self.player['taille']} cm")
        taille.setStyleSheet(f"""
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

# ── Ajout et disposition dans la carte

        infos_layout.addLayout(details_layout)
        
        idendity_card_layout.addLayout(infos_layout)
        idendity_card_layout.addStretch()
        
        details_layout.addWidget(poste)
        details_layout.addWidget(numero)
        details_layout.addWidget(taille)
        details_layout.addWidget(poids)

        scroll_layout.addWidget(idendity_card)

# ── Carte des Statistiques

        stats_card = QFrame()
        stats_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)

        stats_card_layout = QVBoxLayout(stats_card)
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
        
        container = CardsContainer(CARDS)
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: none;
                background: transparent;
            }}
        """)
        
        stats_card_layout.addWidget(pr_label)
        stats_card_layout.addWidget(container)
        #main_layout.addWidget(stats_card)
        scroll_layout.addWidget(stats_card)

# ── Carte des Graphiques

        graphs_card = QFrame()
        graphs_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)

        graphs_card_layout = QHBoxLayout(graphs_card)
        graphs_card_layout.setContentsMargins(PADDING_CARD, PADDING_CARD,
                                       PADDING_CARD, PADDING_CARD)
        graphs_card_layout.setSpacing(24)

        graphs_label = QLabel("Graphiques Personnels")
        graphs_label.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        graphs_card_layout.addWidget(graphs_label)
        scroll_layout.addWidget(graphs_card)

        
# ── Carte des Données

        data_card = QFrame()
        data_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)

        data_card_layout = QHBoxLayout(data_card)
        data_card_layout.setContentsMargins(PADDING_CARD, PADDING_CARD,
                                       PADDING_CARD, PADDING_CARD)
        data_card_layout.setSpacing(24)

        data_label = QLabel("Données numériques")
        data_label.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        data_card_layout.addWidget(data_label)
        scroll_layout.addWidget(data_card)
        
        
        
        
        
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)



    # ── Logique ─────────────────────────────────────────────




    # ── Styles boutons ───────────────────────────────────────
