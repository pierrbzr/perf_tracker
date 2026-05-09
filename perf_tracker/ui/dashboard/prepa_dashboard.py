"""
ui/dashboard/prepa_dashboard.py
Dashboard préparateur physique — placeholder en attendant le vrai contenu.
"""

from queue import Full

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal

from models.wellness import calc_average_wellness, get_submission_wellness_rate_today
from models.rpe import calc_average_rpe, get_submission_rpe_rate_today
from models.grip import get_team_grip_today, get_submission_grip_rate_today
from models.poids import get_team_poids_today, get_submission_poids_rate_today

from numpy import mean

from assets.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_BG_CARD, COLOR_BG_INPUT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_BORDER, COLOR_BORDER_ACTIVE, FONT_FAMILY,
    FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS, PADDING_CARD
)

class PrepaDashboard(QWidget):
    go_to_wellness = pyqtSignal()
    go_to_rpe = pyqtSignal()
    go_to_grip = pyqtSignal()
    go_to_poids = pyqtSignal()
    go_to_players = pyqtSignal()
    go_to_wellness_graph = pyqtSignal()
    go_to_rpe_graph = pyqtSignal()
    go_to_grip_graph = pyqtSignal()
    go_to_poids_graph = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()

    def calc_fill_rate_wellness(self) -> float:
        wellness_rate = get_submission_wellness_rate_today()
        
        if (wellness_rate["rate"]) is None:
            return ["-"]
        else:
            return str(wellness_rate["rate"]) + "%"
            
    def calc_fill_rate_rpe(self) -> float:
        rpe_rate = get_submission_rpe_rate_today()
        
        if (rpe_rate["rate"]) is None:
            return ["-"]
        else:
            return str(rpe_rate["rate"]) + "%"
        
    def calc_average_grip(self):
        team_grip = get_team_grip_today()
        
        grip = []
                
        for joueur in team_grip:
            if joueur['grip'] is not None:
                grip.append(joueur['grip'])
                
        if not grip:
            return ["-", "-", "-"]

        return [
            round(max(grip), 2),
            round(min(grip), 2),
            round(mean(grip), 2),
        ]
            
    def calc_fill_rate_grip(self) -> float:
        grip_rate = get_submission_grip_rate_today()
        
        if (grip_rate["rate"]) is None:
            return ["-"]
        else:
            return str(grip_rate["rate"]) + "%"
        
    def calc_average_poids(self):
        team_poids = get_team_poids_today()
        
        poids = []
                
        for joueur in team_poids:
            if joueur['poids'] is not None:
                poids.append(joueur['poids'])
                
        if not poids:
            return ["-", "-", "-"]

        return [
            round(max(poids), 2),
            round(min(poids), 2),
            round(mean(poids), 2),        ]
            
    def calc_fill_rate_poids(self) -> float:
        poids_rate = get_submission_poids_rate_today()
        
        if (poids_rate["rate"]) is None:
            return ["-"]
        else:
            return str(poids_rate["rate"]) + "%"

        
    def _build_ui(self):

        average_wellness = calc_average_wellness()
        fill_rate_wellness = self.calc_fill_rate_wellness()

        average_rpe = calc_average_rpe()
        fill_rate_rpe = self.calc_fill_rate_rpe()
        
        average_grip = self.calc_average_grip()
        fill_rate_grip = self.calc_fill_rate_grip()
        
        average_poids = self.calc_average_poids()
        fill_rate_poids = self.calc_fill_rate_poids()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # ── Title Layout ──────────────────────────────────────
        title_layout = QHBoxLayout()
        title_label = QLabel(f"🏒  Dashboard Préparateur Physique")
        title_label.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
        """)

        logout_btn = QPushButton("Se Déconnecter")
        logout_btn.setFixedWidth(160)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout_requested.emit)

        title_layout.addWidget(title_label, alignment=Qt.AlignLeft)
        title_layout.addStretch()
        title_layout.addWidget(logout_btn, alignment=Qt.AlignRight)
        main_layout.addLayout(title_layout)

 # ── Layout Wellness / RPE ───────────────────────────────────────
 
        wellness_rpe_layout = QHBoxLayout()
        grip_poids_layout = QHBoxLayout()
        player_layout = QHBoxLayout()
        wellness_rpe_layout.setSpacing(16)
        grip_poids_layout.setSpacing(16)
        player_layout.setSpacing(16)
        main_layout.addLayout(wellness_rpe_layout)
        main_layout.addLayout(grip_poids_layout)
        #main_layout.addLayout(player_layout)

 # ── Widget Wellness ───────────────────────────────────────
        
        wellness_frame = QFrame()
        wellness_frame.setObjectName("wellness")
        wellness_frame.setMinimumHeight(200)
        wellness_frame.setMaximumHeight(600)
        
        wellness_frame.setStyleSheet(f"""                   
            background-color: {COLOR_BG_CARD}; 
            border-radius: 10px;
        """)

        wellness_layout = QVBoxLayout(wellness_frame)
        wellness_layout.setContentsMargins(16, 16, 16, 16)
        wellness_layout.setSpacing(12)
        
        # Titre
        wellness_title = QLabel("Wellness : ")
        wellness_title.setAlignment(Qt.AlignLeft)
        wellness_title.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: 20px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        wellness_layout.addWidget(wellness_title)

        # Label Wellness
        label_style = f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
        """
        value_style = f"""
            color: {COLOR_GREEN};
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """
 
        for nom_label, valeur in [
            ("Sommeil",      average_wellness[0]),
            ("Énergie",      average_wellness[1]),
            ("Humeur",       average_wellness[2]),
            ("Courbatures",  average_wellness[3]),
            ("Stress",       average_wellness[4]),
        ]:
            row = QHBoxLayout()
            row.setContentsMargins(4, 0, 4, 0)
 
            lbl = QLabel(nom_label)
            lbl.setStyleSheet(label_style)
 
            val = QLabel(str(valeur))
            val.setAlignment(Qt.AlignRight)
            val.setStyleSheet(value_style)
 
            row.addWidget(lbl)
            row.addWidget(val)
 
            wellness_layout.addLayout(row)
            wellness_layout.addStretch(1)

        # Séparateur
        wellness_separator = QFrame()
        wellness_separator.setFixedHeight(1)
        wellness_separator.setStyleSheet("background-color: #2e3134;")
        wellness_layout.addWidget(wellness_separator)
        
        # Total
        total_row = QHBoxLayout()
        total_row.setContentsMargins(4, 0, 4, 0)
        
        total_lbl = QLabel("Total")
        total_lbl.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        
        total_val = QLabel(str(average_wellness[5]))
        total_val.setAlignment(Qt.AlignRight)
        total_val.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        
        total_row.addWidget(total_lbl)
        total_row.addStretch()
        total_row.addWidget(total_val)
        wellness_layout.addLayout(total_row)
        wellness_layout.addSpacing(12)
        
        # Taux de remplissage
        wellness_rate_row = QHBoxLayout()
        wellness_rate_row.setContentsMargins(4, 0, 4, 0)
        
        wellness_rate_label = QLabel("Taux de Remplissage")
        wellness_rate_label.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        
        wellness_rate_val = QLabel(fill_rate_wellness)
        wellness_rate_val.setAlignment(Qt.AlignRight)
        wellness_rate_val.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        
        wellness_rate_row.addWidget(wellness_rate_label)
        wellness_rate_row.addStretch()
        wellness_rate_row.addWidget(wellness_rate_val)
        wellness_layout.addLayout(wellness_rate_row)
        wellness_layout.addSpacing(12)

        # Layout Boutons
        
        wellness_btn_layout = QHBoxLayout()
        wellness_btn_layout.setContentsMargins(0, 8, 0, 8)

        # Bouton Wellness
        wellness_btn = QPushButton("Gérer Wellness")
        wellness_btn.setCursor(Qt.PointingHandCursor)
        wellness_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        wellness_btn.clicked.connect(self.go_to_wellness.emit)
        
        # Bouton Graphique
        graph_wellness_btn = QPushButton("Graphiques Wellness")
        graph_wellness_btn.setCursor(Qt.PointingHandCursor)
        graph_wellness_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        graph_wellness_btn.clicked.connect(self.go_to_wellness_graph.emit)
        
        wellness_layout.addLayout(wellness_btn_layout)
        wellness_btn_layout.addWidget(graph_wellness_btn)
        wellness_btn_layout.addWidget(wellness_btn)


# ── Widget RPE ────────────────────────────────────────
        rpe_frame = QFrame()
        rpe_frame.setObjectName("rpe")
        rpe_frame.setMinimumHeight(200)
        rpe_frame.setMaximumHeight(600)

        rpe_frame.setStyleSheet(f"""
            QFrame#rpe {{
                background-color: {COLOR_BG_CARD};
                border-radius: 10px;
            }}
        """)

        rpe_layout = QVBoxLayout(rpe_frame)
        rpe_layout.setContentsMargins(16, 16, 16, 16)
        rpe_layout.setSpacing(12)
        
        # Titre
        rpe_title = QLabel("RPE :")
        wellness_title.setAlignment(Qt.AlignLeft)
        rpe_title.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            background-color: transparent;
            font-size: 20px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        rpe_layout.addWidget(rpe_title)
        
        # Label RPE
        label_style = f"""
            color: {COLOR_TEXT_PRIMARY};
            background-color: transparent;
            font-size: 14px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
        """
        value_style = f"""
            color: {COLOR_GREEN};
            background-color: transparent;
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """
        
        for nom_label, valeur in [
            ("RPE Musculaire", average_rpe[0]),
            ("RPE Cardio",     average_rpe[1]),
        ]:
            row = QHBoxLayout()
            row.setContentsMargins(4, 0, 4, 0)
            
            lbl = QLabel(nom_label)
            lbl.setStyleSheet(label_style)
            
            val = QLabel(str(valeur))
            val.setAlignment(Qt.AlignRight)
            val.setStyleSheet(value_style)
            
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            
            rpe_layout.addLayout(row)
            rpe_layout.addStretch(1)

        # Séparateur
        rpe_separator = QFrame()
        rpe_separator.setFixedHeight(1)
        rpe_separator.setStyleSheet("background-color: #2e3134;")
        rpe_layout.addWidget(rpe_separator)

        # Taux de remplissage RPE
        rpe_rate_row = QHBoxLayout()
        rpe_rate_row.setContentsMargins(4, 0, 4, 0)
        
        rpe_rate_lbl = QLabel("Taux de Remplissage")
        rpe_rate_lbl.setStyleSheet(label_style)
        
        rpe_rate_val = QLabel(fill_rate_rpe)
        rpe_rate_val.setAlignment(Qt.AlignRight)
        rpe_rate_val.setStyleSheet(value_style)
        
        rpe_rate_row.addWidget(rpe_rate_lbl)
        rpe_rate_row.addStretch()
        rpe_rate_row.addWidget(rpe_rate_val)
        rpe_layout.addLayout(rpe_rate_row)
        rpe_layout.addSpacing(12)
        
        # Layout Boutons
        
        rpe_btn_layout = QHBoxLayout()
        rpe_btn_layout.setContentsMargins(0, 8, 0, 8)

        # Bouton RPE
        rpe_btn = QPushButton("Gérer RPE")
        rpe_btn.setCursor(Qt.PointingHandCursor)
        rpe_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        rpe_btn.clicked.connect(self.go_to_rpe.emit)
        
        # Bouton Graphique
        graph_rpe_btn = QPushButton("Graphiques RPE")
        graph_rpe_btn.setCursor(Qt.PointingHandCursor)
        graph_rpe_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        graph_rpe_btn.clicked.connect(self.go_to_rpe_graph.emit)
        
        rpe_layout.addLayout(rpe_btn_layout)
        rpe_btn_layout.addWidget(graph_rpe_btn)
        rpe_btn_layout.addWidget(rpe_btn)
        
# ── Widget Grip ────────────────────────────────────────
        grip_frame = QFrame()
        grip_frame.setObjectName("grip")
        grip_frame.setMinimumHeight(200)
        grip_frame.setMaximumHeight(600)

        grip_frame.setStyleSheet(f"""
            QFrame#grip {{
                background-color: {COLOR_BG_CARD};
                border-radius: 10px;
            }}
        """)

        grip_layout = QVBoxLayout(grip_frame)
        grip_layout.setContentsMargins(16, 16, 16, 16)
        grip_layout.setSpacing(12)

        grip_title = QLabel("Grip :")
        grip_title.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            background-color: transparent;
            font-size: 20px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        grip_layout.addWidget(grip_title)
        
        # Label Grip
        label_style = f"""
            color: {COLOR_TEXT_PRIMARY};
            background-color: transparent;
            font-size: 14px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
        """
        value_style = f"""
            color: {COLOR_GREEN};
            background-color: transparent;
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """
        
        for nom_label, valeur in [
            ("Grip Max", average_grip[0]),
            ("Grip Moyen", average_grip[2]),
            ("Grip Min", average_grip[1]),
        ]:
            
            row = QHBoxLayout()
            row.setContentsMargins(4, 0, 4, 0)
            
            lbl = QLabel(nom_label)
            lbl.setStyleSheet(label_style)
            
            val = QLabel(str(valeur))
            val.setAlignment(Qt.AlignRight)
            val.setStyleSheet(value_style)
            
            row.addWidget(lbl)
            row.addWidget(val)
            
            grip_layout.addLayout(row)
            grip_layout.addStretch(1)

        # Séparateur
        grip_separator = QFrame()
        grip_separator.setFixedHeight(1)
        grip_separator.setStyleSheet("background-color: #2e3134;")
        grip_layout.addWidget(grip_separator)

        # Taux de remplissage Grip
        grip_rate_row = QHBoxLayout()
        grip_rate_row.setContentsMargins(4, 0, 4, 0)
        
        grip_rate_lbl = QLabel("Taux de Remplissage")
        grip_rate_lbl.setStyleSheet(label_style)
        
        grip_rate_val = QLabel(fill_rate_grip)
        grip_rate_val.setAlignment(Qt.AlignRight)
        grip_rate_val.setStyleSheet(value_style)
        
        grip_rate_row.addWidget(grip_rate_lbl)
        grip_rate_row.addStretch()
        grip_rate_row.addWidget(grip_rate_val)
        grip_layout.addLayout(grip_rate_row)
        grip_layout.addSpacing(12)
        
        # Layout Boutons
        
        grip_btn_layout = QHBoxLayout()
        grip_btn_layout.setContentsMargins(0, 8, 0, 8)

        # Bouton RPE
        grip_btn = QPushButton("Gérer Grip")
        grip_btn.setCursor(Qt.PointingHandCursor)
        grip_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        grip_btn.clicked.connect(self.go_to_grip.emit)
        
        # Bouton Graphique
        graph_grip_btn = QPushButton("Graphiques Grip")
        graph_grip_btn.setCursor(Qt.PointingHandCursor)
        graph_grip_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        graph_grip_btn.clicked.connect(self.go_to_grip_graph.emit)
        
        grip_layout.addLayout(grip_btn_layout)
        grip_btn_layout.addWidget(graph_grip_btn)
        grip_btn_layout.addWidget(grip_btn)
        
# ── Widget Poids ────────────────────────────────────────
        poids_frame = QFrame()
        poids_frame.setObjectName("poids")
        poids_frame.setMinimumHeight(200)
        poids_frame.setMaximumHeight(600)

        poids_frame.setStyleSheet(f"""
            QFrame#poids {{
                background-color: {COLOR_BG_CARD};
                border-radius: 10px;
            }}
        """)

        poids_layout = QVBoxLayout(poids_frame)
        poids_layout.setContentsMargins(16, 16, 16, 16)
        poids_layout.setSpacing(12)

        poids_title = QLabel("Poids :")
        poids_title.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            background-color: transparent;
            font-size: 20px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """)
        poids_layout.addWidget(poids_title)
        
        # Label Poids
        label_style = f"""
            color: {COLOR_TEXT_PRIMARY};
            background-color: transparent;
            font-size: 14px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
        """
        value_style = f"""
            color: {COLOR_GREEN};
            background-color: transparent;
            font-size: 14px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
        """
        
        for nom_label, valeur in [
            (f"Poids Max", average_poids[0]),
            (f"Poids Moyen", average_poids[2]),
            (f"Poids Min", average_poids[1]),
        ]:
            row = QHBoxLayout()
            row.setContentsMargins(4, 0, 4, 0)
            
            lbl = QLabel(nom_label)
            lbl.setStyleSheet(label_style)
            
            val = QLabel(str(valeur))
            val.setAlignment(Qt.AlignRight)
            val.setStyleSheet(value_style)
            
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            
            poids_layout.addLayout(row)
            poids_layout.addStretch(1)

        # Séparateur
        poids_separator = QFrame()
        poids_separator.setFixedHeight(1)
        poids_separator.setStyleSheet("background-color: #2e3134;")
        poids_layout.addWidget(poids_separator)

        # Taux de remplissage Poids
        poids_rate_row = QHBoxLayout()
        poids_rate_row.setContentsMargins(4, 0, 4, 0)
        
        poids_rate_lbl = QLabel("Taux de Remplissage")
        poids_rate_lbl.setStyleSheet(label_style)
        
        poids_rate_val = QLabel(fill_rate_poids)
        poids_rate_val.setAlignment(Qt.AlignRight)
        poids_rate_val.setStyleSheet(value_style)
        
        poids_rate_row.addWidget(poids_rate_lbl)
        poids_rate_row.addStretch()
        poids_rate_row.addWidget(poids_rate_val)
        poids_layout.addLayout(poids_rate_row)
        poids_layout.addSpacing(12)
        
        # Layout Boutons
        
        poids_btn_layout = QHBoxLayout()
        poids_btn_layout.setContentsMargins(0, 8, 0, 8)

        # Bouton poids
        poids_btn = QPushButton("Gérer Poids")
        poids_btn.setCursor(Qt.PointingHandCursor)
        poids_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        poids_btn.clicked.connect(self.go_to_poids.emit)
        
        # Bouton Graphique
        graph_poids_btn = QPushButton("Graphiques Poids")
        graph_poids_btn.setCursor(Qt.PointingHandCursor)
        graph_poids_btn.setStyleSheet(f"""
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
            QPushButton:hover {{ background-color: #00C962; }}
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        graph_poids_btn.clicked.connect(self.go_to_poids_graph.emit)
        
        poids_layout.addLayout(poids_btn_layout)
        poids_btn_layout.addWidget(graph_poids_btn)
        poids_btn_layout.addWidget(poids_btn)
        
        

# ── Ajout des frames ──────────────────────────────────
        wellness_rpe_layout.addWidget(wellness_frame)
        wellness_rpe_layout.addWidget(rpe_frame)
        grip_poids_layout.addWidget(grip_frame)
        grip_poids_layout.addWidget(poids_frame)
        
# ── Bouton de redirection vers la Liste des Joueurs ──────────────────────────────────

        player_btn = QPushButton("Liste des Joueurs")
        player_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: 2px solid {COLOR_GREEN};
                border-radius: {BORDER_RADIUS}px;
                padding: 10px;
                font-size: {FONT_SIZE_BODY}px;
                font-weight: 700;
                font-family: "{FONT_FAMILY}";
            }}
           QPushButton:hover {{
                background-color: {COLOR_GREEN};
                color: white;
            }}            
            QPushButton:pressed {{ background-color: #007A3D; }}
        """)
        player_btn.clicked.connect(self.go_to_players.emit)
                
        main_layout.addWidget(player_btn)

def _refresh_wellness(self):
        """Recharge les données depuis la BDD — appelé au retour sur le dashboard."""
        self.__init__(self.user)
        

