import requests

# URL de l'API
base_url = "http://0.0.0.0:8080"

'''
# Données pour créer un nouveau post avec un utilisateur special
post = {
    "title": "Mon nouveau post",
    "body": "Contenu de mon nouveau post"
}

headers = {"authorization": "utilisateur_special"}

# Envoi d'une requête POST pour créer un nouveau post avec l'utilisateur spécifié
response = requests.post(f"{base_url}/posts", json=post, headers=headers)

if response.status_code == 200:
    print("Réponse du serveur :", response.json())
else:
    print("Erreur lors de la création du post :")
    print("Code de statut HTTP :", response.status_code)
    print("Message d'erreur :", response.text)
'''

'''
# Recuperation de tous les posts

response2 = requests.get(f"{base_url}/posts")

if response2.status_code == 200:
    print("Réponse du serveur :", response2.json())
else:
    print("Erreur lors de la lecture des posts :")
    print("Code de statut HTTP :", response2.status_code)
    print("Message d'erreur :", response2.text)
'''

'''
# Recuperation des posts de utilisateur special

response3 = requests.get(f"{base_url}/posts?user=utilisateur_special")

if response3.status_code == 200:
    print("Réponse du serveur :", response3.json())
else:
    print("Erreur lors de la lecture des posts :")
    print("Code de statut HTTP :", response3.status_code)
    print("Message d'erreur :", response3.text)
'''
