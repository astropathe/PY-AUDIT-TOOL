import os
from utils.logger import setup_logging
from utils.scanner import scan_ports
from utils.reporter import generate_report
from checks.system_info import get_os_info, check_python_status, get_privilege_status
from checks.security_config import check_firewall, check_ssh_config, check_antivirus

def run_audit():
    # 1. Initialisation du logger (console + fichier audit_trace.log)
    logger = setup_logging()
    logger.info("="*50)
    logger.info("DÉMARRAGE DE L'OUTIL D'AUDIT SÉCURITÉ")
    logger.info("="*50)

    results = {}

    try:
        # 2. Vérification des privilèges
        # Crucial pour savoir si les résultats suivants seront fiables
        results["Droits d'exécution"] = get_privilege_status()
        logger.info(f"Niveau de privilèges : {results["Droits d'exécution"]}")

        # 3. Analyse du Système
        logger.info("Analyse des informations système...")
        results["Système"] = get_os_info()
        results["Python"] = check_python_status()
        
        # 4. Analyse de la configuration de sécurité
        logger.info("Vérification des paramètres de sécurité (Firewall, AV, SSH)...")
        results["Pare-feu"] = check_firewall()
        results["Antivirus"] = check_antivirus()
        results["SSH Config"] = check_ssh_config()
        
        # 5. Analyse réseau (Scan de ports locaux)
        logger.info("Scan des ports locaux (20-1024) en cours...")
        open_p = scan_ports()
        if open_p:
            results["Ports Ouverts"] = f"⚠️ {len(open_p)} port(s) détecté(s) : {open_p}"
            logger.warning(f"Attention : Ports ouverts trouvés : {open_p}")
        else:
            results["Ports Ouverts"] = "✅ Aucun port critique exposé"
            logger.info("Aucun port critique ouvert détecté.")

        # 6. Calcul d'un score de sécurité rapide (Optionnel/Pédagogique)
        score = 100
        if "❌" in results["Pare-feu"]: score -= 30
        if "❌" in results["Antivirus"]: score -= 30
        if "⚠️" in results["Python"]: score -= 10
        if open_p: score -= 10
        results["Score de Sécurité global"] = f"{score}/100"

        # 7. Génération du rapport dans le dossier /reports
        logger.info("Génération du rapport final...")
        report_path = generate_report(results)
        
        print("\n" + "*"*30)
        print(f"✅ AUDIT TERMINÉ AVEC SUCCÈS")
        print(f"📊 SCORE : {results['Score de Sécurité global']}")
        print(f"📄 FICHIER : {report_path}")
        print("*"*30)
        
        logger.info(f"Audit terminé. Rapport disponible ici : {report_path}")

    except KeyboardInterrupt:
        logger.error("L'audit a été interrompu par l'utilisateur.")
    except Exception as e:
        logger.error(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    run_audit()