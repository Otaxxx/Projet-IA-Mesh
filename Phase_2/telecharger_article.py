import wikipediaapi
import os

def telecharger_articles():
    wiki = wikipediaapi.Wikipedia(
        user_agent="Projet_L3_OffGrid (ton_email@exemple.com)",
        language='fr'
    )
    
    # Ta liste des 6 articles
    sujets = [
        "Orelsan",
        "LoRaWAN",                          # Le standard du réseau LoRa
        "Réseau maillé",                    # Le nom exact pour "Mesh"
        "Intelligence artificielle",
        "Micro-informatique",
        "Interface de programmation",       # Le nom exact pour "API"
        "Apprentissage automatique"         # Le nom exact pour "Machine Learning"
    ]
    
    if not os.path.exists('articles_bruts'):
        os.makedirs('articles_bruts')

    for sujet in sujets:
        page = wiki.page(sujet)
        if page.exists():
            nom_fichier = sujet.replace(" ", "_").replace("'", "_") + ".txt"
            with open(f"articles_bruts/{nom_fichier}", "w", encoding="utf-8") as f:
                f.write(page.text)
            print(f"✓ {sujet} téléchargé.")
        else:
            print(f"✗ {sujet} introuvable sur Wikipédia.")

if __name__ == "__main__":
    telecharger_articles()