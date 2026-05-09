"""
assets/theme.py
Thème visuel de l'application - Jokers de Cergy-Pontoise
Couleurs : Vert (#1DB954 → adapté #00A651) + Rouge (#C8102E)
Fond sombre
"""

# ============================================================
# PALETTE DE COULEURS
# ============================================================

# Couleurs principales club
COLOR_GREEN         = "#00A651"   # Vert Jokers (accent principal)
COLOR_GREEN_DARK    = "#007A3D"   # Vert foncé (hover, bordures)
COLOR_GREEN_LIGHT   = "#00C962"   # Vert clair (highlights)

COLOR_RED           = "#C8102E"   # Rouge Jokers (accent secondaire / alertes)
COLOR_RED_DARK      = "#9B0D23"   # Rouge foncé (hover)
COLOR_RED_LIGHT     = "#E8314F"   # Rouge clair (warnings)

# Fonds sombres
COLOR_BG_DARK       = "#0D0D0D"   # Fond principal (quasi noir)
COLOR_BG_CARD       = "#1A1A1A"   # Fond carte / panel
COLOR_BG_SIDEBAR    = "#111111"   # Fond sidebar
COLOR_BG_INPUT      = "#242424"   # Fond champs input
COLOR_BG_HOVER      = "#2A2A2A"   # Hover sur éléments

# Textes
COLOR_TEXT_PRIMARY  = "#F0F0F0"   # Texte principal (blanc cassé)
COLOR_TEXT_SECONDARY= "#A0A0A0"   # Texte secondaire (gris)
COLOR_TEXT_MUTED    = "#606060"   # Texte désactivé
COLOR_TEXT_ON_GREEN = "#FFFFFF"   # Texte sur fond vert
COLOR_TEXT_ON_RED   = "#FFFFFF"   # Texte sur fond rouge

# Bordures
COLOR_BORDER        = "#2E2E2E"   # Bordure standard
COLOR_BORDER_ACTIVE = "#00A651"   # Bordure active (vert)

# États wellness / RPE (code couleur)
COLOR_GOOD          = "#00A651"   # Bon état (vert)
COLOR_WARNING       = "#F5A623"   # Attention (orange)
COLOR_DANGER        = "#C8102E"   # Danger (rouge)
COLOR_NEUTRAL       = "#A0A0A0"   # Neutre (gris)


# ============================================================
# TYPOGRAPHIE
# ============================================================

FONT_FAMILY         = "Segoe UI"  # Natif Windows, propre et lisible
FONT_SIZE_TITLE     = 22
FONT_SIZE_SUBTITLE  = 16
FONT_SIZE_BODY      = 13
FONT_SIZE_SMALL     = 11
FONT_SIZE_LABEL     = 12


# ============================================================
# DIMENSIONS
# ============================================================

WINDOW_WIDTH        = 1080
WINDOW_HEIGHT       = 980
SIDEBAR_WIDTH       = 220
BORDER_RADIUS       = 8
PADDING_CARD        = 16
PADDING_SECTION     = 16
SPACING             = 12


# ============================================================
# STYLESHEET GLOBAL PyQt5
# ============================================================

STYLESHEET = f"""
/* ── Fenêtre principale ── */
QMainWindow, QWidget {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_PRIMARY};
    font-family: "{FONT_FAMILY}";
    font-size: {FONT_SIZE_BODY}px;
}}

/* ── Labels ── */
QLabel {{
    color: {COLOR_TEXT_PRIMARY};
    background: transparent;
    border: none;
}}

QWidget QLabel {{
    border: none;
    background: transparent;
}}

QLabel#title {{
    font-size: {FONT_SIZE_TITLE}px;
    font-weight: bold;
    color: {COLOR_GREEN};
}}

QLabel#subtitle {{
    font-size: {FONT_SIZE_SUBTITLE}px;
    font-weight: 600;
    color: {COLOR_TEXT_PRIMARY};
}}

QLabel#muted {{
    color: {COLOR_TEXT_MUTED};
    font-size: {FONT_SIZE_SMALL}px;
}}

/* ── Bouton principal (vert) ── */
QPushButton {{
    background-color: {COLOR_GREEN};
    color: {COLOR_TEXT_ON_GREEN};
    border: none;
    border-radius: {BORDER_RADIUS}px;
    padding: 10px 24px;
    font-size: {FONT_SIZE_BODY}px;
    font-weight: 600;
    font-family: "{FONT_FAMILY}";
}}

QPushButton:hover {{
    background-color: {COLOR_GREEN_LIGHT};
}}

QPushButton:pressed {{
    background-color: {COLOR_GREEN_DARK};
}}

QPushButton:disabled {{
    background-color: {COLOR_BG_INPUT};
    color: {COLOR_TEXT_MUTED};
}}

/* ── Bouton danger (rouge) ── */
QPushButton#danger {{
    background-color: {COLOR_RED};
    color: {COLOR_TEXT_ON_RED};
}}

QPushButton#danger:hover {{
    background-color: {COLOR_RED_LIGHT};
}}

QPushButton#danger:pressed {{
    background-color: {COLOR_RED_DARK};
}}

/* ── Bouton secondaire (outline) ── */
QPushButton#secondary {{
    background-color: transparent;
    color: {COLOR_GREEN};
    border: 2px solid {COLOR_GREEN};
}}

QPushButton#secondary:hover {{
    background-color: {COLOR_GREEN};
    color: {COLOR_TEXT_ON_GREEN};
}}

/* ── Champs de saisie ── */
QLineEdit, QTextEdit, QSpinBox, QComboBox {{
    background-color: {COLOR_BG_INPUT};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    border-radius: {BORDER_RADIUS}px;
    padding: 8px 12px;
    font-size: {FONT_SIZE_BODY}px;
    font-family: "{FONT_FAMILY}";
}}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {COLOR_BORDER_ACTIVE};
    outline: none;
}}

QLineEdit::placeholder {{
    color: {COLOR_TEXT_MUTED};
}}

/* ── ComboBox ── */
QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    selection-background-color: {COLOR_GREEN};
    selection-color: {COLOR_TEXT_ON_GREEN};
}}

/* ── Tableaux ── */
QTableWidget {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    border-radius: {BORDER_RADIUS}px;
    gridline-color: {COLOR_BORDER};
    font-family: "{FONT_FAMILY}";
    font-size: {FONT_SIZE_BODY}px;
}}

QTableWidget::item {{
    padding: 8px 12px;
}}

QTableWidget::item:selected {{
    background-color: {COLOR_GREEN_DARK};
    color: {COLOR_TEXT_ON_GREEN};
}}

QHeaderView::section {{
    background-color: {COLOR_BG_SIDEBAR};
    color: {COLOR_TEXT_SECONDARY};
    border: none;
    border-bottom: 1px solid {COLOR_BORDER};
    padding: 10px 12px;
    font-weight: 600;
    font-size: {FONT_SIZE_SMALL}px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* ── Scrollbar ── */
QScrollBar:vertical {{
    background: {COLOR_BG_DARK};
    width: 6px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical {{
    background: {COLOR_BORDER};
    border-radius: 3px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLOR_GREEN};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* ── Slider (pour wellness 0-5 et RPE 0-10) ── */
QSlider::groove:horizontal {{
    height: 6px;
    background: {COLOR_BORDER};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    width: 18px;
    height: 18px;
    background: {COLOR_GREEN};
    border-radius: 9px;
    margin: -6px 0;
}}

QSlider::sub-page:horizontal {{
    background: {COLOR_GREEN};
    border-radius: 3px;
}}

/* ── Séparateur ── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    color: {COLOR_BORDER};
}}

/* ── Message box ── */
QMessageBox {{
    background-color: {COLOR_BG_CARD};
    color: {COLOR_TEXT_PRIMARY};
}}
"""


# ============================================================
# HELPERS — couleur selon score wellness
# ============================================================

def wellness_color(score: float) -> str:
    """
    Retourne une couleur hex selon le score wellness (0-5).
    ≥ 3.5 → vert / 2.0-3.4 → orange / < 2.0 → rouge
    """
    if score >= 3.5:
        return COLOR_GOOD
    elif score >= 2.0:
        return COLOR_WARNING
    else:
        return COLOR_DANGER


def rpe_color(value: int) -> str:
    """
    Retourne une couleur hex selon la valeur RPE (0-10).
    ≤ 4 → vert / 5-7 → orange / ≥ 8 → rouge
    """
    if value <= 4:
        return COLOR_GOOD
    elif value <= 7:
        return COLOR_WARNING
    else:
        return COLOR_DANGER