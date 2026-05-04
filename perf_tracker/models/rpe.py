"""
models/rpe.py
Toutes les requêtes SQL liées au RPE (CRUD).
RPEM = ressenti musculaire / RPEC = ressenti cardio
Échelle : 0 à 10
"""

from database.db import get_connection
from datetime import date as date_type


# ============================================================
# CRÉATION
# ============================================================

def create_rpe(player_id: int, rpem: int, rpec: int,
               date: str = None) -> int:
    """
    Enregistre une saisie RPE pour un joueur.
    - rpem : ressenti musculaire (0-10)
    - rpec : ressenti cardio (0-10)
    - date : format YYYY-MM-DD, aujourd'hui par défaut
    Retourne l'id de la saisie créée.
    """
    if date is None:
        date = date_type.today().isoformat()

    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT OR REPLACE INTO rpe (player_id, date, rpem, rpec)
        VALUES (?, ?, ?, ?)
        """,
        (player_id, date, rpem, rpec)
    )
    rpe_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rpe_id


# ============================================================
# LECTURE
# ============================================================

def get_rpe_by_date(player_id: int, date: str) -> dict | None:
    """
    Retourne la saisie RPE d'un joueur pour une date donnée.
    Retourne None si aucune saisie ce jour.
    """
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, player_id, date, rpem, rpec, created_at
        FROM rpe
        WHERE player_id = ? AND date = ?
        """,
        (player_id, date)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_rpe_today(player_id: int) -> dict | None:
    """Retourne la saisie RPE du jour pour un joueur."""
    today = date_type.today().isoformat()
    return get_rpe_by_date(player_id, today)


def get_rpe_history(player_id: int, limit: int = 30) -> list:
    """
    Retourne l'historique RPE d'un joueur (30 derniers jours par défaut).
    Trié du plus récent au plus ancien.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, player_id, date, rpem, rpec
        FROM rpe
        WHERE player_id = ?
        ORDER BY date DESC
        LIMIT ?
        """,
        (player_id, limit)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_rpe_today() -> list:
    """
    Retourne la saisie RPE de tous les joueurs pour aujourd'hui.
    Inclut les joueurs n'ayant pas encore saisi (rpem/rpec = None).
    """
    today = date_type.today().isoformat()
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero, p.poste,
               r.rpem, r.rpec, r.date
        FROM players p
        LEFT JOIN rpe r ON r.player_id = p.id AND r.date = ?
        ORDER BY p.numero ASC
        """,
        (today,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_rpe_range(date_start: str, date_end: str) -> list:
    """
    Retourne toutes les saisies RPE de l'équipe entre deux dates.
    Utile pour les graphiques et exports.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero,
               r.date, r.rpem, r.rpec
        FROM rpe r
        JOIN players p ON p.id = r.player_id
        WHERE r.date BETWEEN ? AND ?
        ORDER BY r.date DESC, p.numero ASC
        """,
        (date_start, date_end)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ============================================================
# VÉRIFICATION
# ============================================================

def has_rpe_submitted_today(player_id: int) -> bool:
    """Vérifie si un joueur a déjà saisi son RPE aujourd'hui."""
    return get_rpe_today(player_id) is not None


def get_submission_rpe_rate_today() -> dict:
    """
    Retourne le taux de saisie RPE de l'équipe pour aujourd'hui.
    Ex: {'total': 8, 'submitted': 5, 'rate': 62.5}
    """
    today = date_type.today().isoformat()
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    submitted = conn.execute(
        "SELECT COUNT(*) FROM rpe WHERE date = ?", (today,)
    ).fetchone()[0]

    conn.close()
    rate = round((submitted / total * 100), 1) if total > 0 else 0.0
    return {"total": total, "submitted": submitted, "rate": rate}