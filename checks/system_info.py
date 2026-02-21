import platform
import sys
import os
import ctypes

def get_os_info():
    """Retourne le nom et la version du système d'exploitation."""
    return f"{platform.system()} {platform.release()}"

def check_python_status():
    """Vérifie si la version de Python est à jour."""
    v = sys.version_info
    status = "OK"
    if v.major == 3 and v.minor < 10:
        status = "⚠️ OBSOLÈTE (Mettre à jour vers 3.10+)"
    return f"Python {v.major}.{v.minor} ({status})"

def is_admin():
    """Vérifie si le script possède les privilèges Administrateur ou Root."""
    try:
        if platform.system() == "Windows":
            # Vérifie les privilèges sous Windows
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # Vérifie l'UID sous Linux (0 = root)
            return os.getuid() == 0
    except AttributeError:
        return False

def get_privilege_status():
    """Retourne une chaîne lisible du statut des privilèges."""
    if is_admin():
        return "🔓 ADMINISTRATEUR / ROOT"
    else:
        return "👤 UTILISATEUR SIMPLE (Certains checks seront limités)"