# Firewall, SSH, etc.
import subprocess
import platform
import os

def check_firewall():
    """Vérifie si le pare-feu est actif selon l'OS."""
    try:
        system = platform.system()
        if system == "Windows":
            cmd = ["netsh", "advfirewall", "show", "allprofiles"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            return "✅ ACTIF" if "ON" in res.stdout.upper() else "❌ DÉSACTIVÉ"
        
        elif system == "Linux":
            # Nécessite souvent les droits sudo, on gère l'erreur proprement
            res = subprocess.run(["ufw", "status"], capture_output=True, text=True)
            return "✅ ACTIF" if "active" in res.stdout.lower() else "❌ DÉSACTIVÉ"
            
        return "❓ OS non supporté pour le pare-feu"
    except Exception:
        return "⚠️ Erreur lors de l'accès au Pare-feu"

def check_ssh_config():
    """Vérifie si la config SSH est trop permissive (Linux uniquement)."""
    ssh_path = "/etc/ssh/sshd_config"
    issues = []
    
    if not os.path.exists(ssh_path):
        return "ℹ️ SSH non installé ou config introuvable"

    try:
        with open(ssh_path, "r") as f:
            content = f.read()
            if "PermitRootLogin yes" in content:
                issues.append("Root Login autorisé")
            if "PasswordAuthentication yes" in content:
                issues.append("Auth par mot de passe simple")
        
        return "⚠️ Faible (" + ", ".join(issues) + ")" if issues else "✅ Sécurisé"
    except PermissionError:
        return "🔒 Droits insuffisants pour lire SSH"