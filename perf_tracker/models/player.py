"""
models/player.py
Toutes les requêtes SQL liées au joueurs
"""

from database.db import get_connection

# ============================================================
# LECTURE
# ============================================================

def get_all_players() -> list:
    """Retourne tous les joueurs triés par numéro de mailot."""
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, nom, prenom, numero, poste, date_naissance, taille, poids, created_at
        FROM players
        ORDER BY numero ASC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_player_by_id(player_id : int) -> dict | None:
    """Retourne un joueur par son id, ou None s'il n,'existe pas."""
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, nom, prenom, numero, poste, date_naissance, taille, poids, created_at
        FROM players
        WHERE id = ?
        """,
        (player_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def search_players(query: str) -> list:
    """Recherche des joueurs par nom ou prénom (insensible à la casse)."""
    conn = get_connection()
    pattern = f"%{query}%"
    rows = conn.execute(
        """
        SELECT id, nom, prenom, numero, poste
        FROM players
        WHERE nom LIKE ? OR prenom LIKE ?
        ORDER BY nom ASC
        """,
        (pattern, pattern)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============================================================
# CRÉATION
# ============================================================
 
def create_player(nom: str, prenom: str, numero: int = None,
                  poste: str = None, date_naissance: str = None,
                  taille: int = None, poids: int = None) -> int:
    """
    Créer un nouveau joueur.
    Retourne l'id du joueur créé.
    """
    conn = get_connection()
    cursor = conn.execute(
         """
        INSERT INTO players (nom, prenom, numero, poste, date_naissance, taille, poids)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (nom, prenom, numero, poste, date_naissance, taille, poids)
    )
    player_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return player_id

# ============================================================
# MISE À JOUR
# ============================================================
 
def update_player(player_id: int, nom: str, prenom: str, numero: int = None,
                  poste: str = None, date_naissance: str = None,
                  taille: int = None, poids: int = None) -> bool:
    """
    Met à jour les informations d'un joueur.
    Retourne True si la mise à jour a réussi.
    """
    conn = get_connection()
    cursor = conn.execute(
        """
        UPDATE players
        SET nom = ?, prenom = ?, numero = ?, poste = ?,
            date_naissance = ?, taille = ?, poids = ?
        WHERE id = ?
        """,
        (nom, prenom, numero, poste, date_naissance, taille, poids, player_id)
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated
 
 
# ============================================================
# SUPPRESSION
# ============================================================
 
def delete_player(player_id: int) -> bool:
    """
    Supprime un joueur par son id.
    Retourne True si la suppression a réussi.
    ⚠️  Supprime aussi ses données wellness et RPE (CASCADE à gérer en app).
    """
    conn = get_connection()
 
    # Supprimer d'abord les données liées
    conn.execute("DELETE FROM wellness WHERE player_id = ?", (player_id,))
    conn.execute("DELETE FROM rpe WHERE player_id = ?", (player_id,))
 
    cursor = conn.execute("DELETE FROM players WHERE id = ?", (player_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
 
 
# ============================================================
# UTILITAIRES
# ============================================================
 
def player_exists(player_id: int) -> bool:
    """Vérifie si un joueur existe."""
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM players WHERE id = ?", (player_id,)
    ).fetchone()
    conn.close()
    return row is not None
 
 
def get_player_count() -> int:
    """Retourne le nombre total de joueurs."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    conn.close()
    return count