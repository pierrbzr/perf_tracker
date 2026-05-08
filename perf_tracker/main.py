"""
main.py
Point d'entrée de l'application perf_tracker.
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow
from assets.theme import STYLESHEET, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG_DARK
from database.db import init_db, seed_data
from database.session import save_session, load_session, clear_session

from ui.login import LoginScreen
from ui.dashboard.prepa_dashboard import PrepaDashboard
from ui.dashboard.coach_dashboard import CoachDashboard

from ui.wellness.wellness_player_list import WellnessPlayerList
from ui.rpe.rpe_player_list import RPEPlayerList
from ui.grip.grip_player_list import GripPlayerList
from ui.poids.poids_player_list import PoidsPlayerList
from ui.players.player_list import PlayerList
from ui.graphs.graphs import Graphs

from ui.wellness.wellness_form import WellnessForm
from ui.rpe.rpe_form import RPEForm
from ui.grip.grip_form import GripForm
from ui.poids.poids_form import PoidsForm
from ui.players.player_form import PlayerForm


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perf Tracker — Jokers de Cergy-Pontoise")
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(f"background-color: {COLOR_BG_DARK};")
        self._current_user = None

        #Tentative de connexion automatique via session sauvegardée
        session = load_session()
        if session:
            self._route_to_dashboard(session)
            self._current_user = session
        else:
            self._show_login()

    # ── Routing ─────────────────────────────────────────────

    def _show_login(self):
        """Affiche l'écran de login."""
        screen = LoginScreen()
        screen.login_success.connect(self._on_login_success)
        self.setCentralWidget(screen)
        self.setWindowTitle("Perf Tracker — Connexion")

    def _on_login_success(self, user: dict):
        """Sauvegarde la session et redirige vers le bon dashboard"""
        self._current_user = user
        save_session(user)
        self._route_to_dashboard(user)

    def _on_logout(self):
        """Déconnexion → retour à l'écran de login."""
        clear_session()
        self._current_user = None
        self._show_login()

    # ── Routing Dashboard ─────────────────────────────────────────────

    def _route_to_dashboard(self, user: dict):
        role = user.get("role")
        if role =="prepa":
            self._show_prepa_dashboard(user)
        elif role == "coach":
            self._show_coach_dashboard(user)
        else:
            clear_session()
            self._show_login()

    def _show_prepa_dashboard(self, user: dict = None):
        """Affiche le dashboard préparateur physique."""
        user = user or self._current_user
        self._prepa_screen = PrepaDashboard(user)
        self._prepa_screen.logout_requested.connect(self._on_logout)
        self._prepa_screen.go_to_wellness.connect(self._show_wellness_player_list)
        self._prepa_screen.go_to_rpe.connect(self._show_rpe_player_list)
        self._prepa_screen.go_to_grip.connect(self._show_grip_player_list)
        self._prepa_screen.go_to_poids.connect(self._show_poids_player_list)
        self._prepa_screen.go_to_players.connect(self._show_player_list)
        self._prepa_screen.go_to_graphs.connect(self._show_graphs_list)
        self.setCentralWidget(self._prepa_screen)
        
        self.setWindowTitle(
            f"Perf Tracker — Prépa | {user['prenom']} {user['nom']}"
        )

    def _show_coach_dashboard(self, user: dict):
        """Affiche le dashboard coach."""
        screen = CoachDashboard(user)
        screen.logout_requested.connect(self._on_logout)
        self.setCentralWidget(screen)
        self.setWindowTitle(
            f"Perf Tracker — Coach | {user['prenom']} {user['nom']}"
        )

# ── Routing Wellness ─────────────────────────────────────

    def _show_wellness_player_list(self):
        screen = WellnessPlayerList()
        screen.back_requested.connect(lambda: self._on_back_to_dashboard()) 
        screen.wellness_selected.connect(self._show_wellness_form)
        self.setCentralWidget(screen)
        self.setWindowTitle("Perf Tracker — Wellness")
        
    def _show_wellness_form(self, player: dict):
        screen = WellnessForm(player)
        screen.back_requested.connect(self._show_wellness_player_list)
        screen.wellness_saved.connect(self._show_wellness_player_list)
        self.setCentralWidget(screen)
        self.setWindowTitle(
            f"Perf Tracker — Wellness | {player['prenom']} {player['nom']}"
        )

# ── Routing RPE ─────────────────────────────────────

    def _show_rpe_player_list(self):
        screen = RPEPlayerList()
        screen.back_requested.connect(lambda: self._on_back_to_dashboard()) 
        screen.rpe_selected.connect(self._show_rpe_form)
        self.setCentralWidget(screen)
        self.setWindowTitle("Perf Tracker — RPE")
        
    def _show_rpe_form(self, player: dict):
        screen = RPEForm(player)
        screen.back_requested.connect(self._show_rpe_player_list)
        screen.rpe_saved.connect(self._show_rpe_player_list)
        self.setCentralWidget(screen)
        self.setWindowTitle(
            f"Perf Tracker — RPE | {player['prenom']} {player['nom']}"
        )

# ── Routing Grip ─────────────────────────────────────

    def _show_grip_player_list(self):
        screen = GripPlayerList()
        screen.back_requested.connect(lambda: self._on_back_to_dashboard()) 
        screen.grip_selected.connect(self._show_grip_form)
        self.setCentralWidget(screen)
        self.setWindowTitle("Perf Tracker — Grip")
        
    def _show_grip_form(self, player: dict):
        screen = GripForm(player)
        screen.back_requested.connect(self._show_grip_player_list)
        screen.grip_saved.connect(self._show_grip_player_list)
        self.setCentralWidget(screen)
        self.setWindowTitle(
            f"Perf Tracker — Grip | {player['prenom']} {player['nom']}"
        )

# ── Routing Poids ───────────────────────────────────── 

    def _show_poids_player_list(self):
        screen = PoidsPlayerList()
        screen.back_requested.connect(lambda: self._on_back_to_dashboard()) 
        screen.poids_selected.connect(self._show_poids_form)
        self.setCentralWidget(screen)
        self.setWindowTitle("Perf Tracker — Poids")
    
    def _show_poids_form(self, player: dict):
        screen = PoidsForm(player)
        screen.back_requested.connect(self._show_poids_player_list)
        screen.poids_saved.connect(self._show_poids_player_list)
        self.setCentralWidget(screen)
        self.setWindowTitle(
            f"Perf Tracker — Poids | {player['prenom']} {player['nom']}"
        )
        
# ── Routing Liste de joueurs ─────────────────────────────────────

    def _show_player_list(self):
        screen = PlayerList()
        screen.back_requested.connect(lambda: self._on_back_to_dashboard()) 
        screen.player_selected.connect(self._show_players)
        self.setCentralWidget(screen)
        self.setWindowTitle("Perf Tracker — Liste des Joueurs")
        
    def _show_players(self, player: dict):
        screen = PlayerForm(player)
        screen.back_requested.connect(self._show_player_list)
        self.setCentralWidget(screen)
        self.setWindowTitle(
            f"Perf Tracker — Grip | {player['prenom']} {player['nom']}"
        )
        
# ── Routing Graphiques Dashboard ─────────────────────────────────────

    def _show_graphs_list(self):
        screen = Graphs()
        screen.back_requested.connect(lambda: self._on_back_to_dashboard()) 
        self.setCentralWidget(screen)
        self.setWindowTitle("Perf Tracker — Graphiques")
        

# ── Routing Dashboard ─────────────────────────────────────

    def _on_back_to_dashboard(self):
        """Retour au dashboard → recrée avec données fraîches."""
        self._show_prepa_dashboard()
 
 
if __name__ == "__main__":
    init_db()
    seed_data()
 
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
 
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
 