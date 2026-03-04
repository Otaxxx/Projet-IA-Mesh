# Projet LoRa RAG (Ollama + Meshtastic)

Projet Python qui :
- telecharge et nettoie des articles Wikipedia
- repond a des questions via un mini moteur RAG
- sert de bridge LoRa (Meshtastic) vers l'IA

## Prerequis
- Windows 10/11
- Python 3.10+ (recommande)
- Ollama installe et lance

## Installation
Depuis la racine du projet :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install ollama wikipedia-api meshtastic pypubsub
```

## Ollama
Lancer Ollama et telecharger le modele :

```powershell
ollama pull llama3.2
```

## 1) Telechargement des articles

```powershell
python Phase_2/telecharger_article.py
python Phase_2/clean_data.py
```

## 2) Test IA simple

```powershell
python Phase_1/test_ai.py
```

## 3) Test du moteur RAG

```powershell
python -m Phase_2.test_rag
```

## 4) Bridge LoRa (Meshtastic)
1. Brancher le device Meshtastic
2. Ouvrir `Phase_4/bridge_seriel.py` et regler le port serie :
   - `PORT_COM = "PORT COM SOUAHITE"` (ex: "COM3")
3. Mettre a jour les utilisateurs autorises dans `Phase_5/whitelist.py`

Lancer le bridge :

```powershell
python Phase_4/bridge_seriel.py
```

## Depannage rapide
- Ollama : verifier que le service est lance et que le modele existe.
- Meshtastic : verifier le port COM et les drivers du device.
- Acces refuse : ajouter l'ID Meshtastic dans `Phase_5/whitelist.py`.

## Structure
- `Phase_1/` : connexion Ollama
- `Phase_2/` : RAG + nettoyage + telechargement
- `Phase_4/` : bridge LoRa
- `Phase_5/` : whitelist des IDs autorises