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

def create_statistiques(player_id: int, bench: float, squat: float, deadlift: float, 
                clean: float, broadjump: float, cmj: float, pullup: float, 
                sprint5m: str, sprint10m: str, sprint20m: str, date: str = None) -> int:
    """
    Enregistre une saisie des statistiques pour un joueur.
    Retourne l'id de la saisie créée.
    """
    if date is None:
        date = date_type.today().isoformat()

    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT OR REPLACE INTO statistiques (player_id, date, bench, squat, deadlift, clean, broadjump, cmj, pullup, sprint5m, sprint10m, sprint20m)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (player_id, date, bench, squat, deadlift, clean, broadjump, cmj, pullup, sprint5m, sprint10m, sprint20m)
    )
    statistiques_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return statistiques_id


# ============================================================
# LECTURE
# ============================================================

def get_player_statistiques(player_id: int) -> dict | None:
    """
    Retourne les statistiques d'un joueur pour une date donnée.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM statistiques
        WHERE player_id = ?
        ORDER BY date ASC
    """, (player_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_player_recent_statistiques(player_id: int) -> dict | None:
    """
    Retourne les statistiques d'un joueur pour une date donnée.
    """
    conn = get_connection()
    row = conn.execute("""
        SELECT *
        FROM statistiques
        WHERE player_id = ?
        ORDER BY date DESC LIMIT 1;
    """,
    (player_id,)
    ).fetchone()
    conn.close()
    
    return dict(row) if row else None

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


# ============================================================
# VÉRIFICATION
# ============================================================

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