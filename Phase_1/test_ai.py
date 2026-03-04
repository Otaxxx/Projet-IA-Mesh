from core_ollama import demander_a_ia

print("--- TEST CONNEXION IA ---")
question = " parle moi de micro informatique"
reponse = demander_a_ia(question)

print(f"Question : {question}")
print(f"Réponse de l'IA : {reponse}")