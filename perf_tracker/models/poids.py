"""
models/poids.py
Toutes les requêtes SQL liées au poids (CRUD).
poids = Poids du joueur 
"""

from database.db import get_connection
from datetime import date as date_type


# ============================================================
# CRÉATION
# ============================================================

def create_poids(player_id: int, poids: float,
               date: str = None) -> int:
    """
    Enregistre une saisie Poids pour un joueur.
    - poids : poids du joueur (réel)
    - date : format YYYY-MM-DD, aujourd'hui par défaut
    Retourne l'id de la saisie créée.
    """
    if date is None:
        date = date_type.today().isoformat()

    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT OR REPLACE INTO poids (player_id, date, poids)
        VALUES (?, ?, ?)
        """,
        (player_id, date, poids)
    )
    poids_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return poids_id


# ============================================================
# LECTURE
# ============================================================

def get_poids_by_date(player_id: int, date: str) -> dict | None:
    """
    Retourne la saisie du poids d'un joueur pour une date donnée.
    Retourne None si aucune saisie ce jour.
    """
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, player_id, date, poids, created_at
        FROM poids
        WHERE player_id = ? AND date = ?
        """,
        (player_id, date)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_poids_today(player_id: int) -> dict | None:
    """Retourne la saisie du poids du jour pour un joueur."""
    today = date_type.today().isoformat()
    return get_poids_by_date(player_id, today)


def get_poids_history(player_id: int, limit: int = 30) -> list:
    """
    Retourne l'historique du poids d'un joueur (30 derniers jours par défaut).
    Trié du plus récent au plus ancien.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, player_id, date, poids
        FROM poids
        WHERE player_id = ?
        ORDER BY date DESC
        LIMIT ?
        """,
        (player_id, limit)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_poids_today() -> list:
    """
    Retourne la saisie du poids de tous les joueurs pour aujourd'hui.
    Inclut les joueurs n'ayant pas encore saisi (poids = None).
    """
    today = date_type.today().isoformat()
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero, p.poste,
               pds.poids, pds.date
        FROM players p
        LEFT JOIN poids pds ON pds.player_id = p.id AND pds.date = ?
        ORDER BY p.numero ASC
        """,
        (today,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_poids_range(date_start: str, date_end: str) -> list:
    """
    Retourne toutes les saisies du poids de l'équipe entre deux dates.
    Utile pour les graphiques et exports.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT p.id AS player_id, p.nom, p.prenom, p.numero,
               pds.date, pds.poids
        FROM poids pds
        JOIN players p ON p.id = pds.player_id
        WHERE pds.date BETWEEN ? AND ?
        ORDER BY pds.date DESC, p.numero ASC
        """,
        (date_start, date_end)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ============================================================
# VÉRIFICATION
# ============================================================

def has_poids_submitted_today(player_id: int) -> bool:
    """Vérifie si un joueur a déjà saisi son poids aujourd'hui."""
    return get_poids_today(player_id) is not None


def get_submission_poids_rate_today() -> dict:
    """
    Retourne le taux de saisie du poids de l'équipe pour aujourd'hui.
    Ex: {'total': 8, 'submitted': 5, 'rate': 62.5}
    """
    today = date_type.today().isoformat()
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    submitted = conn.execute(
        "SELECT COUNT(*) FROM poids WHERE date = ?", (today,)
    ).fetchone()[0]

    conn.close()
    rate = round((submitted / total * 100), 1) if total > 0 else 0.0
    return {"total": total, "submitted": submitted, "rate": rate}