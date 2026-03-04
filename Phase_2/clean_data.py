import os
import re

def nettoyer_et_transformer():
    if not os.path.exists('articles_propres'):
        os.makedirs('articles_propres')

    for fichier in os.listdir('articles_bruts'):
        if fichier.endswith(".txt"):
            with open(f"articles_bruts/{fichier}", "r", encoding="utf-8") as f:
                texte = f.read()

            # --- TRANSFORMATION AVANCÉE ---
            # 1. On enlève les balises de style Wikipédia (ex: [[Lien|Texte]])
            texte = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', texte)
            
            # 2. On enlève les références entre crochets (ex: [1], [2-5])
            texte = re.sub(r'\[\d+\]|\[\d+-\d+\]', '', texte)

            # 3. On enlève les sections inutiles (Bibliographie, Liens externes, etc.)
            sections_a_supprimer = ["Notes et références", "Bibliographie", "Articles connexes", "Liens externes"]
            for section in sections_a_supprimer:
                texte = texte.split(section)[0]

            # 4. On compacte les espaces
            texte = " ".join(texte.split())

            # 5. NOUVELLE LIMITE : 10000 caractères pour plus de profondeur
            texte_final = texte[:10000]

            with open(f"articles_propres/{fichier}", "w", encoding="utf-8") as f:
                f.write(texte_final)
            print(f"🚀 {fichier} transformé (version longue : {len(texte_final)} car.)")

if __name__ == "__main__":
    nettoyer_et_transformer()