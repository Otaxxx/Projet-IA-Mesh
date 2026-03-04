from .rag_engine import executer_rag
import time

def demo():
    print("=== TEST DU SYSTÈME RAG ===")
    
    question = "  quel est le lien entre un reseau maillé et une IA ? "
    
    print(f"\nQuestion posée : {question}")
    
    start = time.time()
    reponse = executer_rag(question)
    end = time.time()
    
    print("-" * 30)
    print(reponse)
    print("-" * 30)
    print(f"Temps de traitement : {round(end - start, 2)}s")

if __name__ == "__main__":
    demo()