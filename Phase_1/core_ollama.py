import os
import ollama

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
CPU_THREADS = max(2, (os.cpu_count() or 4))

def demander_a_ia(prompt, *, max_tokens=96, stream=False):
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
                "temperature": 0.1,
                "num_thread": CPU_THREADS,
                "top_p": 0.9,
            },
            stream=stream,
        )

        if stream:
            chunks = []
            for chunk in resp:
                content = chunk.get("message", {}).get("content", "")
                if content:
                    print(content, end="", flush=True)
                    chunks.append(content)
            print()
            return "".join(chunks)
        else:
            return resp["message"]["content"]
    except Exception as e:
        return f"Erreur : {e}"