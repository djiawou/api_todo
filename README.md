# API de Gestion des Tâches

Cette API permet de gérer des tâches avec des utilisateurs assignés, des statuts et des dates d'échéance.

## Configuration

Assurez-vous d'avoir un fichier `.env` avec les configurations suivantes 

    MONGO_URI=mongodb://<votre_mongodb_uri>


## Installation

1. Cloner le projet :

```bash
git clone <url_du_projet>
cd <nom_du_projet>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run -p <numero_port> (default= 5000)

## Endpoints
1. Créer une Tâche
URL : /tasks
Méthode : POST
Description : Crée une nouvelle tâche.

2. Mettre à Jour une Tâche
URL : /tasks/<task_id>
Méthode : PUT
Description : Met à jour une tâche existante.

3. Supprimer une Tâche
URL : /tasks/<task_id>
Méthode : DELETE
Description : Supprime une tâche existante.

4. Récupérer les Tâches d'un Utilisateur
URL : /tasks/user/<user_id>
Méthode : GET
Description : Récupère toutes les tâches assignées à un utilisateur spécifique.

5. Mettre à Jour le Statut d'une Tâche
URL : /tasks/<task_id>/status
Méthode : PATCH
Description : Met à jour uniquement le statut d'une tâche.




## Notes 
    fichier de test api.jon pour les reponses des requetes 
