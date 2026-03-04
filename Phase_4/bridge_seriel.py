import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import sys, time
from pathlib import Path

# import RAG et Whitelist
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

try:
    from Phase_2.rag_engine import executer_rag
    from Phase_5.whitelist import ALLOWED_USERS
except ImportError:
    print("Erreur : Phase_2/rag_engine.py ou Phase_5/whitelist.py introuvable.")
    sys.exit()

def on_receive(packet, interface):
    """Fonction appelee a chaque reception de message LoRa."""
    try:
        # traite que les messages texte 
        if 'decoded' in packet and packet['decoded'].get('portnum') == 'TEXT_MESSAGE_APP':
            
            # ignore les messages que le bridge envoie lui-meme
            if packet.get('from') == interface.myInfo.my_node_num:
                return

            sender = packet['fromId'] # L'ID de l'emetteur 
            
            # Verification de l'ID de l'emetteur
            if sender not in ALLOWED_USERS:
                print(f"ACCES REFUSE : L'utilisateur {sender} n'est pas autorise.")
                return

            question = packet['decoded']['text']
            
            print(f"ACCES AUTORISE pour {sender}")
            print(f"Question recue : {question}")
            
            # Generation de la reponse via le moteur RAG
            print("Generation de la reponse...")
            reponse = executer_rag(question)
            
            # Envoi de la reponse via le XIAO
            print(f"ENVOI ({len(reponse)} octets) : {reponse}")
            interface.sendText(reponse, destinationId=sender)
            print("Transmis avec succes au reseau Mesh.")

    except Exception as e:
        print(f"Erreur lors du traitement du paquet : {e}")

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