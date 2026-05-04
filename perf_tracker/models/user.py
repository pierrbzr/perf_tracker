"""
models/user.py
Toutes les requêtes SQL liées aux utilisateurs staff (CRUD + authentification).
Rôles : 'prepa' / 'coach'
"""

from database.db import get_connection, hash_password


# ============================================================
# AUTHENTIFICATION
# ============================================================

def login(email: str, password: str) -> dict | None:
    """
    Vérifie les identifiants d'un utilisateur staff.
    Retourne le profil utilisateur si valide, None sinon.
    """
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, nom, prenom, role, email
        FROM users
        WHERE email = ? AND password = ?
        """,
        (email, hash_password(password))
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ============================================================
# LECTURE
# ============================================================

def get_all_users() -> list:
    """Retourne tous les comptes staff."""
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, nom, prenom, role, email, created_at
        FROM users
        ORDER BY role ASC, nom ASC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user_by_id(user_id: int) -> dict | None:
    """Retourne un utilisateur par son id."""
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, nom, prenom, role, email, created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_email(email: str) -> dict | None:
    """Retourne un utilisateur par son email."""
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, nom, prenom, role, email, created_at
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ============================================================
# CRÉATION
# ============================================================

def create_user(nom: str, prenom: str, role: str,
                email: str, password: str) -> int | None:
    """
    Crée un nouveau compte staff.
    - role : 'prepa' ou 'coach'
    Retourne l'id créé, ou None si l'email existe déjà.
    """
    if get_user_by_email(email):
        return None

    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO users (nom, prenom, role, email, password)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nom, prenom, role, email, hash_password(password))
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


# ============================================================
# MISE À JOUR
# ============================================================

def update_user(user_id: int, nom: str, prenom: str,
                role: str, email: str) -> bool:
    """
    Met à jour les informations d'un utilisateur (sans le mot de passe).
    Retourne True si la mise à jour a réussi.
    """
    conn = get_connection()
    cursor = conn.execute(
        """
        UPDATE users
        SET nom = ?, prenom = ?, role = ?, email = ?
        WHERE id = ?
        """,
        (nom, prenom, role, email, user_id)
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def update_password(user_id: int, old_password: str, new_password: str) -> bool:
    """
    Met à jour le mot de passe d'un utilisateur après vérification de l'ancien.
    Retourne True si la mise à jour a réussi.
    """
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM users WHERE id = ? AND password = ?",
        (user_id, hash_password(old_password))
    ).fetchone()

    if not row:
        conn.close()
        return False

    conn.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (hash_password(new_password), user_id)
    )
    conn.commit()
    conn.close()
    return True


# ============================================================
# SUPPRESSION
# ============================================================

def delete_user(user_id: int) -> bool:
    """
    Supprime un compte staff.
    Retourne True si la suppression a réussi.
    """
    conn = get_connection()
    cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


# ============================================================
# UTILITAIRES
# ============================================================

def email_exists(email: str) -> bool:
    """Vérifie si un email est déjà utilisé."""
    return get_user_by_email(email) is not None


def get_user_count() -> int:
    """Retourne le nombre total de comptes staff."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return count