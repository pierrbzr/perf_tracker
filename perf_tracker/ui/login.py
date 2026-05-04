"""
ui/login.py
Écran de connexion pour le staff (prépa / coach).
Login par email + mot de passe.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from assets.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_BG_CARD, COLOR_BG_INPUT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_BORDER, COLOR_BORDER_ACTIVE, FONT_FAMILY,
    FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    BORDER_RADIUS, PADDING_CARD
)
from models.user import login


class LoginScreen(QWidget):
    """
    Écran de login staff.
    Émet login_success(user_dict) quand la connexion réussit.
    """
    login_success = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    # ── Construction UI ──────────────────────────────────────

    def _build_ui(self):
        # Layout principal centré
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)
        root.setContentsMargins(0, 0, 0, 0)

        # Carte centrale
        card = QFrame()
        card.setFixedWidth(420)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(PADDING_CARD * 2, PADDING_CARD * 2,
                                       PADDING_CARD * 2, PADDING_CARD * 2)
        card_layout.setSpacing(20)

        # ── En-tête ──
        header = QVBoxLayout()
        header.setSpacing(6)

        # Logo texte club
        club_label = QLabel("JOKERS")
        club_label.setAlignment(Qt.AlignCenter)
        club_label.setStyleSheet(f"""
            color: {COLOR_GREEN};
            font-size: 28px;
            font-weight: 800;
            font-family: "{FONT_FAMILY}";
            letter-spacing: 4px;
            border: none;
            background: transparent;
        """)

        subtitle_label = QLabel("Cergy-Pontoise")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            letter-spacing: 2px;
            border: none;
            background: transparent;
        """)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"color: {COLOR_BORDER}; margin: 8px 0;")

        title_label = QLabel("Connexion Staff")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            color: {COLOR_TEXT_PRIMARY};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: 700;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

        header.addWidget(club_label)
        header.addWidget(subtitle_label)
        header.addWidget(separator)
        header.addWidget(title_label)
        card_layout.addLayout(header)

        # ── Formulaire ──
        form = QVBoxLayout()
        form.setSpacing(12)

        # Email
        email_label = QLabel("Adresse email")
        email_label.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemple@jokers.fr")
        self.email_input.setFixedHeight(44)
        self.email_input.setStyleSheet(self._input_style())
        self.email_input.returnPressed.connect(self._on_login)

        # Mot de passe
        password_label = QLabel("Mot de passe")
        password_label.setStyleSheet(f"""
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: 600;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(44)
        self.password_input.setStyleSheet(self._input_style())
        self.password_input.returnPressed.connect(self._on_login)

        form.addWidget(email_label)
        form.addWidget(self.email_input)
        form.addWidget(password_label)
        form.addWidget(self.password_input)
        card_layout.addLayout(form)

        # ── Message d'erreur ──
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet(f"""
            color: {COLOR_RED};
            font-size: {FONT_SIZE_SMALL}px;
            font-family: "{FONT_FAMILY}";
            padding: 4px;
        """)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)

        # ── Bouton connexion ──
        self.login_btn = QPushButton("Se connecter")
        self.login_btn.setFixedHeight(46)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet(f"""
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
            QPushButton:hover {{
                background-color: #00C962;
            }}
            QPushButton:pressed {{
                background-color: #007A3D;
            }}
        """)
        self.login_btn.clicked.connect(self._on_login)
        card_layout.addWidget(self.login_btn)

        # ── Footer ──
        footer = QLabel("Accès réservé au staff autorisé")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(f"""
            color: {COLOR_TEXT_MUTED};
            font-size: {FONT_SIZE_SMALL - 1}px;
            font-family: "{FONT_FAMILY}";
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(footer)

        root.addWidget(card)

    # ── Logique ─────────────────────────────────────────────

    def _on_login(self):
        """Vérifie les identifiants et émet login_success si valide."""
        email = self.email_input.text().strip()
        password = self.password_input.text()

        # Validation basique
        if not email or not password:
            self._show_error("Veuillez remplir tous les champs.")
            return

        # Vérification en base
        user = login(email, password)

        if user:
            self._clear_error()
            self.login_success.emit(user)
        else:
            self._show_error("Email ou mot de passe incorrect.")
            self.password_input.clear()
            self.password_input.setFocus()

    def _show_error(self, message: str):
        self.error_label.setText(f"⚠  {message}")
        self.error_label.show()

    def _clear_error(self):
        self.error_label.hide()
        self.error_label.setText("")

    # ── Style helpers ────────────────────────────────────────

    def _input_style(self) -> str:
        return f"""
            QLineEdit {{
                background-color: {COLOR_BG_INPUT};
                color: {COLOR_TEXT_PRIMARY};
                border: 1px solid {COLOR_BORDER};
                border-radius: {BORDER_RADIUS}px;
                padding: 8px 14px;
                font-size: {FONT_SIZE_BODY}px;
                font-family: "{FONT_FAMILY}";
            }}
            QLineEdit:focus {{
                border: 1px solid {COLOR_BORDER_ACTIVE};
            }}
        """