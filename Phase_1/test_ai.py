# Test basique de connexion à l'IA Ollama
from core_ollama import demander_a_ia

question = "parle moi de micro informatique"
reponse = demander_a_ia(question)

print(f"Question : {question}")
print(f"Réponse : {reponse}")