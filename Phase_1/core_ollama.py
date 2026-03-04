import os
import ollama

# Config modèle et CPU
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
CPU_THREADS = max(2, (os.cpu_count() or 4))

# Envoie une requête à l'IA et retourne la réponse
def demander_a_ia(prompt, *, max_tokens=96):
    try:
        resp = ollama.chat(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant expert et concis. "
                        "Réponds directement en quelques phrases, sans politesse."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            options={
                "num_predict": max_tokens,
                "temperature": 0.1,  # Déterministe
                "num_thread": CPU_THREADS,
                "top_p": 0.9,
            },
        )

        # Retourne la réponse complète
        return resp["message"]["content"]
    except Exception as e:
        return f"Erreur : {e}"