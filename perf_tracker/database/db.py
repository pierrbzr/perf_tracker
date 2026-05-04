"""
database/db.py
Connexion SQLite + initialisation du schéma + données de test
"""
 
from datetime import date
import sqlite3
import os
import hashlib
import sys
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "perf_tracker.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
 
def get_connection() -> sqlite3.Connection:
    """Retourne une connexion à la base de données avec foreign keys activées."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def resource_path(relative_path):
    """Chemin compatible dev et PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def init_db():
    """Initialise la base de données en exécutant le schéma SQL."""
    conn = get_connection()
    schema_path = resource_path("database/schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"[DB] Base initialisée : {DB_PATH}")


def hash_password(password: str) -> str:
    """Hash simple SHA-256 pourles mots de passe staff."""
    return hashlib.sha256(password.encode()).hexdigest()


def seed_data():
    """Insère des données de test si la base est vide."""
    today = date.today().isoformat()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
         conn.close()
         return
    
    print("[DB] Insertion des données de test...")

    staff = [
        ("LE DUS", "Maxime",  "prepa", "prepa@team.fr",  hash_password("prepa123")),
        ("DA COSTA", "Kévin", "coach", "coach@team.fr",  hash_password("coach123")),
    ]
    cursor.executemany(
        "INSERT INTO users (nom, prenom, role, email, password) VALUES (?,?,?,?,?)",
        staff
    )

    joueurs = [
        ("Test",  "J",  101, "Attaquant",  "2000-03-15", 180, 78.5),
        ("Test",   "J",    102, "Milieu",     "1999-07-22", 175, 73.0),
        ("Test",   "J",  103, "Défenseur",  "2001-01-10", 183, 82.0),
        ("Test",    "J",    104, "Attaquant",  "2002-05-18", 172, 70.0),
        ("Test", "J",   105, "Défenseur",  "2000-09-05", 179, 76.0),
        ("Test", "J",     106, "Milieu",     "2001-12-25", 177, 74.5),
        ("Test",  "J",      107, "Défenseur",  "1999-04-14", 181, 79.0),
        
        ("Perrenoud",  "Phileas",      15, "Attaquant",  "2004-10-01", 179, 73.0),
        ("Delatour",  "Colin",      77, "Attaquant",  "2003-09-25", 173, 70.0),
        ("Petit",  "Louis",      6, "Attaquant",  "1998-01-06", 177, 77.0),
        ("Hostein",  "Arthur",      49, "Attaquant",  "2008-02-10", 188, 80.0),
        ("Shalei",  "Nikita",      24, "Défenseur",  "2001-06-24", 181, 80.0),
        ("Hostein",  "Paulin",      44, "Défenseur",  "2008-02-10", 188, 80.0),
        ("Briantais",  "Eliott",      18, "Défenseur",  "2008-01-09", 185, 76.0),
        ("Le Lem",  "Paul",      19, "Attaquant",  "2006-06-24", 176, 76.0),
        ("Jribi Chauvière",  "Ewen",      70, "Défenseur",  "2007-03-09", 180, 82.0),
        ("Gire",  "Lucas",      90, "Attaquant",  "2007-03-03", 184, 71.0),
        ("Richard",  "Olivier",      1, "Gardien", "1991-07-03", 188, 80),
        ("Ylonen",  "Sebastian",      37, "Gardien",  "1991-07-03", 186, 78.0),
        ("Bazire",  "Pierre",      60, "Gardien", "2005-02-09", 178, 78),
    ]
    cursor.executemany(
        """INSERT INTO players
           (nom, prenom, numero, poste, date_naissance, taille, poids)
           VALUES (?,?,?,?,?,?,?)""",
        joueurs
    )
    
    # ── Wellness de test (aujourd'hui) ──
    wellness_data = [
        (1, today, 4, 3, 4, 2, 3),
        (2, today, 3, 4, 3, 1, 2),
        (3, today, 5, 5, 4, 3, 4),
        (4, today, 2, 2, 3, 4, 5),
        (5, today, 4, 3, 5, 2, 1),
        (6, today, 3, 4, 2, 3, 2),
        (7, today, 5, 4, 4, 1, 3),
        (8, today, 1, 2, 2, 5, 4),
    ]
    cursor.executemany(
        """INSERT OR IGNORE INTO wellness
           (player_id, date, sommeil, humeur, energie, courbatures, stress, score_total)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        [(p, d, s, h, e, c, st, round((s+h+e+c+st)/5, 2))
         for p, d, s, h, e, c, st in wellness_data]
    )
 
    # ── RPE de test (aujourd'hui) ──
    rpe_data = [
        (1, today, 6, 5),
        (2, today, 7, 6),
        (3, today, 5, 4),
        (4, today, 8, 7),
        (5, today, 6, 5),
        (6, today, 4, 3),
        (7, today, 7, 6),
        (8, today, 9, 8),
    ]
    cursor.executemany(
        """INSERT OR IGNORE INTO rpe
           (player_id, date, rpem, rpec)
           VALUES (?, ?, ?, ?)""",
        rpe_data
    )
 
    conn.commit()
    conn.close()
    print("[DB] Données de test insérées.")
 
 
if __name__ == "__main__":
    # Supprimer l'ancienne base si elle existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("[DB] Ancienne base supprimée.")
    init_db()
    seed_data()
    print("[DB] Prêt.")
 