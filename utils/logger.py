import logging
import os

def setup_logging():
    """Configure le système de log pour écrire dans un fichier et sur la console."""
    log_format = "%(asctime)s - [%(levelname)s] - %(message)s"
    
    # Configuration de base
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler("audit_trace.log", encoding="utf-8"), # Sauvegarde dans un fichier
            logging.StreamHandler() # Affiche aussi dans la console
        ]
    )
    return logging.getLogger("CyberAudit")