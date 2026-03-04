# Moteur RAG : récupère le contexte pertinent des articles et génère des réponses courtes
import os, sys, re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
from Phase_1.core_ollama import demander_a_ia

DOCS_DIR = BASE_DIR / "articles_propres"
_ARTICLES, _CONTENTS = None, None

# Charge les articles en cache
def _load_docs():
    global _ARTICLES, _CONTENTS
    if _ARTICLES is not None:
        return _ARTICLES, _CONTENTS
    _ARTICLES, _CONTENTS = [], {}
    if DOCS_DIR.exists():
        for f in os.listdir(DOCS_DIR):
            if f.endswith(".txt"):
                name = f[:-4]
                _ARTICLES.append(name)
                with open(DOCS_DIR / f, "r", encoding="utf-8") as fh:
                    _CONTENTS[name] = fh.read()
    return _ARTICLES, _CONTENTS

# Extrait les phrases les plus pertinentes du texte
def _best_context(q, text, max_chars=1200):
    q_terms = set(re.findall(r"\w+", q.lower()))
    sentences = re.split(r"(?<=[\.?\!])\s+|\n+", text)
    ranked = sorted((s for s in sentences if s.strip()), 
                    key=lambda s: sum(1 for t in re.findall(r"\w+", s.lower()) if t in q_terms), 
                    reverse=True)
    ctx, total = [], 0
    for s in ranked:
        if total + len(s) > max_chars:
            break
        ctx.append(s.strip())
        total += len(s)
    return " ".join(ctx) if ctx else text[:max_chars]

# Sélectionne le meilleur article pour la question
def choisir_meilleur_article(question):
    articles, _ = _load_docs()
    if not articles:
        return None
    ql = question.lower()
    # Cherche d'abord une correspondance directe
    for a in articles:
        if a.lower() in ql:
            return a
    # Sinon demande à l'IA
    liste = "\n".join(f"{i+1}. {t}" for i, t in enumerate(articles))
    prompt = f"Choisis le doc pour: {question}\nDOCS:\n{liste}\nRéponds UNIQUEMENT par le chiffre. Sinon 0."
    rep = demander_a_ia(prompt, max_tokens=5).strip()
    m = re.search(r"\d+", rep)
    if m:
        idx = int(m.group()) - 1
        if 0 <= idx < len(articles):
            return articles[idx]
    return None

# Exécute le pipeline RAG complet
def executer_rag(question):
    articles, contents = _load_docs()
    liste_sujets = ", ".join(articles)
    
    # Cas spécial : énumère les sujets disponibles
    if any(m in question.lower() for m in ["sujet", "connais", "liste"]):
        return f"Sujets: {liste_sujets}"[:190]
        
    # Sélectionne et cherche l'article pertinent
    art = choisir_meilleur_article(question)
    if art:
        ctx = _best_context(question, contents.get(art, ""), max_chars=800)
        # Demande une réponse très courte à l'IA
        prompt = (
            f"CONTEXTE: {ctx}\n"
            f"QUESTION: {question}\n"
            "Réponds en une seule phrase très courte (15-20 mots max). "
            "Ta réponse doit être complète et se terminer par un point."
        )
        rep = demander_a_ia(prompt, max_tokens=60).strip()
        final = f"[{art}] {rep}"
    else:
        final = f"Inconnu. Sujets: {liste_sujets}"

    # Tronque si trop long
    if len(final) > 190:
        zone_recherche = final[:190]
        dernier_point = max(zone_recherche.rfind('.'), zone_recherche.rfind('?'), zone_recherche.rfind('!'))
        
        if dernier_point > 100:
            final = zone_recherche[:dernier_point + 1]
        else:
            final = zone_recherche.rsplit(' ', 1)[0] + "..."
            
    return final