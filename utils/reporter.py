# Génération du rapport final

import datetime

def generate_report(data):
    report_name = f"rapport_audit_{datetime.date.today()}.txt"
    
    with open(report_name, "w", encoding="utf-8") as f:
        f.write("="*30 + "\n")
        f.write(f" RAPPORT D'AUTO-AUDIT SÉCURITÉ\n")
        f.write(f" Date : {datetime.datetime.now()}\n")
        f.write("="*30 + "\n\n")
        
        for key, value in data.items():
            f.write(f"[{key.upper()}] : {value}\n")
            
    return report_name