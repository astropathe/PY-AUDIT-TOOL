import platform
import sys
import subprocess

def get_os_info():
    return f"{platform.system()} {platform.release()}"

def check_python_status():
    v = sys.version_info
    status = "OK"
    if v.major == 3 and v.minor < 10:
        status = "⚠️ OBSOLÈTE (Mettre à jour vers 3.10+)"
    return f"Python {v.major}.{v.minor} ({status})"

def check_firewall():
    """Vérifie le pare-feu (Windows uniquement ici)."""
    try:
        if platform.system() == "Windows":
            cmd = ["netsh", "advfirewall", "show", "allprofiles"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            return "ACTIF" if "ON" in res.stdout.upper() else "❌ DÉSACTIVÉ"
        return "Non supporté (Linux/Mac)"
    except:
        return "Erreur d'analyse"