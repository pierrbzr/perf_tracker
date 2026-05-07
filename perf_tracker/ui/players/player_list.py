"""
ui/player_list.py
Liste des joueurs  et affichage des données.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal

from assets.theme import (
    COLOR_GREEN, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_BG_CARD, COLOR_BG_HOVER, COLOR_BORDER,
    COLOR_GOOD, COLOR_WARNING, COLOR_DANGER, COLOR_NEUTRAL,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS
)
from models.player import get_all_players
from models.wellness import has_wellness_submitted_today
from models.rpe import has_rpe_submitted_today
from models.grip import has_grip_submitted_today
from models.poids import has_poids_submitted_today

class PlayerList(QWidget):
    """
    Liste des joueurs avec indication si les paramètres ont déjà été saisi aujourd'hui.
    Émet player_selected(player_dict) au clic sur un joueur.
    """
    player_selected = pyqtSignal(dict)
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
        """)
        back_btn.clicked.connect(self.back_requested.emit)

        title = QLabel("Liste — Sélectionner un joueur")
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
        """)
        self.refresh_btn.clicked.connect(self._refresh)

        header.addWidget(back_btn)
        header.addSpacing(16)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
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
        main_layout.addWidget(scroll)

        self._load_players()

    def _load_players(self):
        # Vider la liste
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        players = get_all_players()

        for player in players:
            wellness_submitted = has_wellness_submitted_today(player["id"])
            rpe_submitted = has_rpe_submitted_today(player["id"])
            grip_submitted = has_grip_submitted_today(player["id"])
            poids_submitted = has_poids_submitted_today(player["id"])
            card = self._make_player_card(player, wellness_submitted, rpe_submitted, grip_submitted, poids_submitted)
            self.list_layout.addWidget(card)

        self.list_layout.addStretch()

    def _make_player_card(self, player: dict, wellness_submitted: bool, rpe_submitted: bool, grip_submitted: bool, poids_submitted: bool) -> QFrame:
        """Crée une carte joueur cliquable."""
        card = QFrame()
        card.setFixedHeight(72)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: {BORDER_RADIUS}px;
            }}
            QFrame:hover {{
                background-color: {COLOR_BG_HOVER};
                border-color: {COLOR_GREEN};
            }}
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        # ── Gauche : numéro + nom + poste ──

        # Numéro maillot
        numero = QLabel(f"#{player['numero']}")
        numero.setFixedWidth(40)
        numero.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

        # Nom complet
        nom = QLabel(f"{player['prenom']} {player['nom']}")
        nom.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: {FONT_SIZE_BODY}px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

        # Poste
        poste = QLabel(player['poste'] or "")
        poste.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        layout.addWidget(numero)
        layout.addWidget(nom)
        layout.addWidget(poste)
        layout.addStretch()

        # ── Droite : statuts + boutons ──
        
        right_layout = QHBoxLayout()
        right_layout.setSpacing(12)

        # Statut Wellness
        w_color = COLOR_GOOD if wellness_submitted else COLOR_DANGER
        w_statut = QLabel("Wellness")
        w_statut.setFixedWidth(80)
        w_statut.setAlignment(Qt.AlignCenter)
        w_statut.setStyleSheet(f"""
            color: {w_color};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        # Statut RPE
        r_color = COLOR_GOOD if rpe_submitted else COLOR_DANGER
        r_statut = QLabel("RPE")
        r_statut.setFixedWidth(80)
        r_statut.setAlignment(Qt.AlignCenter)
        r_statut.setStyleSheet(f"""
            color: {r_color};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        # Statut Grip
        g_color = COLOR_GOOD if grip_submitted else COLOR_DANGER
        g_statut = QLabel("Grip")
        g_statut.setFixedWidth(80)
        g_statut.setAlignment(Qt.AlignCenter)
        g_statut.setStyleSheet(f"""
            color: {g_color};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        
        # Statut Poids
        p_color = COLOR_GOOD if poids_submitted else COLOR_DANGER
        p_statut = QLabel("Poids")
        p_statut.setFixedWidth(80)
        p_statut.setAlignment(Qt.AlignCenter)
        p_statut.setStyleSheet(f"""
            color: {p_color};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

        # Bouton Affichage du Joueur
        a_btn = QPushButton("Afficher Profil")
        a_btn.setFixedSize(80, 36)
        a_btn.setCursor(Qt.PointingHandCursor)
        a_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_GREEN};
                border: 2px solid {COLOR_GREEN};
                border-radius: {BORDER_RADIUS}px;
                font-size: {FONT_SIZE_SMALL}px;
                font-weight: 600;
                font-family: "{FONT_FAMILY}";
                min-width: 80px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_GREEN};
                color: white;
            }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        a_btn.clicked.connect(lambda: self.player_selected.emit(player))

        right_layout.addWidget(w_statut)
        right_layout.addWidget(r_statut)
        right_layout.addWidget(g_statut)
        right_layout.addWidget(p_statut)
        right_layout.addWidget(a_btn)

        layout.addLayout(right_layout)

        return card
       
    def _refresh(self):
        """Recharge la liste des joueurs depuis la BDD."""
        self._load_players()