"""
ui/dashboard/prepa_dashboard.py
Dashboard préparateur physique — placeholder en attendant le vrai contenu.
"""

from queue import Full

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal

from models.wellness import get_team_wellness_today, get_submission_wellness_rate_today
from models.rpe import get_team_rpe_today, get_submission_rpe_rate_today

from numpy import mean # type: ignore

from assets.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_BG_CARD, COLOR_BG_INPUT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_BORDER, COLOR_BORDER_ACTIVE, FONT_FAMILY,
    FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS, PADDING_CARD
)

class PrepaDashboard(QWidget):
    go_to_wellness_rpe = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()

    def calc_average_wellness(self):

        team_wellness = get_team_wellness_today()

        sommeil = []
        humeur = []
        energie = []
        courbatures = []
        stress = []
        score_total = []

        for joueur in team_wellness:
            if joueur['score_total'] is not None:
                score_total.append(joueur['score_total'])
                sommeil.append(joueur['sommeil'])
                humeur.append(joueur['humeur'])
                energie.append(joueur['energie'])
                courbatures.append(joueur['courbatures'])
                stress.append(joueur['stress'])
                
        if not sommeil:
            return ["-", "-", "-", "-", "-", "-"]

        return [
        round(mean(sommeil), 2),
        round(mean(humeur), 2),
        round(mean(energie), 2),
        round(mean(courbatures), 2),
        round(mean(stress), 2),
        round(mean(score_total), 2),
    ]
    
    def calc_average_rpe(self):
        team_rpe = get_team_rpe_today()
        
        rpe_m = []
        rpe_c = []
                
        for joueur in team_rpe:
            if joueur['rpem'] is not None:
                rpe_m.append(joueur['rpem'])
                rpe_c.append(joueur['rpec'])
                
        if not rpe_m:
            return ["-", "-"]

        return [
            round(mean(rpe_m), 2),
            round(mean(rpe_c), 2),
        ]
    
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
        
    def _build_ui(self):

        average_wellness = self.calc_average_wellness()
        average_rpe = self.calc_average_rpe()
        fill_rate_wellness = self.calc_fill_rate_wellness()
        fill_rate_rpe = self.calc_fill_rate_rpe()

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
        wellness_rpe_layout.setSpacing(16)
        main_layout.addLayout(wellness_rpe_layout)

 # ── Widget Wellness ───────────────────────────────────────
        
        wellness_frame = QFrame()
        wellness_frame.setObjectName("wellness")
        wellness_frame.setMinimumHeight(200)
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
            row.addStretch()
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
        wellness_layout.addSpacing(8)

        # Bouton
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
        wellness_btn.clicked.connect(self.go_to_wellness_rpe.emit)
        wellness_layout.addWidget(wellness_btn)

        # ── Widget RPE ────────────────────────────────────────
        rpe_frame = QFrame()
        rpe_frame.setObjectName("rpe")
        rpe_frame.setMinimumHeight(200)
        rpe_frame.setStyleSheet(f"""
            QFrame#rpe {{
                background-color: {COLOR_BG_CARD};
                border-radius: 10px;
            }}
        """)

        rpe_layout = QVBoxLayout(rpe_frame)
        rpe_layout.setContentsMargins(16, 16, 16, 16)
        rpe_layout.setSpacing(12)

        rpe_title = QLabel("RPE :")
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
        rpe_btn.clicked.connect(self.go_to_wellness_rpe.emit)
        rpe_layout.addWidget(rpe_btn)

        # ── Ajout des frames ──────────────────────────────────
        wellness_rpe_layout.addWidget(wellness_frame)
        wellness_rpe_layout.addWidget(rpe_frame)
        
    # ── Widget Liste des joueurs ────────────────────────────────────────
        yellow_frame = QFrame()
        yellow_frame.setStyleSheet(
            "background-color: #5c4a00; border-radius: 10px;"
        )
        yellow_frame.setMinimumHeight(200)
        main_layout.addWidget(yellow_frame)

        
def _refresh_wellness(self):
        """Recharge les données depuis la BDD — appelé au retour sur le dashboard."""
        self.__init__(self.user)
