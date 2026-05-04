"""
models/wellness.py
Toutes les requêtes SQL liées au wellness (CRUD).
"""

from database.db import get_connection
from datetime import date as date_type


# ============================================================
# CRÉATION
# ============================================================

def create_wellness(player_id: int, sommeil: int, humeur: int,
                    energie: int, courbatures: int, stress: int,
                    date: str = None) -> int:
    """
    Enregistre une saisie wellness pour un joueur.
    - date : format YYYY-MM-DD, aujourd'hui par défaut
    - score_total : moyenne des 5 indicateurs (calculé auto)
    Retourne l'id de la saisie créée.
    """
    if date is None:
        date = date_type.today().isoformat()

    score_total = round((sommeil + humeur + energie + courbatures + stress) / 5, 2)

    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT OR REPLACE INTO wellness (player_id, date, sommeil, humeur, energie, courbatures, stress, score_total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (player_id, date, sommeil, humeur, energie, courbatures, stress, score_total)
    )
    wellness_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return wellness_id


# ============================================================
# LECTURE
# ============================================================

def get_wellness_by_date(player_id: int, date: str) -> dict | None:
    """
    Retourne la saisie wellness d'un joueur pour une date donnée.
    Retourne None si aucune saisie ce jour.
    """
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, player_id, date, sommeil, humeur, energie, courbatures, stress, score_total, created_at
        FROM wellness
        WHERE player_id = ? AND date = ?
        """,
        (player_id, date)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_wellness_today(player_id: int) -> dict | None:
    """Retourne la saisie wellness du jour pour un joueur."""
    today = date_type.today().isoformat()
    return get_wellness_by_date(player_id, today)


def get_wellness_history(player_id: int, limit: int = 10) -> list:
    """
    Retourne l'historique wellness d'un joueur (10 derniers jours par défaut).
    Trié du plus récent au plus ancien.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, player_id, date, sommeil, humeur, energie, courbatures, stress, score_total
        FROM wellness
        WHERE player_id = ?
        ORDER BY date DESC
        LIMIT ?
        """,
        (player_id, limit)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_wellness_today() -> list:
    """
    Retourne la saisie wellness de tous les joueurs pour aujourd'hui.
    Inclut les joueurs n'ayant pas encore saisi (score_total = None).
    """
    today = date_type.today().isoformat()
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero, p.poste,
               w.sommeil, w.humeur, w.energie, w.courbatures, w.stress,
               w.score_total, w.date
        FROM players p
        LEFT JOIN wellness w ON w.player_id = p.id AND w.date = ?
        ORDER BY p.numero ASC
        """,
        (today,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_wellness_range(date_start: str, date_end: str) -> list:
    """
    Retourne toutes les saisies wellness de l'équipe entre deux dates.
    Utile pour les graphiques et exports.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero,
               w.date, w.sommeil, w.humeur, w.energie,
               w.courbatures, w.stress, w.score_total
        FROM wellness w
        JOIN players p ON p.id = w.player_id
        WHERE w.date BETWEEN ? AND ?
        ORDER BY w.date DESC, p.numero ASC
        """,
        (date_start, date_end)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ============================================================
# VÉRIFICATION
# ============================================================

def has_submitted_today(player_id: int) -> bool:
    """Vérifie si un joueur a déjà saisi son wellness aujourd'hui."""
    return get_wellness_today(player_id) is not None


def get_submission_wellness_rate_today() -> dict:
    """
    Retourne le taux de saisie wellness de l'équipe pour aujourd'hui.
    Ex: {'total': 8, 'submitted': 5, 'rate': 62.5}
    """
    today = date_type.today().isoformat()
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    submitted = conn.execute(
        "SELECT COUNT(*) FROM wellness WHERE date = ?", (today,)
    ).fetchone()[0]

    conn.close()
    rate = round((submitted / total * 100), 1) if total > 0 else 0.0
    return {"total": total, "submitted": submitted, "rate": rate}