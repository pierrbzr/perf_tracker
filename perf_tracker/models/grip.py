"""
models/grip.py
Toutes les requêtes SQL liées au Grip (CRUD).
Grip = Valeur du grip 
"""

from database.db import get_connection
from datetime import date as date_type


# ============================================================
# CRÉATION
# ============================================================

def create_grip(player_id: int, grip: float,
               date: str = None) -> int:
    """
    Enregistre une saisie Grip pour un joueur.
    - grip : force du grip (réel)
    - date : format YYYY-MM-DD, aujourd'hui par défaut
    Retourne l'id de la saisie créée.
    """
    if date is None:
        date = date_type.today().isoformat()

    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT OR REPLACE INTO grip (player_id, date, grip)
        VALUES (?, ?, ?)
        """,
        (player_id, date, grip)
    )
    grip_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return grip_id


# ============================================================
# LECTURE
# ============================================================

def get_grip_by_date(player_id: int, date: str) -> dict | None:
    """
    Retourne la saisie du Grip d'un joueur pour une date donnée.
    Retourne None si aucune saisie ce jour.
    """
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, player_id, date, grip, created_at
        FROM grip
        WHERE player_id = ? AND date = ?
        """,
        (player_id, date)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_grip_today(player_id: int) -> dict | None:
    """Retourne la saisie du grip du jour pour un joueur."""
    today = date_type.today().isoformat()
    return get_grip_by_date(player_id, today)


def get_grip_history(player_id: int, limit: int = 30) -> list:
    """
    Retourne l'historique du grip d'un joueur (30 derniers jours par défaut).
    Trié du plus récent au plus ancien.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, player_id, date, grip
        FROM grip
        WHERE player_id = ?
        ORDER BY date DESC
        LIMIT ?
        """,
        (player_id, limit)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_grip_today() -> list:
    """
    Retourne la saisie du grip de tous les joueurs pour aujourd'hui.
    Inclut les joueurs n'ayant pas encore saisi (grip = None).
    """
    today = date_type.today().isoformat()
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero, p.poste,
               g.grip, g.date
        FROM players p
        LEFT JOIN grip g ON g.player_id = p.id AND g.date = ?
        ORDER BY p.numero ASC
        """,
        (today,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_grip_range(date_start: str, date_end: str) -> list:
    """
    Retourne toutes les saisies du grip de l'équipe entre deux dates.
    Utile pour les graphiques et exports.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero,
               g.date, g.grip
        FROM grip g
        JOIN players p ON p.id = g.player_id
        WHERE g.date BETWEEN ? AND ?
        ORDER BY g.date DESC, p.numero ASC
        """,
        (date_start, date_end)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ============================================================
# VÉRIFICATION
# ============================================================

def has_grip_submitted_today(player_id: int) -> bool:
    """Vérifie si un joueur a déjà saisi son grip aujourd'hui."""
    return get_grip_today(player_id) is not None


def get_submission_grip_rate_today() -> dict:
    """
    Retourne le taux de saisie du grip de l'équipe pour aujourd'hui.
    Ex: {'total': 8, 'submitted': 5, 'rate': 62.5}
    """
    today = date_type.today().isoformat()
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    submitted = conn.execute(
        "SELECT COUNT(*) FROM grip WHERE date = ?", (today,)
    ).fetchone()[0]

    conn.close()
    rate = round((submitted / total * 100), 1) if total > 0 else 0.0
    return {"total": total, "submitted": submitted, "rate": rate}