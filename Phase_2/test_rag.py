# Teste le moteur RAG avec une question
from .rag_engine import executer_rag
import time

def demo():
    question = "quel est le lien entre un reseau maillé et une IA ?"
    
    print(f"Question : {question}")
    
    start = time.time()
    reponse = executer_rag(question)
    elapsed = round(time.time() - start, 2)
    
    print(f"\nRéponse : {reponse}")
    print(f"Temps : {elapsed}s")

if __name__ == "__main__":
    demo()