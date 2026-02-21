from checks.system_info import get_os_info, check_python_status
from checks.security_config import check_firewall, check_ssh_config # <-- Nouveau !
from utils.scanner import scan_ports
from utils.reporter import generate_report

def run_audit():
    print("🚀 Lancement de l'audit de sécurité local...\n")
    results = {}
    
    # 1. Infos Système
    results["Système"] = get_os_info()
    results["Python"] = check_python_status()
    
    # 2. Config Sécurité (Provenant de security_config.py)
    print("[*] Analyse des configurations de sécurité...")
    results["Pare-feu"] = check_firewall()
    results["SSH Config"] = check_ssh_config()
    
    # 3. Réseau
    print("[*] Scan des ports locaux (20-1024)...")
    open_p = scan_ports()
    results["Ports Ouverts"] = open_p if open_p else "Aucun port critique détecté"
    
    # 4. Rapport
    file_path = generate_report(results)
    print(f"\n✅ Audit terminé ! Rapport : {file_path}")

if __name__ == "__main__":
    run_audit()