import subprocess
import platform
import os

def check_firewall():
    """Vérifie l'état du pare-feu selon l'OS."""
    system = platform.system()
    try:
        if system == "Windows":
            cmd = ["netsh", "advfirewall", "show", "allprofiles"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return "✅ ACTIF" if "ON" in res.stdout.upper() else "❌ DÉSACTIVÉ"
        
        elif system == "Linux":
            res = subprocess.run(["ufw", "status"], capture_output=True, text=True)
            return "✅ ACTIF" if "active" in res.stdout.lower() else "❌ DÉSACTIVÉ"
            
        return "❓ OS non supporté"
    except Exception:
        return "⚠️ Erreur (Droits insuffisants ?)"

def check_antivirus():
    """Vérifie si la protection en temps réel est active (Windows uniquement)."""
    if platform.system() != "Windows":
        return "ℹ️ Non applicable sur cet OS"
    
    try:
        # Commande PowerShell pour interroger Windows Defender
        cmd = "powershell Get-MpComputerStatus | select -ExpandProperty RealTimeProtectionEnabled"
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if "True" in res.stdout:
            return "✅ ACTIF"
        elif "False" in res.stdout:
            return "❌ DÉSACTIVÉ"
        else:
            return "❓ Inconnu"
    except Exception:
        return "⚠️ Erreur de détection"

def check_ssh_config():
    """Analyse la configuration SSH pour détecter des failles de durcissement."""
    if platform.system() == "Windows":
        return "ℹ️ Check SSH ignoré sur Windows"
        
    ssh_path = "/etc/ssh/sshd_config"
    if not os.path.exists(ssh_path):
        return "✅ Service SSH non présent"

    issues = []
    try:
        with open(ssh_path, "r") as f:
            content = f.read()
            if "PermitRootLogin yes" in content:
                issues.append("Root Login autorisé")
            if "PasswordAuthentication yes" in content:
                issues.append("Auth par mot de passe (préférer les clés)")
        
        return "⚠️ FAIBLE (" + ", ".join(issues) + ")" if issues else "✅ SÉCURISÉ"
    except PermissionError:
        return "🔒 Droits insuffisants pour lire la config SSH"