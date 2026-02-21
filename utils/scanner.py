import socket

def scan_ports(port_range=range(20, 1025)):
    """Scanne les ports locaux pour détecter des services ouverts."""
    open_ports = []
    target = "127.0.0.1"
    
    for port in port_range:
        # Utilisation de 'with' pour fermer le socket automatiquement
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.01) # Scan rapide en local
            if s.connect_ex((target, port)) == 0:
                open_ports.append(port)
    return open_ports