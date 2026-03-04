# Bridge Meshtastic : reçoit les messages du réseau LoRa, interroge l'IA, renvoie les réponses
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import sys, time
from pathlib import Path

# Importe RAG et Whitelist
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

try:
    from Phase_2.rag_engine import executer_rag
    from Phase_5.whitelist import ALLOWED_USERS
except ImportError:
    print("Erreur : Phase_2/rag_engine.py ou Phase_5/whitelist.py introuvable.")
    sys.exit()

# Callback appelé à la réception d'un message LoRa
def on_receive(packet, interface):
    try:
        # Traite uniquement les messages texte
        if 'decoded' in packet and packet['decoded'].get('portnum') == 'TEXT_MESSAGE_APP':
            
            # Ignore les messages du bridge lui-même
            if packet.get('from') == interface.myInfo.my_node_num:
                return

            sender = packet['fromId']
            
            # Vérifie l'autorisation de l'utilisateur
            if sender not in ALLOWED_USERS:
                print(f"ACCES REFUSE : {sender} non autorisé.")
                return

            question = packet['decoded']['text']
            print(f"ACCES OK : {sender}")
            print(f"Question : {question}")
            
            # Génère la réponse via RAG
            reponse = executer_rag(question)
            
            # Envoie la réponse au réseau
            print(f"ENVOI ({len(reponse)} octets) : {reponse}")
            interface.sendText(reponse, destinationId=sender)
            print("Transmis.")

    except Exception as e:
        print(f"Erreur : {e}")

def main():
    # port COM specifique
    PORT_COM = 'COM6' 
    
    print("========================================")
    print("BRIDGE LORA-RAG SECURISE DEMARRE")
    print(f"Connexion sur : {PORT_COM}")
    print(f"Nombre d'utilisateurs autorises : {len(ALLOWED_USERS)}")
    print("========================================")

    try:
        # Initialisation de l'interface avec le bon argument devPath
        interface = meshtastic.serial_interface.SerialInterface(devPath=PORT_COM)
        
        # Abonnement aux messages entrants
        pub.subscribe(on_receive, "meshtastic.receive")
        
        print("En attente de messages sur le canal LoRa...")
        
        # Boucle infinie pour maintenir le script actif
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"Impossible de se connecter au module Meshtastic : {e}")
        sys.exit()

if __name__ == "__main__":
    main()