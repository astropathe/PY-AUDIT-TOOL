import datetime
import os

def generate_report(data):
    # 1. Définir le nom du dossier
    folder_name = "reports"
    
    # 2. Créer le dossier s'il n'existe pas encore
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    # 3. Préparer le nom du fichier avec le timestamp précis
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%Hh%Mm%Ss")
    file_name = f"rapport_audit_{timestamp}.txt"
    
    # 4. Créer le chemin complet (ex: reports/rapport_audit_...txt)
    file_path = os.path.join(folder_name, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("="*40 + "\n")
        f.write(f" 🛡️ RAPPORT D'AUTO-AUDIT SÉCURITÉ\n")
        f.write(f" Généré le : {now.strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write("="*40 + "\n\n")
        
        for key, value in data.items():
            f.write(f"[{key.upper()}] : {value}\n")
            
    return file_path