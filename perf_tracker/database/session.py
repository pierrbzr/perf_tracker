"""
database/session.py
Gestion de la session persistante (connexion automatique).
Stocke les infos de l'utilisateur connecté dans un fichier JSON local.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION_FILE = os.path.join(BASE_DIR, "session.json")

def save_session(user: dict):
     """
    Sauvegarde la session de l'utilisateur connecté.
    Appelé après un login réussi.
    """
     
     data = {
          "id": user["id"],
          "nom": user["nom"],
          "prenom": user["prenom"],
          "role": user["role"],
          "email": user["email"],
     }
     with open(SESSION_FILE, "w", encoding="utf-8") as f:
          json.dump(data, f, ensure_ascii=False, indent=2)

def load_session() -> dict | None:
    """
    Charge la session sauvegardée
    Retourne le dict utilisateur si une session existe, None sinon
    """  
    
    if not os.path.exists(SESSION_FILE):
         return None
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
         clear_session()
         return None
    
def clear_session():
    """
    Supprime la session sauvegardée
    Appelé lors du logout 
    """

    if os.path.exists(SESSION_FILE):
         os.remove(SESSION_FILE)
        

def has_session() -> bool:
    """
    Verifie si une session existe
    """

    return os.path.exists(SESSION_FILE)