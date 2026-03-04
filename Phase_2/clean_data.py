# Nettoie les articles bruts (supprime balises, références, sections inutiles)
import os
import re

def nettoyer_et_transformer():
    # Crée le dossier de sortie
    if not os.path.exists('articles_propres'):
        os.makedirs('articles_propres')

    for fichier in os.listdir('articles_bruts'):
        if fichier.endswith(".txt"):
            with open(f"articles_bruts/{fichier}", "r", encoding="utf-8") as f:
                texte = f.read()

            # Supprime balises Wikipédia [[...]]
            texte = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', texte)
            
            # Supprime références numériques [...]
            texte = re.sub(r'\[\d+\]|\[\d+-\d+\]', '', texte)

            # Supprime sections inutiles
            sections_a_supprimer = ["Notes et références", "Bibliographie", "Articles connexes", "Liens externes"]
            for section in sections_a_supprimer:
                texte = texte.split(section)[0]

            # Compacte les espaces
            texte = " ".join(texte.split())

            # Limite à 10000 caractères
            texte_final = texte[:10000]

            with open(f"articles_propres/{fichier}", "w", encoding="utf-8") as f:
                f.write(texte_final)
            print(f"✓ {fichier} transformé ({len(texte_final)} car.)")

if __name__ == "__main__":
    nettoyer_et_transformer()